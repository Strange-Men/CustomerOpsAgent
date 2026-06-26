"""Tests for Bad Case Bank schema and data quality."""

from __future__ import annotations

import json
from pathlib import Path

from app.eval.bad_case_schema import (
    BadCase,
    VALID_AFTER_STATUSES,
    VALID_BASELINE_STATUSES,
    VALID_FAILURE_TYPES,
    VALID_INTENTS,
    VALID_ROUTES,
    VALID_SCENARIOS,
    validate_bad_case,
)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BAD_CASES_PATH = Path(__file__).resolve().parent.parent / "app" / "eval" / "bad_cases.jsonl"


def _load_all_cases() -> list[BadCase]:
    """Load all bad cases from the JSONL file."""
    cases: list[BadCase] = []
    with open(BAD_CASES_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(BadCase(**json.loads(line)))
    return cases


# ---------------------------------------------------------------------------
# Test: loading and schema validation
# ---------------------------------------------------------------------------


class TestBadCaseLoading:
    """Test that bad cases load and validate correctly."""

    def test_file_exists(self) -> None:
        """bad_cases.jsonl must exist."""
        assert BAD_CASES_PATH.exists(), f"File not found: {BAD_CASES_PATH}"

    def test_load_all_cases(self) -> None:
        """All cases must load without validation errors."""
        cases = _load_all_cases()
        assert len(cases) > 0, "No cases loaded"

    def test_minimum_case_count(self) -> None:
        """Must have at least 120 bad cases."""
        cases = _load_all_cases()
        assert len(cases) >= 120, f"Expected >= 120 cases, got {len(cases)}"


# ---------------------------------------------------------------------------
# Test: field presence and value constraints
# ---------------------------------------------------------------------------


class TestBadCaseFields:
    """Test that each case has valid fields."""

    def test_case_id_unique(self) -> None:
        """case_id must be unique across all cases."""
        cases = _load_all_cases()
        ids = [c.case_id for c in cases]
        assert len(ids) == len(set(ids)), "Duplicate case_id found"

    def test_user_query_not_empty(self) -> None:
        """user_query must not be empty."""
        cases = _load_all_cases()
        for c in cases:
            assert c.user_query.strip(), f"Empty user_query in {c.case_id}"

    def test_scenario_valid(self) -> None:
        """scenario must be a valid value."""
        cases = _load_all_cases()
        for c in cases:
            assert c.scenario in VALID_SCENARIOS, (
                f"Invalid scenario '{c.scenario}' in {c.case_id}"
            )

    def test_expected_route_valid(self) -> None:
        """expected_route must be a valid value."""
        cases = _load_all_cases()
        for c in cases:
            assert c.expected_route in VALID_ROUTES, (
                f"Invalid expected_route '{c.expected_route}' in {c.case_id}"
            )

    def test_expected_intent_valid(self) -> None:
        """expected_intent must be a valid value."""
        cases = _load_all_cases()
        for c in cases:
            assert c.expected_intent in VALID_INTENTS, (
                f"Invalid expected_intent '{c.expected_intent}' in {c.case_id}"
            )

    def test_failure_types_valid(self) -> None:
        """All failure_type values must be valid."""
        cases = _load_all_cases()
        for c in cases:
            for ft in c.failure_type:
                assert ft in VALID_FAILURE_TYPES, (
                    f"Invalid failure_type '{ft}' in {c.case_id}"
                )

    def test_baseline_status_valid(self) -> None:
        """baseline_status must be a valid value."""
        cases = _load_all_cases()
        for c in cases:
            assert c.baseline_status in VALID_BASELINE_STATUSES, (
                f"Invalid baseline_status '{c.baseline_status}' in {c.case_id}"
            )

    def test_after_status_valid(self) -> None:
        """after_status must be a valid value."""
        cases = _load_all_cases()
        for c in cases:
            assert c.after_status in VALID_AFTER_STATUSES, (
                f"Invalid after_status '{c.after_status}' in {c.case_id}"
            )

    def test_expected_behavior_not_empty(self) -> None:
        """expected_behavior must not be empty."""
        cases = _load_all_cases()
        for c in cases:
            assert c.expected_behavior.strip(), (
                f"Empty expected_behavior in {c.case_id}"
            )


# ---------------------------------------------------------------------------
# Test: scenario distribution
# ---------------------------------------------------------------------------


class TestScenarioDistribution:
    """Test that scenarios are reasonably distributed."""

    def test_minimum_scenario_count(self) -> None:
        """Must have at least 6 different scenarios."""
        cases = _load_all_cases()
        scenarios = {c.scenario for c in cases}
        assert len(scenarios) >= 6, f"Only {len(scenarios)} scenarios found"

    def test_out_of_scope_present(self) -> None:
        """Must have out_of_scope cases."""
        cases = _load_all_cases()
        oos = [c for c in cases if c.scenario == "out_of_scope"]
        assert len(oos) >= 5, f"Expected >= 5 out_of_scope cases, got {len(oos)}"

    def test_no_single_scenario_dominates(self) -> None:
        """No single scenario should have more than 30% of cases."""
        cases = _load_all_cases()
        from collections import Counter
        counts = Counter(c.scenario for c in cases)
        total = len(cases)
        for scenario, count in counts.items():
            ratio = count / total
            assert ratio < 0.30, (
                f"Scenario '{scenario}' has {ratio:.1%} of cases (too dominant)"
            )


# ---------------------------------------------------------------------------
# Test: validate_bad_case helper
# ---------------------------------------------------------------------------


class TestValidateBadCase:
    """Test the validate_bad_case helper function."""

    def test_valid_case_no_errors(self) -> None:
        """A valid case should produce no errors."""
        case = BadCase(
            case_id="test_001",
            user_query="测试问题",
            scenario="customs",
            expected_route="rag_knowledge_base",
            expected_intent="aftersale",
            expected_detail_intent="customs",
            expected_behavior="回答应包含清关信息",
            required_evidence=["customs_global_delay_001"],
            failure_type=["incomplete_answer"],
            baseline_status="fail",
            optimization_action="优化清关模板",
            after_status="pending",
            notes="",
        )
        errors = validate_bad_case(case)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_invalid_scenario_detected(self) -> None:
        """Invalid scenario should be caught."""
        case = BadCase(
            case_id="test_002",
            user_query="test",
            scenario="invalid_scenario",
            expected_route="rag_knowledge_base",
            expected_intent="aftersale",
            expected_behavior="test",
        )
        errors = validate_bad_case(case)
        assert any("scenario" in e for e in errors)

    def test_invalid_route_detected(self) -> None:
        """Invalid expected_route should be caught."""
        case = BadCase(
            case_id="test_003",
            user_query="test",
            scenario="customs",
            expected_route="invalid_route",
            expected_intent="aftersale",
            expected_behavior="test",
        )
        errors = validate_bad_case(case)
        assert any("route" in e for e in errors)
