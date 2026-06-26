"""Tests for Bad Case Evaluation Harness."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.eval.bad_case_eval import (
    BadCaseResult,
    _check_has_next_step,
    _check_intent_match,
    _check_out_of_scope_rejection,
    _check_route_match,
    evaluate_bad_case,
    load_bad_cases,
)
from app.eval.bad_case_schema import BadCase


# ---------------------------------------------------------------------------
# Test: load_bad_cases
# ---------------------------------------------------------------------------


class TestLoadBadCases:
    """Test loading bad cases from JSONL."""

    def test_load_default(self) -> None:
        """Loading default path should return >= 120 cases."""
        cases = load_bad_cases()
        assert len(cases) >= 120

    def test_load_returns_bad_case_instances(self) -> None:
        """Loaded cases must be BadCase instances."""
        cases = load_bad_cases()
        assert all(isinstance(c, BadCase) for c in cases)

    def test_load_nonexistent_file(self) -> None:
        """Loading a nonexistent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_bad_cases("/nonexistent/path.jsonl")


# ---------------------------------------------------------------------------
# Test: route matching
# ---------------------------------------------------------------------------


class TestRouteMatch:
    """Test route matching logic."""

    def test_exact_match(self) -> None:
        """Exact route match should return True."""
        assert _check_route_match("rag_knowledge_base", "rag_knowledge_base")

    def test_fallback_match(self) -> None:
        """Fallback expected with fallback actual should match."""
        assert _check_route_match("fallback", "fallback")

    def test_mismatch(self) -> None:
        """Different routes should not match."""
        assert not _check_route_match("rag_knowledge_base", "logistics_tool")


# ---------------------------------------------------------------------------
# Test: intent matching
# ---------------------------------------------------------------------------


class TestIntentMatch:
    """Test intent matching logic."""

    def test_exact_match(self) -> None:
        """Exact intent match should return True."""
        assert _check_intent_match("aftersale", "aftersale")

    def test_aftersale_trace_compatible(self) -> None:
        """aftersale and trace should be compatible."""
        assert _check_intent_match("aftersale", "trace")
        assert _check_intent_match("trace", "aftersale")

    def test_other_mismatch(self) -> None:
        """'other' should not match 'aftersale'."""
        assert not _check_intent_match("other", "aftersale")


# ---------------------------------------------------------------------------
# Test: next step detection
# ---------------------------------------------------------------------------


class TestNextStepDetection:
    """Test next-step keyword detection."""

    def test_chinese_suggestion(self) -> None:
        """Chinese suggestion keywords should be detected."""
        assert _check_has_next_step("建议您联系人工客服")

    def test_english_suggestion(self) -> None:
        """English suggestion keywords should be detected."""
        assert _check_has_next_step("We recommend contacting support")

    def test_no_suggestion(self) -> None:
        """Text without suggestion keywords should return False."""
        assert not _check_has_next_step("这是纯粹的事实陈述")


# ---------------------------------------------------------------------------
# Test: out-of-scope rejection
# ---------------------------------------------------------------------------


class TestOutOfScopeRejection:
    """Test out-of-scope rejection detection."""

    def test_chinese_rejection(self) -> None:
        """Chinese rejection keywords should be detected."""
        assert _check_out_of_scope_rejection("您的问题超出了我的服务范围")

    def test_english_rejection(self) -> None:
        """English rejection keywords should be detected."""
        assert _check_out_of_scope_rejection("This is out of scope for customer service")

    def test_no_rejection(self) -> None:
        """Generic answer without rejection should return False."""
        assert not _check_out_of_scope_rejection("好的，我来帮您写论文")


# ---------------------------------------------------------------------------
# Test: evaluate_bad_case
# ---------------------------------------------------------------------------


