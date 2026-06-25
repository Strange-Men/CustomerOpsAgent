"""
CustomerOps Agent - Answer Workflow Optimization Tests (M9)

Tests for M9 optimizations:
- Intent recognition: logistics_status vs logistics_policy
- Route decision: policy queries use RAG, not logistics tool
- Fallback rules: missing_order_id only for logistics_status
- Mock answer generator: improved evidence coverage
- Citation selection: citations from retrieved chunks
- No eval leakage in agent modules
"""

from __future__ import annotations

from pathlib import Path

from backend.app.agent.intent_recognizer import recognize_intent
from backend.app.agent.mock_answer_generator import generate_mock_rag_answer
from backend.app.agent.schemas import IntentResult
from backend.app.agent.workflow import run_customer_service_agent
from backend.app.rag.schemas import RetrievedChunk


# ============================================================
# Test Intent Recognition: logistics_status vs logistics_policy
# ============================================================


class TestIntentLogisticsSplit:
    """Test that logistics queries are properly split into status and policy."""

    def test_logistics_policy_without_order_id_uses_rag(self):
        """Logistics policy query should route to RAG, not require order_id."""
        query = "美国标准物流多久到？"
        result = recognize_intent(query)
        assert result.detail_intent == "logistics_policy"
        assert result.route_intent == "aftersale"

    def test_shipping_time_en_uses_rag_not_tool(self):
        """English shipping time query should use RAG, not logistics tool."""
        query = "How long does shipping take to the US?"
        result = recognize_intent(query)
        assert result.detail_intent == "logistics_policy"
        assert result.route_intent == "aftersale"

    def test_logistics_status_without_order_id_fallback(self):
        """Logistics status query without order_id should fallback."""
        query = "我的快递到哪了？"
        result = recognize_intent(query)
        assert result.detail_intent == "logistics_status"
        assert result.route_intent == "logistics"

    def test_logistics_status_with_order_id_uses_tool(self):
        """Logistics status query with order_id should use logistics tool."""
        query = "我的订单123456到哪了？"
        result = recognize_intent(query)
        assert result.detail_intent == "logistics_status"
        assert result.route_intent == "logistics"

    def test_delivery_time_policy_uses_rag(self):
        """Delivery time policy query should use RAG."""
        query = "配送时效多久？"
        result = recognize_intent(query)
        assert result.detail_intent == "logistics_policy"
        assert result.route_intent == "aftersale"

    def test_shipping_cost_uses_rag(self):
        """Shipping cost query should use RAG."""
        query = "运费多少？"
        result = recognize_intent(query)
        assert result.detail_intent == "logistics_policy"
        assert result.route_intent == "aftersale"

    def test_free_shipping_uses_rag(self):
        """Free shipping query should use RAG."""
        query = "有没有包邮？"
        result = recognize_intent(query)
        assert result.detail_intent == "logistics_policy"
        assert result.route_intent == "aftersale"


# ============================================================
# Test Route Decision: policy queries don't require order_id
# ============================================================


class TestRouteDecision:
    """Test that route decision properly handles policy vs status queries."""

    def test_customs_query_uses_rag_without_order_id(self):
        """Customs query should use RAG without requiring order_id."""
        query = "清关延迟怎么办？"
        response = run_customer_service_agent(query)
        assert response.route == "rag_knowledge_base"
        assert response.fallback_triggered is False
        assert response.fallback_reason != "missing_order_id"

    def test_refund_policy_uses_rag_without_order_id(self):
        """Refund policy query should use RAG without requiring order_id."""
        query = "退款多久到账？"
        response = run_customer_service_agent(query)
        assert response.route == "rag_knowledge_base"
        assert response.fallback_triggered is False
        assert response.fallback_reason != "missing_order_id"

    def test_order_cancel_policy_uses_rag_without_order_id(self):
        """Order cancel policy query should use RAG without requiring order_id."""
        query = "订单能取消吗？"
        response = run_customer_service_agent(query)
        assert response.route == "rag_knowledge_base"
        assert response.fallback_triggered is False
        assert response.fallback_reason != "missing_order_id"

    def test_return_policy_uses_rag_without_order_id(self):
        """Return policy query should use RAG without requiring order_id."""
        query = "退货政策是什么？"
        response = run_customer_service_agent(query)
        assert response.route == "rag_knowledge_base"
        assert response.fallback_triggered is False

    def test_logistics_policy_uses_rag_not_tool(self):
        """Logistics policy query should use RAG, not logistics tool."""
        query = "美国标准物流多久到？"
        response = run_customer_service_agent(query)
        assert response.route == "rag_knowledge_base"
        assert response.fallback_triggered is False
        assert response.tool_used is None

    def test_logistics_status_with_order_id_uses_tool(self):
        """Logistics status with order_id should use logistics tool."""
        query = "我的订单123456到哪了？"
        response = run_customer_service_agent(query)
        assert response.route == "logistics_tool"
        assert response.tool_used == "mock_logistics_tool"
        assert response.order_id == "123456"

    def test_logistics_status_without_order_id_fallback(self):
        """Logistics status without order_id should fallback."""
        query = "我的快递到哪了？"
        response = run_customer_service_agent(query)
        assert response.fallback_triggered is True
        assert response.fallback_reason == "missing_order_id"


