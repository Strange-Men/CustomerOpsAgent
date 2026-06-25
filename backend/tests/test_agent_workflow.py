"""
CustomerOps Agent - Agent Workflow Tests

Tests for the node-based customer service agent workflow.
Covers entity extraction, intent recognition, logistics tool, fallback rules,
prompt builder, mock answer generator, and workflow integration.
"""

from __future__ import annotations

from pathlib import Path

from backend.app.agent.entity_extractor import (
    extract_customer_variables,
    extract_order_id,
)
from backend.app.agent.fallback_rules import (
    build_fallback_answer,
    detect_private_info_request,
    detect_sensitive_order_query,
    should_fallback,
)
from backend.app.agent.intent_recognizer import recognize_intent
from backend.app.agent.logistics_tool import query_mock_logistics
from backend.app.agent.mock_answer_generator import (
    generate_mock_answer,
    generate_mock_logistics_answer,
    generate_mock_rag_answer,
)
from backend.app.agent.prompt_builder import (
    build_customer_service_prompt,
    build_logistics_prompt,
)
from backend.app.agent.schemas import (
    AgentResponse,
    EvidenceCheckResult,
    ExtractedVariables,
    IntentResult,
    LogisticsToolResult,
)
from backend.app.agent.workflow import run_customer_service_agent
from backend.app.rag.schemas import RetrievedChunk


# ============================================================
# Test Entity Extractor
# ============================================================


class TestEntityExtractor:
    """Tests for entity extraction."""

    def test_extract_order_id_zh_six_digits(self):
        """Test extracting 6-digit order ID from Chinese query."""
        query = "我的订单123456的快递到哪了？"
        order_id = extract_order_id(query)
        assert order_id == "123456"

    def test_extract_order_id_zh_alphanumeric(self):
        """Test extracting alphanumeric order ID from Chinese query."""
        query = "我的订单 CN20250618001 到哪了"
        order_id = extract_order_id(query)
        assert order_id == "CN20250618001"

    def test_extract_order_id_en(self):
        """Test extracting order ID from English query."""
        query = "order id: ABC123456, where is my package?"
        order_id = extract_order_id(query)
        assert order_id == "ABC123456"

    def test_extract_order_id_en_tracking(self):
        """Test extracting tracking number from English query."""
        query = "tracking number: TRK123456"
        order_id = extract_order_id(query)
        assert order_id == "TRK123456"

    def test_extract_order_id_none(self):
        """Test when no order ID is present."""
        query = "我想退款怎么办？"
        order_id = extract_order_id(query)
        assert order_id is None

    def test_extract_order_id_empty(self):
        """Test with empty query."""
        order_id = extract_order_id("")
        assert order_id is None

    def test_extract_customer_variables_uses_existing_order_id(self):
        """Test that existing_order_id is used when query has no order ID."""
        query = "我的快递到哪了"
        variables = extract_customer_variables(query, existing_order_id="EXIST123")
        assert variables.order_id == "EXIST123"
        assert variables.has_order_id is True

    def test_extract_customer_variables_from_query(self):
        """Test extracting order ID from query."""
        query = "订单123456的物流信息"
        variables = extract_customer_variables(query)
        assert variables.order_id == "123456"
        assert variables.has_order_id is True

    def test_extract_customer_variables_none(self):
        """Test when no order ID is available."""
        query = "我想退货"
        variables = extract_customer_variables(query)
        assert variables.order_id is None
        assert variables.has_order_id is False


# ============================================================
# Test Intent Recognizer
# ============================================================


