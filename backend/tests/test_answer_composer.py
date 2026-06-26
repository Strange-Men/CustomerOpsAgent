"""
CustomerOps Agent - Answer Sanitizer Tests

Tests for the sanitize_customer_answer function.
Ensures customer-facing answers do not leak internal doc_ids,
citation references, or system metadata.
"""

from __future__ import annotations

from backend.app.agent.answer_sanitizer import sanitize_customer_answer


class TestSanitizeCustomerAnswer:
    """Tests for sanitize_customer_answer."""

    def test_removes_trailing_citation_section(self):
        """Remove trailing '证据引用' paragraph."""
        raw = (
            "您好，支付失败可能是余额不足。建议您更换支付方式。\n\n"
            "证据引用：payment_global_failure_001"
        )
        result = sanitize_customer_answer(raw)
        assert "证据引用" not in result
        assert "payment_global_failure_001" not in result
        assert "建议您更换支付方式" in result

    def test_removes_parenthesized_doc_id_list(self):
        """Remove parenthesized doc_id lists like (payment_global_failure_001、refund_eu_policy_001)."""
        raw = "您好，支付失败可能是余额不足。建议您更换支付方式。（payment_global_failure_001、refund_eu_policy_001）"
        result = sanitize_customer_answer(raw)
        assert "payment_global_failure_001" not in result
        assert "refund_eu_policy_001" not in result
        assert "建议您更换支付方式" in result

    def test_removes_citation_refs_at_end(self):
        """Remove citation references at the end of the answer."""
        raw = "您好，建议您重新支付。\n\n引用：payment_global_failure_001"
        result = sanitize_customer_answer(raw)
        assert "引用" not in result
        assert "payment_global_failure_001" not in result
        assert "建议您重新支付" in result

    def test_removes_knowledge_base_tail(self):
        """Remove '以上信息根据当前知识库（xxx）。' tails."""
        raw = (
            "您好，关于退款问题，以下是相关信息：\n\n"
            "退款到账时间一般为 3-10 个工作日。\n\n"
            "以上信息根据当前知识库（payment_global_failure_001 (支付失败处理流程)）。"
        )
        result = sanitize_customer_answer(raw)
        assert "以上信息根据当前知识库" not in result
        assert "payment_global_failure_001" not in result
        assert "退款到账时间" in result

    def test_preserves_normal_business_content(self):
        """Preserve normal business content like amounts, dates, order numbers."""
        raw = "您好，您的订单 ORD-2024-0088 退款金额为 ¥299.00，预计 3-5 个工作日到账。"
        result = sanitize_customer_answer(raw)
        assert "ORD-2024-0088" in result
        assert "¥299.00" in result
        assert "3-5 个工作日" in result

    def test_preserves_customer_service_suggestions(self):
        """Preserve customer service suggestions."""
        raw = "建议您保留支付截图，联系人工客服处理。"
        result = sanitize_customer_answer(raw)
        assert "建议您保留支付截图" in result
        assert "联系人工客服" in result

    def test_handles_empty_string(self):
        """Handle empty string gracefully."""
        assert sanitize_customer_answer("") == ""

    def test_handles_none_like_empty(self):
        """Handle None-like empty input."""
        # The function accepts str, but let's test edge case
        assert sanitize_customer_answer("") == ""

    def test_removes_multiple_doc_id_patterns(self):
        """Remove multiple doc_id patterns in various positions."""
        raw = (
            "您好，关于支付问题。\n"
            "（payment_global_failure_001、refund_eu_policy_001）\n"
            "建议您检查支付方式。"
        )
        result = sanitize_customer_answer(raw)
        assert "payment_global_failure_001" not in result
        assert "refund_eu_policy_001" not in result
        assert "建议您检查支付方式" in result

    def test_removes_doc_id_in_middle_of_line(self):
        """Remove doc_id that appears inline in a line."""
        raw = "您好，建议您重新支付。 payment_global_failure_001"
        result = sanitize_customer_answer(raw)
        assert "payment_global_failure_001" not in result
        assert "建议您重新支付" in result

    def test_preserves_evidence_in_chinese(self):
        """Preserve normal Chinese text that mentions '证据' in context."""
        # This is tricky — we should NOT remove "证据" when it's part of normal text
        raw = "您好，建议您保留相关证据，如截图或聊天记录。"
        result = sanitize_customer_answer(raw)
        assert "保留相关证据" in result

    def test_removes_reference_citation_prefix(self):
        """Remove '引用证据：' prefix lines."""
        raw = "您好，退款处理中。\n\n引用证据：refund_eu_policy_001"
        result = sanitize_customer_answer(raw)
        assert "引用证据" not in result
        assert "refund_eu_policy_001" not in result
        assert "退款处理中" in result

    def test_removes_bracket_evidence(self):
        """Remove 【证据】 patterns."""
        raw = "您好，建议重新支付。\n\n【证据】payment_global_failure_001"
        result = sanitize_customer_answer(raw)
        assert "【证据】" not in result
        assert "payment_global_failure_001" not in result

    def test_clean_answer_passes_through(self):
        """A clean answer without any internal terms should pass through unchanged."""
        raw = (
            "您好，关于支付失败问题，常见原因包括：\n"
            "1）银行卡余额不足\n"
            "2）支付渠道暂时不可用\n"
            "3）网络连接中断\n\n"
            "建议您更换支付方式或稍后重试。如问题持续，请联系人工客服。"
        )
        result = sanitize_customer_answer(raw)
        assert result == raw

    def test_preserves_markdown_bold(self):
        """Markdown bold syntax should NOT be treated as internal leak."""
        raw = "您好，**退款处理时间**一般为 3-10 个工作日。"
        result = sanitize_customer_answer(raw)
        assert "**退款处理时间**" in result
        assert "3-10 个工作日" in result

    def test_preserves_markdown_bold_with_citation_removal(self):
        """Markdown bold should be preserved while citation tails are removed."""
        raw = (
            "您好，**退款处理时间**一般为 3-10 个工作日。\n\n"
            "证据引用：refund_eu_policy_001"
        )
        result = sanitize_customer_answer(raw)
        assert "**退款处理时间**" in result
        assert "3-10 个工作日" in result
        assert "证据引用" not in result
        assert "refund_eu_policy_001" not in result

    def test_preserves_multiple_markdown_bold(self):
        """Multiple markdown bold instances should all be preserved."""
        raw = "您好，**支付方式**包括信用卡和**支付宝**。"
        result = sanitize_customer_answer(raw)
        assert "**支付方式**" in result
        assert "**支付宝**" in result