# ============================================================
# Test Mock Answer Generator: improved evidence coverage
# ============================================================


class TestMockAnswerCoverage:
    """Test that mock answer generator uses more evidence."""

    def test_mock_rag_answer_includes_more_than_one_evidence_sentence(self):
        """RAG answer should include content from multiple chunks."""
        chunks = [
            RetrievedChunk(
                chunk_id="POL-LOGISTICS-001::chunk_001",
                doc_id="POL-LOGISTICS-001",
                title="跨境物流配送政策",
                category="logistics",
                market="GLOBAL",
                language="zh",
                policy_type="shipping",
                priority=1,
                source="official_2026Q1",
                content="标准物流配送时效为5-10个工作日。快速物流配送时效为2-4个工作日。",
                chunk_index=0,
                score=5.0,
            ),
            RetrievedChunk(
                chunk_id="POL-LOGISTICS-001::chunk_002",
                doc_id="POL-LOGISTICS-001",
                title="跨境物流配送政策",
                category="logistics",
                market="GLOBAL",
                language="zh",
                policy_type="shipping",
                priority=1,
                source="official_2026Q1",
                content="美国标准物流配送时效为7-15个工作日。欧洲标准物流配送时效为10-20个工作日。",
                chunk_index=1,
                score=4.5,
            ),
        ]

        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="logistics_policy",
            confidence=0.8,
        )

        response = generate_mock_rag_answer("物流多久到", intent, chunks)

        # Answer should contain content from both chunks
        assert "5-10个工作日" in response.answer
        assert "7-15个工作日" in response.answer

    def test_rag_answer_keeps_citations(self):
        """RAG route citations should be non-empty and from retrieved chunks."""
        chunks = [
            RetrievedChunk(
                chunk_id="POL-REFUND-001::chunk_001",
                doc_id="POL-REFUND-001",
                title="退款政策",
                category="refund",
                market="GLOBAL",
                language="zh",
                policy_type="refund",
                priority=1,
                source="official_2026Q1",
                content="退款将在3-5个工作日内到账。",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="refund",
            confidence=0.8,
        )

        response = generate_mock_rag_answer("退款多久到账", intent, chunks)

        assert len(response.citations) > 0
        retrieved_chunk_ids = set(c.chunk_id for c in chunks)
        for citation in response.citations:
            assert citation.chunk_id in retrieved_chunk_ids

    def test_rag_answer_includes_citation_reference(self):
        """RAG answer should include citation references in text."""
        chunks = [
            RetrievedChunk(
                chunk_id="POL-REFUND-001::chunk_001",
                doc_id="POL-REFUND-001",
                title="退款政策",
                category="refund",
                market="GLOBAL",
                language="zh",
                policy_type="refund",
                priority=1,
                source="official_2026Q1",
                content="退款将在3-5个工作日内到账。",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="refund",
            confidence=0.8,
        )

        response = generate_mock_rag_answer("退款多久到账", intent, chunks)

        # Answer should reference the document
        assert "POL-REFUND-001" in response.answer


# ============================================================
# Test No Eval Leakage
# ============================================================


class TestNoEvalLeakage:
    """Test that agent modules don't leak eval data."""

    def test_no_eval_leakage_in_agent_modules(self):
        """Static scan: agent modules must not reference eval data."""
        agent_dir = Path(__file__).parent.parent / "app" / "agent"

        forbidden_patterns = [
            "eval_cases_seed",
            "eval_cases_full",
            "expected_doc_ids",
            "expected_keywords",
            "case_id",
        ]

        for py_file in agent_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            content = py_file.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                assert pattern not in content, (
                    f"Found '{pattern}' in {py_file.name}"
                )


# ============================================================
# Test Answer Eval Improvement
# ============================================================


class TestAnswerEvalImprovement:
    """Test that M9 optimizations improve answer quality metrics."""

    def test_answer_eval_improves_after_m9(self):
        """Run answer eval and verify metrics improved over M8 baseline."""
        from backend.app.eval.answer_eval import run_default_answer_evaluation

        report = run_default_answer_evaluation()

        # M8 baseline: answer_pass_rate=31.97%, fallback_rate=40.16%, avg_relevance=0.5967
        assert report.answer_pass_rate > 0.3197, (
            f"answer_pass_rate {report.answer_pass_rate:.4f} should be > 0.3197"
        )
        assert report.fallback_rate < 0.4016, (
            f"fallback_rate {report.fallback_rate:.4f} should be < 0.4016"
        )
        assert report.avg_relevance > 0.5967, (
            f"avg_relevance {report.avg_relevance:.4f} should be > 0.5967"
        )