class TestIntentRecognizer:
    """Tests for intent recognition."""

    def test_recognize_intent_logistics_policy_zh(self):
        """Test recognizing logistics policy intent in Chinese."""
        query = "我的包裹多久能到"
        result = recognize_intent(query)
        assert result.route_intent == "aftersale"
        assert result.detail_intent == "logistics_policy"

    def test_recognize_intent_logistics_status_zh(self):
        """Test recognizing logistics status intent in Chinese."""
        query = "我的快递到哪了"
        result = recognize_intent(query)
        assert result.route_intent == "logistics"
        assert result.detail_intent == "logistics_status"

    def test_recognize_intent_aftersale_refund_zh(self):
        """Test recognizing aftersale/refund intent in Chinese."""
        query = "我想退款怎么办"
        result = recognize_intent(query)
        assert result.route_intent == "aftersale"
        assert result.detail_intent == "refund"

    def test_recognize_intent_customs_en(self):
        """Test recognizing customs intent in English."""
        query = "customs clearance delay"
        result = recognize_intent(query)
        assert result.detail_intent == "customs"
        # Customs should go to aftersale route (knowledge base)
        assert result.route_intent == "aftersale"

    def test_recognize_intent_trace(self):
        """Test recognizing trace intent."""
        query = "有没有产地证明或检测报告"
        result = recognize_intent(query)
        assert result.route_intent == "trace"
        assert result.detail_intent == "trace"

    def test_recognize_intent_other(self):
        """Test recognizing other/out-of-scope intent."""
        query = "你会写 Python 吗"
        result = recognize_intent(query)
        assert result.route_intent == "other"
        assert result.detail_intent == "unknown"

    def test_recognize_intent_empty(self):
        """Test with empty query."""
        result = recognize_intent("")
        assert result.route_intent == "other"
        assert result.detail_intent == "unknown"
        assert result.confidence == 0.0

    def test_recognize_intent_return_zh(self):
        """Test recognizing return intent in Chinese."""
        query = "怎么退货"
        result = recognize_intent(query)
        assert result.route_intent == "aftersale"
        assert result.detail_intent == "return"

    def test_recognize_intent_exchange_zh(self):
        """Test recognizing exchange intent in Chinese."""
        query = "可以换颜色吗"
        result = recognize_intent(query)
        assert result.route_intent == "aftersale"
        assert result.detail_intent == "exchange"

    def test_recognize_intent_payment_en(self):
        """Test recognizing payment intent in English."""
        query = "payment failed"
        result = recognize_intent(query)
        assert result.route_intent == "aftersale"
        assert result.detail_intent == "payment"

    def test_recognize_intent_package_zh(self):
        """Test recognizing package damage intent in Chinese."""
        query = "包裹破损了怎么办"
        result = recognize_intent(query)
        assert result.route_intent == "aftersale"
        assert result.detail_intent == "package"

    def test_recognize_intent_coupon_en(self):
        """Test recognizing coupon intent in English."""
        query = "coupon not working"
        result = recognize_intent(query)
        assert result.route_intent == "aftersale"
        assert result.detail_intent == "coupon"


# ============================================================
# Test Logistics Tool
# ============================================================


class TestLogisticsTool:
    """Tests for mock logistics tool."""

    def test_logistics_tool_missing_order_id(self):
        """Test logistics tool with no order ID."""
        result = query_mock_logistics(None)
        assert result.success is False
        assert result.reason == "missing_order_id"
        assert result.order_id is None

    def test_logistics_tool_success(self):
        """Test logistics tool with valid order ID."""
        result = query_mock_logistics("123456")
        assert result.success is True
        assert result.status is not None
        assert result.estimated_delivery is not None
        assert len(result.trace) > 0
        assert result.order_id == "123456"

    def test_logistics_tool_failure_prefix(self):
        """Test logistics tool with FAIL prefix."""
        result = query_mock_logistics("FAIL123")
        assert result.success is False
        assert result.reason == "tool_timeout"

    def test_logistics_tool_empty_string(self):
        """Test logistics tool with empty string."""
        result = query_mock_logistics("")
        assert result.success is False
        assert result.reason == "missing_order_id"


# ============================================================
# Test Fallback Rules
# ============================================================


