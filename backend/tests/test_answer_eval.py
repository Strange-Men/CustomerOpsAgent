"""
CustomerOps Agent - Answer Quality Evaluation Tests

Tests for the answer quality evaluation harness.
Covers keyword coverage, citation hit rate, relevance, groundedness,
completeness, citation evaluation, per-case results, aggregate metrics,
and anti-cheating static checks.
"""

from __future__ import annotations

from pathlib import Path

from backend.app.agent.schemas import AgentResponse, Citation
from backend.app.eval.answer_eval import (
    AnswerCaseResult,
    AnswerEvalReport,
    citation_hit_rate,
    evaluate_agent_answers,
    evaluate_answer_case,
    evaluate_citation,
    evaluate_completeness,
    evaluate_groundedness,
    evaluate_relevance,
    keyword_coverage,
    normalize_text,
    run_default_answer_evaluation,
)
from backend.app.rag.schemas import EvalCase


# ============================================================
# Helpers
# ============================================================


def _make_case(**kwargs) -> EvalCase:
    """Create an EvalCase with defaults for testing."""
    defaults = {
        "case_id": "test_001",
        "question": "How do I return a product?",
        "category": "return",
        "market": "US",
        "language": "en",
        "difficulty": "medium",
        "expected_doc_ids": ["doc_return_001"],
        "expected_keywords": ["return", "30 days", "policy"],
    }
    defaults.update(kwargs)
    return EvalCase(**defaults)


def _make_response(**kwargs) -> AgentResponse:
    """Create an AgentResponse with defaults for testing."""
    defaults = {
        "answer": "You can return within 30 days per our return policy.",
        "route": "rag_knowledge_base",
        "intent": "aftersale",
        "detail_intent": "return",
        "citations": [
            Citation(
                doc_id="doc_return_001",
                chunk_id="doc_return_001::chunk_000",
                title="Return Policy",
                source="customer_service_seed.jsonl",
                category="return",
                market="GLOBAL",
                language="en",
            ),
        ],
        "fallback_triggered": False,
        "fallback_reason": None,
        "confidence": "high",
        "retrieved_doc_ids": ["doc_return_001"],
        "order_id": None,
        "tool_used": None,
    }
    defaults.update(kwargs)
    return AgentResponse(**defaults)


# ============================================================
# Test normalize_text
# ============================================================


class TestNormalizeText:
    def test_lowercase_and_whitespace(self):
        assert normalize_text("  Hello   World  ") == "hello world"

    def test_cjk_preserved(self):
        assert normalize_text("退款 政策") == "退款 政策"

    def test_empty_string(self):
        assert normalize_text("") == ""


# ============================================================
# Test keyword_coverage
# ============================================================


class TestKeywordCoverage:
    def test_partial_coverage(self):
        answer = "You can return within 30 days."
        keywords = ["return", "30 days", "policy"]
        cov = keyword_coverage(answer, keywords)
        # "return" and "30 days" match, "policy" does not
        assert cov == 2 / 3

    def test_full_coverage(self):
        answer = "Return within 30 days per policy."
        keywords = ["return", "30 days", "policy"]
        cov = keyword_coverage(answer, keywords)
        assert cov == 1.0

    def test_empty_keywords(self):
        assert keyword_coverage("some answer", []) == 0.0

    def test_case_insensitive(self):
        answer = "RETURN the product within 30 DAYS."
        keywords = ["return", "30 days"]
        cov = keyword_coverage(answer, keywords)
        assert cov == 1.0

    def test_cjk_keywords(self):
        answer = "您可以在30天内退货，根据我们的退货政策。"
        keywords = ["退货", "30天", "政策"]
        cov = keyword_coverage(answer, keywords)
        assert cov == 1.0

    def test_no_match(self):
        answer = "Hello world."
        keywords = ["return", "refund"]
        cov = keyword_coverage(answer, keywords)
        assert cov == 0.0


# ============================================================
# Test citation_hit_rate
# ============================================================