class TestAnswerContentSafety:
    """Tests that verify answers don't contain forbidden internal terms."""

    FORBIDDEN_TERMS = [
        "证据引用",
        "引用证据",
        "根据证据",
        "doc_id",
        "retrieved_doc_ids",
        "answer_source",
        "llm_profile",
        "fallback_triggered",
        "payment_global_failure_001",
        "refund_eu_policy_001",
        "order_global_cancel_001",
        "return_us_policy_001",
        "address_us_modify_001",
    ]

    def test_mock_payment_answer_clean(self):
        """Mock answer for payment query should not contain forbidden terms."""
        from backend.app.agent.intent_recognizer import recognize_intent
        from backend.app.agent.mock_answer_generator import generate_mock_rag_answer
        from backend.app.rag.schemas import RetrievedChunk

        chunks = [
            RetrievedChunk(
                chunk_id="PAY-001::chunk_001",
                doc_id="PAY-001",
                title="支付失败处理流程",
                category="payment",
                market="GLOBAL",
                language="zh",
                policy_type="payment",
                priority=1,
                source="official_2026Q1",
                content="支付失败常见原因包括余额不足、银行卡限额、支付渠道异常等。",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = recognize_intent("支付失败怎么办")
        response = generate_mock_rag_answer("支付失败怎么办", intent, chunks)

        for term in self.FORBIDDEN_TERMS:
            assert term not in response.answer, (
                f"Mock answer contains forbidden term: {term}"
            )

    def test_mock_refund_answer_clean(self):
        """Mock answer for refund query should not contain forbidden terms."""
        from backend.app.agent.intent_recognizer import recognize_intent
        from backend.app.agent.mock_answer_generator import generate_mock_rag_answer
        from backend.app.rag.schemas import RetrievedChunk

        chunks = [
            RetrievedChunk(
                chunk_id="REF-001::chunk_001",
                doc_id="REF-001",
                title="退款政策",
                category="refund",
                market="GLOBAL",
                language="zh",
                policy_type="refund",
                priority=1,
                source="official_2026Q1",
                content="退款到账时间一般为 3-10 个工作日。",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = recognize_intent("退款多久到账")
        response = generate_mock_rag_answer("退款多久到账", intent, chunks)

        for term in self.FORBIDDEN_TERMS:
            assert term not in response.answer, (
                f"Mock answer contains forbidden term: {term}"
            )

    def test_mock_customs_answer_clean(self):
        """Mock answer for customs query should not contain forbidden terms."""
        from backend.app.agent.intent_recognizer import recognize_intent
        from backend.app.agent.mock_answer_generator import generate_mock_rag_answer
        from backend.app.rag.schemas import RetrievedChunk

        chunks = [
            RetrievedChunk(
                chunk_id="CUS-001::chunk_001",
                doc_id="CUS-001",
                title="清关流程指南",
                category="customs",
                market="GLOBAL",
                language="zh",
                policy_type="customs",
                priority=1,
                source="official_2026Q1",
                content="清关延迟通常由海关抽检、申报信息不完整导致。",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = recognize_intent("清关延迟怎么办")
        response = generate_mock_rag_answer("清关延迟怎么办", intent, chunks)

        for term in self.FORBIDDEN_TERMS:
            assert term not in response.answer, (
                f"Mock answer contains forbidden term: {term}"
            )

    def test_citations_still_present_in_structured_field(self):
        """Citations should still be in the structured response, just not in answer text."""
        from backend.app.agent.intent_recognizer import recognize_intent
        from backend.app.agent.mock_answer_generator import generate_mock_rag_answer
        from backend.app.rag.schemas import RetrievedChunk

        chunks = [
            RetrievedChunk(
                chunk_id="PAY-001::chunk_001",
                doc_id="PAY-001",
                title="支付失败处理流程",
                category="payment",
                market="GLOBAL",
                language="zh",
                policy_type="payment",
                priority=1,
                source="official_2026Q1",
                content="支付失败常见原因包括余额不足。",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = recognize_intent("支付失败怎么办")
        response = generate_mock_rag_answer("支付失败怎么办", intent, chunks)

        # Citations should still be present in structured field
        assert len(response.citations) > 0
        assert response.citations[0].doc_id == "PAY-001"

        # Retrieved doc IDs should still be present
        assert len(response.retrieved_doc_ids) > 0
        assert "PAY-001" in response.retrieved_doc_ids

    def test_retrieved_doc_ids_still_returned(self):
        """retrieved_doc_ids should still be in the response."""
        from backend.app.agent.intent_recognizer import recognize_intent
        from backend.app.agent.mock_answer_generator import generate_mock_rag_answer
        from backend.app.rag.schemas import RetrievedChunk

        chunks = [
            RetrievedChunk(
                chunk_id="REF-001::chunk_001",
                doc_id="REF-001",
                title="退款政策",
                category="refund",
                market="GLOBAL",
                language="zh",
                policy_type="refund",
                priority=1,
                source="official_2026Q1",
                content="退款到账时间一般为 3-10 个工作日。",
                chunk_index=0,
                score=5.0,
            ),
        ]

        intent = recognize_intent("退款多久到账")
        response = generate_mock_rag_answer("退款多久到账", intent, chunks)

        assert "REF-001" in response.retrieved_doc_ids