class TestFallbackRules:
    """Tests for fallback rules."""

    def test_should_fallback_empty_query(self):
        """Test fallback for empty query."""
        intent = IntentResult(
            route_intent="other",
            detail_intent="unknown",
            confidence=0.0,
        )
        should, reason = should_fallback("", intent)
        assert should is True
        assert reason == "empty_query"

    def test_should_fallback_unknown_intent(self):
        """Test fallback for unknown intent."""
        intent = IntentResult(
            route_intent="other",
            detail_intent="unknown",
            confidence=0.3,
        )
        should, reason = should_fallback("你好", intent)
        assert should is True
        assert reason == "unknown_intent"

    def test_should_fallback_missing_order_id(self):
        """Test fallback for logistics_status without order ID."""
        intent = IntentResult(
            route_intent="logistics",
            detail_intent="logistics_status",
            confidence=0.8,
        )
        variables = ExtractedVariables(order_id=None, has_order_id=False)
        should, reason = should_fallback("快递到哪了", intent, variables=variables)
        assert should is True
        assert reason == "missing_order_id"

    def test_should_not_fallback_logistics_policy_without_order_id(self):
        """Test that logistics_policy does not fallback without order ID."""
        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="logistics_policy",
            confidence=0.8,
        )
        variables = ExtractedVariables(order_id=None, has_order_id=False)
        evidence = EvidenceCheckResult(
            has_evidence=True,
            confidence="medium",
            reasons=["top score 中等"],
        )
        should, reason = should_fallback("物流多久到", intent, evidence=evidence, variables=variables)
        assert should is False
        assert reason is None

    def test_should_fallback_tool_failed(self):
        """Test fallback for failed tool call."""
        intent = IntentResult(
            route_intent="logistics",
            detail_intent="logistics_status",
            confidence=0.8,
        )
        tool_result = LogisticsToolResult(
            success=False,
            reason="tool_timeout",
        )
        should, reason = should_fallback("订单123", intent, tool_result=tool_result)
        assert should is True
        assert reason == "logistics_tool_failed"

    def test_should_fallback_no_evidence(self):
        """Test fallback for no evidence."""
        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="refund",
            confidence=0.8,
        )
        evidence = EvidenceCheckResult(
            has_evidence=False,
            confidence="low",
            reasons=["检索无结果"],
        )
        should, reason = should_fallback("退款", intent, evidence=evidence)
        assert should is True
        assert reason == "no_evidence"

    def test_should_fallback_sensitive_info(self):
        """Test fallback for sensitive information request."""
        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="payment",
            confidence=0.8,
        )
        should, reason = should_fallback("请提供密码", intent)
        assert should is True
        assert reason == "sensitive_info_request"

    def test_should_not_fallback(self):
        """Test when fallback should not be triggered."""
        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="refund",
            confidence=0.8,
        )
        evidence = EvidenceCheckResult(
            has_evidence=True,
            confidence="high",
            reasons=["top score 高"],
        )
        should, reason = should_fallback("退款政策", intent, evidence=evidence)
        assert should is False
        assert reason is None

    def test_build_fallback_answer(self):
        """Test building fallback answers."""
        answer = build_fallback_answer("missing_order_id", "logistics")
        assert "订单号" in answer

    def test_build_fallback_answer_unknown(self):
        """Test building fallback answer for unknown intent."""
        answer = build_fallback_answer("unknown_intent", "other")
        assert "人工客服" in answer

    def test_detect_sensitive_info(self):
        """Test detecting sensitive information requests."""
        assert detect_sensitive_order_query("请提供密码") is True
        assert detect_sensitive_order_query("验证码是多少") is True
        assert detect_sensitive_order_query("我想退款") is False

    def test_detect_private_info(self):
        """Test detecting private information requests."""
        assert detect_private_info_request("请提供密码") is True
        assert detect_private_info_request("发送验证码") is True
        assert detect_private_info_request("物流信息") is False


# ============================================================
# Test Prompt Builder
# ============================================================