class TestCitationHitRate:
    def test_hit(self):
        assert citation_hit_rate(["doc_001", "doc_002"], ["doc_001", "doc_003"]) == 1.0

    def test_no_hit(self):
        assert citation_hit_rate(["doc_002"], ["doc_001", "doc_003"]) == 0.0

    def test_empty_citations(self):
        assert citation_hit_rate([], ["doc_001"]) == 0.0

    def test_empty_expected(self):
        assert citation_hit_rate(["doc_001"], []) == 0.0


# ============================================================
# Test evaluate_relevance
# ============================================================


class TestEvaluateRelevance:
    def test_category_match_no_fallback(self):
        case = _make_case(category="return")
        response = _make_response(detail_intent="return", fallback_triggered=False)
        rel = evaluate_relevance(case, response)
        # category match (0.5) + non-empty answer (0.3) + RAG route (0.2) = 1.0
        assert rel == 1.0

    def test_category_mismatch_no_fallback(self):
        case = _make_case(category="refund")
        response = _make_response(detail_intent="return", fallback_triggered=False)
        rel = evaluate_relevance(case, response)
        # no category match (0.0) + non-empty answer (0.3) + RAG route (0.2) = 0.5
        assert rel == 0.5

    def test_fallback_penalizes_relevance(self):
        case = _make_case(category="return")
        response = _make_response(
            detail_intent="return",
            fallback_triggered=True,
            fallback_reason="no_evidence",
            route="fallback",
        )
        rel = evaluate_relevance(case, response)
        # category match (0.5) + fallback answer (0.1) + fallback route (0.0) = 0.6
        assert rel == 0.6

    def test_logistics_tool_route(self):
        case = _make_case(category="logistics")
        response = _make_response(
            route="logistics_tool",
            intent="logistics",
            detail_intent="logistics",
            tool_used="mock_logistics_tool",
        )
        rel = evaluate_relevance(case, response)
        # category match (0.5) + non-empty (0.3) + logistics route (0.2) = 1.0
        assert rel == 1.0


# ============================================================
# Test evaluate_groundedness
# ============================================================


class TestEvaluateGroundedness:
    def test_rag_requires_citation(self):
        response = _make_response(
            route="rag_knowledge_base",
            citations=[],
            retrieved_doc_ids=["doc_001"],
        )
        case = _make_case()
        gnd = evaluate_groundedness(case, response)
        assert gnd == 0.0

    def test_rag_with_citation(self):
        response = _make_response(route="rag_knowledge_base")
        case = _make_case()
        gnd = evaluate_groundedness(case, response)
        # base 0.8 + retrieved match 0.1 = 0.9
        assert gnd == 0.9

    def test_tool_route_grounded(self):
        response = _make_response(
            route="logistics_tool",
            tool_used="mock_logistics_tool",
            citations=[],
        )
        case = _make_case()
        gnd = evaluate_groundedness(case, response)
        assert gnd == 0.8

    def test_fallback_no_fabrication(self):
        response = _make_response(
            route="fallback",
            fallback_triggered=True,
            answer="Please contact customer service.",
            citations=[],
        )
        case = _make_case()
        gnd = evaluate_groundedness(case, response)
        assert gnd == 0.4

    def test_fabrication_penalized(self):
        response = _make_response(
            route="rag_knowledge_base",
            answer="我们保证赔偿您的损失，100%送达。",
        )
        case = _make_case()
        gnd = evaluate_groundedness(case, response)
        # 0.8 + 0.1 - 0.5 = 0.4
        assert gnd == 0.4


# ============================================================
# Test evaluate_completeness
# ============================================================


