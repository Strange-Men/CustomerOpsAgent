"""
CustomerOps Agent - Fallback Rules

Exception handling and fallback rules for customer service agent workflow.
Ensures safe responses when evidence is insufficient or intent is unclear.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .schemas import (
    EvidenceCheckResult,
    ExtractedVariables,
    IntentResult,
    LogisticsToolResult,
)

if TYPE_CHECKING:
    from backend.app.rag.schemas import RetrievedChunk


def detect_sensitive_order_query(query: str) -> bool:
    """
    Detect if query contains sensitive information requests.

    Checks for requests for passwords, verification codes, full bank card numbers.
    """
    if not query:
        return False

    sensitive_patterns = [
        "密码", "验证码", "银行卡号", "卡号", "cvv", "安全码",
        "password", "verification code", "bank card", "card number",
        "pin", "security code", "cvv2", "cvc",
    ]

    query_lower = query.lower()
    return any(pattern in query_lower for pattern in sensitive_patterns)


def detect_private_info_request(query: str) -> bool:
    """
    Detect if query is asking for private/sensitive information.

    Checks if user is being asked to provide sensitive data.
    """
    if not query:
        return False

    private_patterns = [
        "提供密码", "提供验证码", "提供银行卡", "发送验证码", "告诉密码",
        "provide password", "send verification", "give card number",
        "share password", "tell me your", "what is your password",
    ]

    query_lower = query.lower()
    return any(pattern in query_lower for pattern in private_patterns)


def evaluate_evidence(
    retrieved_chunks: list["RetrievedChunk"],
    intent_result: IntentResult,
    min_score: float = 1.0,
) -> EvidenceCheckResult:
    """
    Evaluate evidence quality from retrieved chunks.

    Args:
        retrieved_chunks: List of retrieved chunks
        intent_result: Intent recognition result
        min_score: Minimum score threshold for usable chunks

    Returns:
        EvidenceCheckResult with evidence evaluation
    """
    if not retrieved_chunks:
        return EvidenceCheckResult(
            has_evidence=False,
            confidence="low",
            reasons=["检索无结果"],
            usable_chunks_count=0,
        )

    # Count usable chunks (score >= min_score)
    usable_chunks = [c for c in retrieved_chunks if c.score >= min_score]

    if not usable_chunks:
        return EvidenceCheckResult(
            has_evidence=False,
            confidence="low",
            reasons=["top score 过低"],
            usable_chunks_count=0,
        )

    # Check category match
    category_match = False
    intent_category = intent_result.detail_intent

    for chunk in usable_chunks:
        if hasattr(chunk, 'category') and chunk.category:
            if chunk.category.lower() == intent_category.lower():
                category_match = True
                break

    # Determine confidence
    top_score = max(c.score for c in usable_chunks)

    if top_score >= 5.0 and category_match:
        confidence = "high"
        reasons = ["top score 高且 category 匹配"]
    elif top_score >= 3.0:
        confidence = "medium"
        reasons = ["top score 中等"]
        if not category_match:
            reasons.append("category 不完全匹配")
    else:
        confidence = "low"
        reasons = ["top score 较低"]

    return EvidenceCheckResult(
        has_evidence=True,
        confidence=confidence,
        reasons=reasons,
        usable_chunks_count=len(usable_chunks),
    )


def should_fallback(
    query: str,
    intent_result: IntentResult,
    evidence: EvidenceCheckResult | None = None,
    tool_result: LogisticsToolResult | None = None,
    variables: ExtractedVariables | None = None,
) -> tuple[bool, str | None]:
    """
    Determine if fallback should be triggered.

    Args:
        query: User query
        intent_result: Intent recognition result
        evidence: Evidence check result (for RAG route)
        tool_result: Logistics tool result (for logistics route)
        variables: Extracted variables

    Returns:
        Tuple of (should_fallback, reason)
    """
    # Rule 1: Query is empty
    if not query or not query.strip():
        return True, "empty_query"

    # Rule 2: Intent is other or unknown
    if intent_result.route_intent == "other" or intent_result.detail_intent == "unknown":
        return True, "unknown_intent"

    # Rule 3: Logistics status query but missing order ID
    # Only applies to logistics_status (real tracking queries), not logistics_policy
    if intent_result.route_intent == "logistics" and intent_result.detail_intent == "logistics_status":
        if variables and not variables.has_order_id:
            return True, "missing_order_id"

    # Rule 4: Logistics tool call failed
    if tool_result and not tool_result.success:
        return True, "logistics_tool_failed"

    # Rule 5: RAG retrieval no results
    if evidence and not evidence.has_evidence:
        return True, "no_evidence"

    # Rule 6: Top score too low
    if evidence and evidence.confidence == "low":
        return True, "low_evidence_confidence"

    # Rule 7: Citation not available (handled in workflow)

    # Rule 8: User asking about out-of-scope topics
    if intent_result.route_intent == "other":
        return True, "out_of_scope"

    # Rule 9: Multiple conflicting intents
    if intent_result.needs_clarification:
        return True, "needs_clarification"

    # Rule 10: Sensitive information request
    if detect_sensitive_order_query(query):
        return True, "sensitive_info_request"

    # Rule 11: Trace/origin without evidence
    if intent_result.detail_intent == "trace":
        if evidence and not evidence.has_evidence:
            return True, "trace_no_evidence"

    return False, None


def build_fallback_answer(reason: str | None, intent: str) -> str:
    """
    Build a fallback answer based on the reason.

    Args:
        reason: Fallback reason
        intent: User intent

    Returns:
        Appropriate fallback answer
    """
    fallback_answers = {
        "empty_query": "您好，请问有什么可以帮您的吗？",
        "unknown_intent": "抱歉，我无法理解您的问题。建议您联系人工客服获取帮助。",
        "missing_order_id": "您好，查询物流信息需要提供订单号。请您提供订单号，或登录账户查看订单状态。",
        "logistics_tool_failed": "抱歉，物流查询系统暂时无法获取信息。建议您稍后重试，或联系人工客服。",
        "no_evidence": "抱歉，当前知识库中未找到相关信息。建议您联系人工客服获取帮助。",
        "low_evidence_confidence": "您的问题我找到了一些相关信息，但置信度不够高。建议您与人工客服确认。",
        "out_of_scope": "您的问题超出了当前客服知识库的覆盖范围。建议您联系人工客服。",
        "needs_clarification": "您提到了多个问题，请问您最想处理哪一个？",
        "sensitive_info_request": "为了您的账户安全，请不要在对话中提供银行卡号、密码或验证码。如有需要，请联系人工客服。",
        "trace_no_evidence": "抱歉，当前知识库中没有产品溯源或检测报告信息。建议您联系人工客服或查看产品包装。",
    }

    answer = fallback_answers.get(reason, "抱歉，暂时无法处理您的问题。建议您联系人工客服获取帮助。")

    # Add intent-specific context
    if intent == "logistics" and reason != "missing_order_id":
        answer += "\n\n如需查询物流状态，建议您登录账户查看或提供订单号。"
    elif intent in ["aftersale", "trace"]:
        answer += "\n\n如需进一步处理，建议您联系人工客服。"

    return answer