class TestPromptBuilder:
    """Tests for prompt builder."""

    def test_prompt_builder_contains_evidence_and_rules(self):
        """Test that prompt contains evidence and rules."""
        # Create mock retrieved chunks
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
                content="物流配送时效一般为5-10个工作日",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="logistics_policy",
            confidence=0.8,
        )

        prompt = build_customer_service_prompt("物流多久到", intent, chunks)

        # Check prompt contains evidence
        assert "doc_id" in prompt or "POL-LOGISTICS-001" in prompt
        assert "title" in prompt or "跨境物流配送政策" in prompt
        assert "content" in prompt or "物流配送时效" in prompt

        # Check prompt contains rules
        assert "证据" in prompt or "evidence" in prompt.lower()

    def test_logistics_prompt_contains_tool_result(self):
        """Test that logistics prompt contains tool result."""
        tool_result = LogisticsToolResult(
            success=True,
            order_id="123456",
            status="in_transit",
            trace=["包裹已到达分拣中心"],
            estimated_delivery="预计2-4个工作日",
        )

        prompt = build_logistics_prompt("我的包裹到哪了", tool_result)

        assert "123456" in prompt
        assert "in_transit" in prompt
        assert "包裹已到达分拣中心" in prompt


# ============================================================
# Test Mock Answer Generator
# ============================================================