class TestEvaluateCompleteness:
    def test_high_coverage(self):
        case = _make_case(expected_keywords=["return", "30 days", "policy"])
        response = _make_response(answer="Return within 30 days per policy.")
        comp = evaluate_completeness(case, response)
        assert comp == 1.0

    def test_low_coverage(self):
        case = _make_case(expected_keywords=["return", "30 days", "policy"])
        response = _make_response(answer="Hello.")
        comp = evaluate_completeness(case, response)
        assert comp == 0.0

    def test_fallback_penalizes_completeness(self):
        case = _make_case(
            expected_keywords=["return", "30 days", "policy"],
            category="return",
        )
        response = _make_response(
            answer="Return within 30 days per policy.",
            fallback_triggered=True,
            route="fallback",
        )
        comp = evaluate_completeness(case, response)
        # coverage=1.0 * 0.3 (fallback penalty) = 0.3
        assert comp == 0.3

    def test_fallback_other_category_not_penalized(self):
        case = _make_case(
            expected_keywords=["return"],
            category="other",
        )
        response = _make_response(
            answer="Return the product.",
            fallback_triggered=True,
            route="fallback",
        )
        comp = evaluate_completeness(case, response)
        # coverage=1.0, category=other so no penalty
        assert comp == 1.0


# ============================================================
# Test evaluate_citation
# ============================================================


class TestEvaluateCitation:
    def test_rag_hit(self):
        case = _make_case(expected_doc_ids=["doc_001"])
        response = _make_response(
            route="rag_knowledge_base",
            citations=[
                Citation(
                    doc_id="doc_001",
                    chunk_id="doc_001::chunk_000",
                    title="T",
                    source="S",
                    category="return",
                    market="GLOBAL",
                    language="en",
                ),
            ],
        )
        assert evaluate_citation(case, response) == 1.0

    def test_rag_no_hit(self):
        case = _make_case(expected_doc_ids=["doc_001"])
        response = _make_response(
            route="rag_knowledge_base",
            citations=[
                Citation(
                    doc_id="doc_999",
                    chunk_id="doc_999::chunk_000",
                    title="T",
                    source="S",
                    category="return",
                    market="GLOBAL",
                    language="en",
                ),
            ],
        )
        assert evaluate_citation(case, response) == 0.0

    def test_tool_route_half_score(self):
        case = _make_case()
        response = _make_response(
            route="logistics_tool",
            tool_used="mock_logistics_tool",
            citations=[],
        )
        assert evaluate_citation(case, response) == 0.5

    def test_fallback_zero(self):
        case = _make_case()
        response = _make_response(route="fallback", citations=[])
        assert evaluate_citation(case, response) == 0.0


# ============================================================
# Test evaluate_answer_case
# ============================================================


class TestEvaluateAnswerCase:
    def test_required_fields(self):
        case = _make_case()
        response = _make_response()
        result = evaluate_answer_case(case, response)

        assert isinstance(result, AnswerCaseResult)
        assert result.case_id == "test_001"
        assert isinstance(result.relevance, float)
        assert isinstance(result.groundedness, float)
        assert isinstance(result.completeness, float)
        assert isinstance(result.citation_hit, float)
        assert isinstance(result.keyword_coverage, float)
        assert isinstance(result.passed, bool)
        assert isinstance(result.failure_reasons, list)

    def test_passing_case(self):
        case = _make_case(
            expected_doc_ids=["doc_return_001"],
            expected_keywords=["return", "30 days"],
        )
        response = _make_response(
            detail_intent="return",
            answer="You can return within 30 days per our return policy.",
        )
        result = evaluate_answer_case(case, response)
        assert result.passed is True
        assert len(result.failure_reasons) == 0

    def test_failing_case_low_groundedness(self):
        case = _make_case()
        response = _make_response(
            route="rag_knowledge_base",
            citations=[],
            retrieved_doc_ids=["doc_001"],
            answer="Return it.",
        )
        result = evaluate_answer_case(case, response)
        assert result.passed is False
        assert any("groundedness" in r for r in result.failure_reasons)


# ============================================================
# Test evaluate_agent_answers (aggregate)
# ============================================================


