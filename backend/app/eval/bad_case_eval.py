"""Bad Case Evaluation Harness.

Loads bad cases from bad_cases.jsonl, runs the agent workflow,
and evaluates each case against expected behavior.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from app.agent.schemas import AgentResponse
from app.agent.workflow import run_customer_service_agent
from app.eval.bad_case_schema import BadCase


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def get_default_bad_cases_path() -> Path:
    """Return the default path to the bad cases JSONL file."""
    return Path(__file__).resolve().parent / "bad_cases.jsonl"


# ---------------------------------------------------------------------------
# Load bad cases
# ---------------------------------------------------------------------------

def load_bad_cases(path: Path | str | None = None) -> list[BadCase]:
    """Load and validate bad cases from a JSONL file.

    Args:
        path: Path to the JSONL file.

    Returns:
        List of validated BadCase instances.
    """
    if path is None:
        path = get_default_bad_cases_path()
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Bad cases file not found: {path}")

    cases: list[BadCase] = []
    with open(path, encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_num}: {exc}") from exc
            try:
                case = BadCase(**data)
            except Exception as exc:
                raise ValueError(f"Schema validation failed on line {line_num}: {exc}") from exc
            cases.append(case)
    return cases


# ---------------------------------------------------------------------------
# Per-case evaluation result
# ---------------------------------------------------------------------------

@dataclass
class BadCaseResult:
    """Evaluation result for a single bad case."""

    case_id: str
    user_query: str
    scenario: str
    expected_route: str
    expected_intent: str
    expected_detail_intent: str | None
    actual_route: str
    actual_intent: str
    actual_detail_intent: str
    fallback_triggered: bool
    fallback_reason: str | None
    has_citations: bool
    citation_count: int
    answer: str
    route_match: bool
    intent_match: bool
    has_next_step: bool
    is_out_of_scope_handled: bool
    status: str  # pass / partial / fail
    failure_reasons: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Evaluation logic
# ---------------------------------------------------------------------------

_NEXT_STEP_KEYWORDS = [
    "建议", "可以", "请", "登录", "联系", "查看", "提供", "提交",
    "操作", "申请", "确认", "检查", "稍后", "重试",
    "suggest", "recommend", "please", "contact", "check", "try",
    "log in", "visit", "provide", "submit",
]

_OUT_OF_SCOPE_REJECT_KEYWORDS = [
    "超出", "服务范围", "无法", "不支持", "只能", "主要处理",
    "超出了我的服务范围", "无法匹配", "跨境电商客服",
    "out of scope", "service range", "not support", "cannot assist",
    "customer service",
]


def _check_route_match(expected: str, actual: str) -> bool:
    """Check if actual route matches expected route."""
    if expected == actual:
        return True
    # Fallback is acceptable when out_of_scope is expected
    if expected == "fallback" and actual == "fallback":
        return True
    return False


def _check_intent_match(expected: str, actual: str) -> bool:
    """Check if actual intent matches expected intent."""
    if expected == actual:
        return True
    # aftersale and trace are both RAG routes
    if expected in ("aftersale", "trace") and actual in ("aftersale", "trace"):
        return True
    return False


def _check_has_next_step(answer: str) -> bool:
    """Check if answer contains next-step suggestions."""
    answer_lower = answer.lower()
    return any(kw in answer_lower for kw in _NEXT_STEP_KEYWORDS)


def _check_out_of_scope_rejection(answer: str) -> bool:
    """Check if out_of_scope case is properly rejected."""
    answer_lower = answer.lower()
    return any(kw in answer_lower for kw in _OUT_OF_SCOPE_REJECT_KEYWORDS)


def evaluate_bad_case(case: BadCase, response: AgentResponse) -> BadCaseResult:
    """Evaluate a single bad case against the agent response.

    Args:
        case: The bad case to evaluate.
        response: The agent's response.

    Returns:
        BadCaseResult with all metrics and pass/fail status.
    """
    route_match = _check_route_match(case.expected_route, response.route)
    intent_match = _check_intent_match(case.expected_intent, response.intent)
    has_citations = len(response.citations) > 0
    has_next_step = _check_has_next_step(response.answer)
    is_oos_handled = True

    failure_reasons: list[str] = []

    # Route check
    if not route_match:
        failure_reasons.append(f"route mismatch: expected={case.expected_route}, actual={response.route}")

    # Intent check
    if not intent_match:
        failure_reasons.append(f"intent mismatch: expected={case.expected_intent}, actual={response.intent}")

    # Citation check for RAG cases
    if case.expected_route == "rag_knowledge_base" and not has_citations:
        failure_reasons.append("RAG route but no citations")

    # Out-of-scope check
    if case.scenario == "out_of_scope":
        is_oos_handled = _check_out_of_scope_rejection(response.answer)
        if not is_oos_handled:
            failure_reasons.append("out_of_scope case not properly rejected")
        if response.route != "fallback":
            failure_reasons.append(f"out_of_scope should use fallback, got {response.route}")

    # Next-step check
    if not has_next_step and case.scenario != "out_of_scope":
        failure_reasons.append("missing next-step suggestion")

    # Determine status
    if len(failure_reasons) == 0:
        status = "pass"
    elif route_match and intent_match:
        status = "partial"
    else:
        status = "fail"

    return BadCaseResult(
        case_id=case.case_id,
        user_query=case.user_query,
        scenario=case.scenario,
        expected_route=case.expected_route,
        expected_intent=case.expected_intent,
        expected_detail_intent=case.expected_detail_intent,
        actual_route=response.route,
        actual_intent=response.intent,
        actual_detail_intent=response.detail_intent,
        fallback_triggered=response.fallback_triggered,
        fallback_reason=response.fallback_reason,
        has_citations=has_citations,
        citation_count=len(response.citations),
        answer=response.answer,
        route_match=route_match,
        intent_match=intent_match,
        has_next_step=has_next_step,
        is_out_of_scope_handled=is_oos_handled,
        status=status,
        failure_reasons=failure_reasons,
    )


# ---------------------------------------------------------------------------
# Aggregate report
# ---------------------------------------------------------------------------

@dataclass
class BadCaseEvalReport:
    """Aggregate bad case evaluation report."""

    total: int
    pass_count: int
    partial_count: int
    fail_count: int
    pass_rate: float
    scenario_distribution: dict[str, int]
    scenario_pass_rate: dict[str, float]
    failure_type_distribution: dict[str, int]
    citation_coverage: float
    fallback_rate: float
    per_case_results: list[BadCaseResult]


# ---------------------------------------------------------------------------
# Evaluate all bad cases
# ---------------------------------------------------------------------------

def evaluate_bad_cases(cases: list[BadCase]) -> BadCaseEvalReport:
    """Run agent workflow on all bad cases and evaluate.

    Args:
        cases: List of bad cases.

    Returns:
        BadCaseEvalReport with aggregate metrics.
    """
    per_case_results: list[BadCaseResult] = []

    for case in cases:
        response = run_customer_service_agent(case.user_query, top_k=5)
        result = evaluate_bad_case(case, response)
        per_case_results.append(result)

    total = len(per_case_results)
    if total == 0:
        return BadCaseEvalReport(
            total=0, pass_count=0, partial_count=0, fail_count=0,
            pass_rate=0.0, scenario_distribution={}, scenario_pass_rate={},
            failure_type_distribution={}, citation_coverage=0.0,
            fallback_rate=0.0, per_case_results=[],
        )

    pass_count = sum(1 for r in per_case_results if r.status == "pass")
    partial_count = sum(1 for r in per_case_results if r.status == "partial")
    fail_count = sum(1 for r in per_case_results if r.status == "fail")
    pass_rate = pass_count / total

    # Scenario distribution
    scenario_counts: dict[str, int] = Counter(r.scenario for r in per_case_results)
    scenario_pass: dict[str, int] = Counter(
        r.scenario for r in per_case_results if r.status == "pass"
    )
    scenario_pass_rate = {
        s: scenario_pass.get(s, 0) / c for s, c in scenario_counts.items()
    }

    # Failure type distribution (from bad case definitions, not results)
    failure_type_counts: dict[str, int] = Counter()
    for case in cases:
        for ft in case.failure_type:
            failure_type_counts[ft] += 1

    # Citation coverage
    rag_cases = [r for r in per_case_results if r.expected_route == "rag_knowledge_base"]
    citation_coverage = (
        sum(1 for r in rag_cases if r.has_citations) / len(rag_cases) if rag_cases else 0.0
    )

    # Fallback rate
    fallback_count = sum(1 for r in per_case_results if r.fallback_triggered)
    fallback_rate = fallback_count / total

    return BadCaseEvalReport(
        total=total,
        pass_count=pass_count,
        partial_count=partial_count,
        fail_count=fail_count,
        pass_rate=pass_rate,
        scenario_distribution=dict(scenario_counts),
        scenario_pass_rate=scenario_pass_rate,
        failure_type_distribution=dict(failure_type_counts),
        citation_coverage=citation_coverage,
        fallback_rate=fallback_rate,
        per_case_results=per_case_results,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 60)
    print("  Bad Case Evaluation Harness")
    print("=" * 60)
    print()

    cases = load_bad_cases()
    print(f"Loaded {len(cases)} bad cases")
    print()

    report = evaluate_bad_cases(cases)

    print(f"Total:              {report.total}")
    print(f"Pass:               {report.pass_count}")
    print(f"Partial:            {report.partial_count}")
    print(f"Fail:               {report.fail_count}")
    print(f"Pass Rate:          {report.pass_rate:.2%}")
    print(f"Citation Coverage:  {report.citation_coverage:.2%}")
    print(f"Fallback Rate:      {report.fallback_rate:.2%}")
    print()

    print("-" * 60)
    print("  Scenario Distribution")
    print("-" * 60)
    for s in sorted(report.scenario_distribution.keys()):
        count = report.scenario_distribution[s]
        pr = report.scenario_pass_rate.get(s, 0.0)
        print(f"  {s:20s}  {count:3d}  pass_rate={pr:.2%}")
    print()

    print("-" * 60)
    print("  Failure Type Distribution (from case definitions)")
    print("-" * 60)
    for ft, count in sorted(report.failure_type_distribution.items(), key=lambda x: -x[1]):
        print(f"  {ft:30s}  {count:3d}")
    print()

    # Show failed cases (top 10)
    failed = [r for r in report.per_case_results if r.status == "fail"]
    if failed:
        print("-" * 60)
        print(f"  Failed Cases (top 10 of {len(failed)})")
        print("-" * 60)
        for fc in failed[:10]:
            print(f"  case_id:    {fc.case_id}")
            print(f"  scenario:   {fc.scenario}")
            print(f"  route:      expected={fc.expected_route} actual={fc.actual_route}")
            print(f"  intent:     expected={fc.expected_intent} actual={fc.actual_intent}")
            print(f"  reasons:    {'; '.join(fc.failure_reasons)}")
            print()