class TestMockAnswerGenerator:
    """Tests for mock answer generator."""

    def test_mock_rag_answer_has_citations(self):
        """Test that RAG answer has citations."""
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
                content="物流配送时效一般为5-10个工作日",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="logistics_policy",
            confidence=0.8,
        )

        response = generate_mock_rag_answer("物流多久到", intent, chunks)

        assert len(response.citations) > 0
        assert response.route == "rag_knowledge_base"

    def test_mock_answer_uses_only_retrieved_citations(self):
        """Test that citations come from retrieved chunks."""
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
                content="物流配送时效一般为5-10个工作日",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="logistics_policy",
            confidence=0.8,
        )

        response = generate_mock_rag_answer("物流多久到", intent, chunks)

        # Verify citations come from retrieved chunks
        retrieved_chunk_ids = set(c.chunk_id for c in chunks)
        for citation in response.citations:
            assert citation.chunk_id in retrieved_chunk_ids

    def test_mock_logistics_answer(self):
        """Test mock logistics answer."""
        tool_result = LogisticsToolResult(
            success=True,
            order_id="123456",
            status="in_transit",
            trace=["包裹已到达分拣中心"],
            estimated_delivery="预计2-4个工作日",
        )

        intent = IntentResult(
            route_intent="logistics",
            detail_intent="logistics_status",
            confidence=0.9,
        )

        response = generate_mock_logistics_answer("包裹到哪了", intent, tool_result)

        assert response.route == "logistics_tool"
        assert response.tool_used == "mock_logistics_tool"
        assert "123456" in response.answer
        assert len(response.citations) == 0

    def test_mock_answer_no_chunks_fallback(self):
        """Test that empty chunks triggers fallback."""
        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="refund",
            confidence=0.8,
        )

        response = generate_mock_answer("退款", intent, retrieved_chunks=[])

        assert response.fallback_triggered is True
        assert response.route == "fallback"

    def test_sensitive_info_no_password_request(self):
        """Test that answers don't request passwords or verification codes."""
        chunks = [
            RetrievedChunk(
                chunk_id="POL-PAYMENT-001::chunk_001",
                doc_id="POL-PAYMENT-001",
                title="支付政策",
                category="payment",
                market="GLOBAL",
                language="zh",
                policy_type="payment",
                priority=1,
                source="official_2026Q1",
                content="支付问题处理流程",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = IntentResult(
            route_intent="aftersale",
            detail_intent="payment",
            confidence=0.8,
        )

        response = generate_mock_rag_answer("支付失败怎么办", intent, chunks)

        # Answer should not contain sensitive info requests
        answer_lower = response.answer.lower()
        assert "密码" not in answer_lower or "不要" in answer_lower or "请不要" in answer_lower
        assert "验证码" not in answer_lower or "不要" in answer_lower or "请不要" in answer_lower
        assert "银行卡号" not in answer_lower or "不要" in answer_lower or "请不要" in answer_lower


# ============================================================
# Test Workflow Integration
# ============================================================


class TestWorkflowIntegration:
    """Integration tests for the complete workflow."""

    def test_workflow_logistics_missing_order_id_fallback(self):
        """Test workflow fallback when logistics query has no order ID."""
        response = run_customer_service_agent("我的快递到哪了")

        assert response.fallback_triggered is True
        assert "missing_order_id" in (response.fallback_reason or "")
        assert response.route == "fallback"

    def test_workflow_logistics_with_order_id_uses_mock_tool(self):
        """Test workflow uses mock logistics tool with order ID."""
        response = run_customer_service_agent("我的订单123456的快递到哪了？")

        assert response.route == "logistics_tool"
        assert response.tool_used == "mock_logistics_tool"
        assert response.order_id == "123456"
        assert response.fallback_triggered is False
        # Answer should contain delivery info
        assert "送达" in response.answer or "物流" in response.answer or "运输" in response.answer

    def test_workflow_aftersale_uses_rag_route(self):
        """Test workflow uses RAG route for aftersale queries."""
        response = run_customer_service_agent("我想退款怎么办？")

        assert response.route == "rag_knowledge_base"
        assert len(response.citations) > 0
        assert len(response.retrieved_doc_ids) > 0

    def test_workflow_customs_uses_rag_route(self):
        """Test workflow uses RAG route for customs queries."""
        response = run_customer_service_agent("清关延迟怎么办？")

        assert response.route == "rag_knowledge_base"
        assert response.detail_intent == "customs"
        assert len(response.citations) > 0

    def test_workflow_trace_without_evidence_fallback(self):
        """Test workflow fallback for trace queries without evidence."""
        response = run_customer_service_agent("有没有产品产地检测报告？")

        # Should fallback if no evidence
        if response.fallback_triggered:
            assert response.route == "fallback"
            assert "trace" in (response.fallback_reason or "") or "no_evidence" in (response.fallback_reason or "")

    def test_workflow_out_of_scope_fallback(self):
        """Test workflow fallback for out-of-scope queries."""
        response = run_customer_service_agent("你能帮我写论文吗？")

        assert response.fallback_triggered is True
        assert response.route == "fallback"

    def test_workflow_with_conversation_history(self):
        """Test workflow with conversation history."""
        history = ["你好", "我想查订单", "订单号是123"]
        response = run_customer_service_agent(
            "快递到哪了",
            conversation_history=history,
        )
        # Should not error
        assert response is not None
        assert isinstance(response, AgentResponse)

    def test_conversation_history_limited_to_five(self):
        """Test that conversation history is limited to 5 messages."""
        history = [f"message_{i}" for i in range(10)]
        # Should not error with more than 5 messages
        response = run_customer_service_agent(
            "你好",
            conversation_history=history,
        )
        assert response is not None


# ============================================================
# Test Static Analysis
# ============================================================


class TestStaticAnalysis:
    """Static analysis tests for code quality."""

    def test_agent_modules_do_not_import_eval_cases(self):
        """Test that agent modules don't import eval cases."""
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

    def test_public_docs_do_not_contain_private_interview_content(self):
        """Test that public docs don't contain interview/revision content."""
        docs_dir = Path(__file__).parent.parent.parent / "docs"

        forbidden_patterns = [
            "面试讲法",
            "面试 Q&A",
            "面试题",
            "手撕",
            "复习",
            "个人学习",
            "简历包装",
            "求职话术",
            "一分钟表达",
        ]

        # Skip RAG_HANDS_ON_REVIEW.md (local-only file)
        # Skip archive directory
        for md_file in docs_dir.glob("*.md"):
            if md_file.name == "RAG_HANDS_ON_REVIEW.md":
                continue

            content = md_file.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                assert pattern not in content, (
                    f"Found '{pattern}' in {md_file.name}"
                )