class TestEvaluateBadCase:
    """Test single-case evaluation."""

    def test_result_is_bad_case_result(self) -> None:
        """evaluate_bad_case should return a BadCaseResult."""
        from app.agent.schemas import AgentResponse

        case = BadCase(
            case_id="test_eval_001",
            user_query="清关延迟一般是什么原因？",
            scenario="customs",
            expected_route="rag_knowledge_base",
            expected_intent="aftersale",
            expected_detail_intent="customs",
            expected_behavior="回答应包含清关原因",
            required_evidence=["customs_global_delay_001"],
            failure_type=["incomplete_answer"],
            baseline_status="fail",
            optimization_action="优化清关模板",
            after_status="pending",
        )
        response = AgentResponse(
            answer="清关延迟通常由海关抽检、资料缺失等原因导致。建议您查看物流轨迹。",
            route="rag_knowledge_base",
            intent="aftersale",
            detail_intent="customs",
            citations=[],
            fallback_triggered=False,
            fallback_reason=None,
            confidence="medium",
            retrieved_doc_ids=["customs_global_delay_001"],
            order_id=None,
            tool_used=None,
        )
        result = evaluate_bad_case(case, response)
        assert isinstance(result, BadCaseResult)
        assert result.case_id == "test_eval_001"

    def test_pass_when_all_checks_pass(self) -> None:
        """Case should pass when route, intent, citations, and next_step all match."""
        from app.agent.schemas import AgentResponse, Citation

        case = BadCase(
            case_id="test_eval_002",
            user_query="退款多久到账？",
            scenario="refund",
            expected_route="rag_knowledge_base",
            expected_intent="aftersale",
            expected_detail_intent="refund",
            expected_behavior="回答应包含退款时间",
            required_evidence=["refund_eu_policy_001"],
            failure_type=["incomplete_answer"],
            baseline_status="fail",
            optimization_action="优化退款模板",
            after_status="pending",
        )
        response = AgentResponse(
            answer="退款一般7-10个工作日到账。建议您提供订单号查询退款进度。",
            route="rag_knowledge_base",
            intent="aftersale",
            detail_intent="refund",
            citations=[Citation(
                doc_id="refund_eu_policy_001",
                chunk_id="refund_eu_policy_001::chunk_000",
                title="Refund Policy EU",
                source="knowledge_base",
                category="refund",
                market="EU",
                language="zh",
            )],
            fallback_triggered=False,
            fallback_reason=None,
            confidence="medium",
            retrieved_doc_ids=["refund_eu_policy_001"],
            order_id=None,
            tool_used=None,
        )
        result = evaluate_bad_case(case, response)
        assert result.status == "pass"


# ---------------------------------------------------------------------------
# Test: anti-cheating
# ---------------------------------------------------------------------------


class TestAntiCheating:
    """Test that eval data is not leaked into agent code."""

    def test_bad_case_ids_not_in_agent(self) -> None:
        """Agent code must not contain bad case IDs."""
        agent_dir = Path(__file__).resolve().parent.parent / "app" / "agent"
        cases = load_bad_cases()
        case_ids = {c.case_id for c in cases}

        for py_file in agent_dir.glob("*.py"):
            if py_file.name == "__pycache__":
                continue
            content = py_file.read_text(encoding="utf-8")
            for cid in case_ids:
                assert cid not in content, (
                    f"Case ID '{cid}' found in {py_file.name}"
                )

    def test_no_expected_keywords_in_agent(self) -> None:
        """Agent code must not reference expected_keywords or expected_doc_ids."""
        agent_dir = Path(__file__).resolve().parent.parent / "app" / "agent"
        forbidden = ["expected_keywords", "expected_doc_ids", "expected_behavior"]

        for py_file in agent_dir.glob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            for term in forbidden:
                assert term not in content, (
                    f"Eval term '{term}' found in {py_file.name}"
                )


# ---------------------------------------------------------------------------
# Test: public docs safety
# ---------------------------------------------------------------------------


class TestPublicDocsSafety:
    """Test that public docs don't contain secrets or eval internals."""

    def test_no_api_keys_in_bad_case_files(self) -> None:
        """Bad case files must not contain API keys."""
        eval_dir = Path(__file__).resolve().parent.parent / "app" / "eval"
        key_patterns = ["sk-", "api_key", "secret", "bearer"]

        for f in eval_dir.glob("bad_case*"):
            content = f.read_text(encoding="utf-8").lower()
            for pat in key_patterns:
                assert pat not in content, (
                    f"Potential key pattern '{pat}' in {f.name}"
                )