class TestEvaluateAgentAnswers:
    def test_summary_metrics(self, monkeypatch):
        """Test aggregate metrics with a mocked workflow."""
        cases = [
            _make_case(case_id="c1", category="return", expected_keywords=["return"]),
            _make_case(case_id="c2", category="return", expected_keywords=["return"]),
        ]

        responses = [
            _make_response(detail_intent="return"),
            _make_response(
                route="fallback",
                fallback_triggered=True,
                fallback_reason="no_evidence",
                answer="Please contact support.",
                citations=[],
                confidence="low",
            ),
        ]

        call_count = 0

        def mock_workflow(query, order_id=None, conversation_history=None, top_k=5):
            nonlocal call_count
            resp = responses[call_count]
            call_count += 1
            return resp

        monkeypatch.setattr(
            "backend.app.eval.answer_eval.run_customer_service_agent",
            mock_workflow,
        )

        report = evaluate_agent_answers(cases)

        assert isinstance(report, AnswerEvalReport)
        assert report.total_cases == 2
        assert 0.0 <= report.avg_relevance <= 1.0
        assert 0.0 <= report.avg_groundedness <= 1.0
        assert 0.0 <= report.avg_completeness <= 1.0
        assert isinstance(report.failed_cases, list)


# ============================================================
# Test run_default_answer_evaluation (full dataset)
# ============================================================


class TestRunDefaultAnswerEvaluation:
    def test_full_dataset(self):
        """Run default answer evaluation on full dataset."""
        report = run_default_answer_evaluation()

        assert report.total_cases >= 120
        assert 0.0 <= report.avg_relevance <= 1.0
        assert 0.0 <= report.avg_groundedness <= 1.0
        assert 0.0 <= report.avg_completeness <= 1.0
        assert 0.0 <= report.citation_hit_rate <= 1.0
        assert 0.0 <= report.answer_pass_rate <= 1.0
        assert 0.0 <= report.fallback_rate <= 1.0
        assert isinstance(report.failed_cases, list)
        assert isinstance(report.per_case_results, list)
        assert len(report.per_case_results) == report.total_cases


# ============================================================
# Anti-cheating: eval fields must not leak into agent module
# ============================================================


class TestAntiCheating:
    def test_answer_eval_uses_expected_keywords_only_in_eval_layer(self):
        """expected_keywords / expected_doc_ids must not appear in agent module."""
        agent_dir = Path(__file__).resolve().parent.parent / "app" / "agent"
        forbidden = [
            "expected_keywords",
            "expected_doc_ids",
            "eval_cases_full",
            "eval_cases_seed",
            "case_id",
        ]

        for py_file in agent_dir.glob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            for term in forbidden:
                assert term not in content, (
                    f"Found '{term}' in {py_file.name} — "
                    f"eval ground-truth must not leak into agent module"
                )

    def test_answer_eval_does_not_modify_agent_workflow(self):
        """answer_eval.py should only import agent workflow, not define it."""
        eval_path = (
            Path(__file__).resolve().parent.parent / "app" / "eval" / "answer_eval.py"
        )
        content = eval_path.read_text(encoding="utf-8")

        # Should import run_customer_service_agent
        assert "run_customer_service_agent" in content

        # Should not define its own workflow logic
        assert "def run_customer_service_agent" not in content

        # Should not import from eval ground-truth into agent
        assert "from backend.app.agent" in content


# ============================================================
# Public docs safety check
# ============================================================


class TestPublicDocsSafety:
    def test_public_docs_do_not_contain_private_interview_content(self):
        """Scan public docs for forbidden interview/review content."""
        docs_dir = Path(__file__).resolve().parent.parent.parent / "docs"
        forbidden_terms = [
            "面试讲法",
            "面试 Q&A",
            "面试题",
            "手撕",
            "复习",
            "个人学习",
            "简历包装",
            "求职话术",
            "一分钟表达",
            "面试官",
        ]

        # Exclude RAG_HANDS_ON_REVIEW.md (local-only file)
        for md_file in docs_dir.rglob("*.md"):
            if md_file.name == "RAG_HANDS_ON_REVIEW.md":
                continue

            content = md_file.read_text(encoding="utf-8")
            for term in forbidden_terms:
                assert term not in content, (
                    f"Found forbidden term '{term}' in {md_file.relative_to(docs_dir)}"
                )
