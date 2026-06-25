"""
CustomerOps Agent - Mock Answer Generator

Mock answer generation for customer service agent workflow.
Generates template-based answers without calling real LLM APIs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .schemas import (
    AgentResponse,
    Citation,
    IntentResult,
    LogisticsToolResult,
)

if TYPE_CHECKING:
    from backend.app.rag.schemas import RetrievedChunk


def _build_citations(retrieved_chunks: list["RetrievedChunk"]) -> list[Citation]:
    """
    Build citations from retrieved chunks.

    Args:
        retrieved_chunks: Retrieved evidence chunks

    Returns:
        List of Citation objects
    """
    citations = []
    for chunk in retrieved_chunks[:5]:  # Limit to top 5
        citations.append(Citation(
            doc_id=chunk.doc_id,
            chunk_id=chunk.chunk_id,
            title=chunk.title,
            source=chunk.source,
            category=chunk.category,
            market=chunk.market,
            language=chunk.language,
        ))
    return citations


def generate_mock_rag_answer(
    query: str,
    intent_result: IntentResult,
    retrieved_chunks: list["RetrievedChunk"],
) -> AgentResponse:
    """
    Generate a mock answer for RAG-based routes.

    This is a template-based implementation that does not call real LLM APIs.

    Args:
        query: User query
        intent_result: Intent recognition result
        retrieved_chunks: Retrieved evidence chunks

    Returns:
        AgentResponse with template-based answer and citations
    """
    # Build citations from retrieved chunks
    citations = _build_citations(retrieved_chunks)

    # Build retrieved doc IDs
    retrieved_doc_ids = list(dict.fromkeys(c.doc_id for c in retrieved_chunks))

    # Get top chunk content for answer
    if retrieved_chunks:
        top_chunk = retrieved_chunks[0]
        top_content = top_chunk.content[:200] + "..." if len(top_chunk.content) > 200 else top_chunk.content
        top_doc_id = top_chunk.doc_id
    else:
        top_content = ""
        top_doc_id = ""

    # Build answer based on intent
    detail_intent = intent_result.detail_intent

    if detail_intent == "customs":
        answer = f"您好，关于清关问题：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如有进一步问题，建议您联系人工客服。"
    elif detail_intent == "return":
        answer = f"您好，关于退货政策：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如需申请退货，建议您登录账户操作或联系人工客服。"
    elif detail_intent == "refund":
        answer = f"您好，关于退款问题：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n退款到账时间以支付平台实际处理为准。如有疑问，请联系人工客服。"
    elif detail_intent == "exchange":
        answer = f"您好，关于换货政策：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如需申请换货，建议您登录账户操作或联系人工客服。"
    elif detail_intent == "address":
        answer = f"您好，关于地址修改：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如需修改地址，请尽快登录账户操作或联系人工客服。"
    elif detail_intent == "order":
        answer = f"您好，关于订单问题：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如有其他问题，请联系人工客服。"
    elif detail_intent == "payment":
        answer = f"您好，关于支付问题：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如遇支付异常，建议您检查支付方式或联系人工客服。"
    elif detail_intent == "package":
        answer = f"您好，关于包裹问题：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如包裹有损坏或丢失，请及时联系人工客服处理。"
    elif detail_intent == "coupon":
        answer = f"您好，关于优惠券问题：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如有其他问题，请联系人工客服。"
    elif detail_intent == "trace":
        answer = f"您好，关于产品溯源信息：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如需更详细的溯源信息，建议您查看产品包装或联系人工客服。"
    else:
        answer = f"您好，根据知识库信息：\n\n{top_content}\n\n以上信息来自文档 {top_doc_id}。\n\n如有其他问题，请联系人工客服。"

    return AgentResponse(
        answer=answer,
        route="rag_knowledge_base",
        intent=intent_result.route_intent,
        detail_intent=intent_result.detail_intent,
        citations=citations,
        fallback_triggered=False,
        fallback_reason=None,
        confidence="medium",
        retrieved_doc_ids=retrieved_doc_ids,
        order_id=None,
        tool_used=None,
    )


def generate_mock_logistics_answer(
    query: str,
    intent_result: IntentResult,
    tool_result: LogisticsToolResult,
) -> AgentResponse:
    """
    Generate a mock answer for logistics tool route.

    This is a template-based implementation that does not call real LLM APIs.

    Args:
        query: User query
        intent_result: Intent recognition result
        tool_result: Logistics tool result

    Returns:
        AgentResponse with template-based logistics answer
    """
    # Build trace section
    trace_text = "\n".join([f"  • {t}" for t in tool_result.trace]) if tool_result.trace else "暂无物流轨迹"

    answer = f"""您好，根据物流查询结果：

📦 订单号：{tool_result.order_id}
📋 状态：{tool_result.status}
🚚 物流轨迹：
{trace_text}
⏰ 预计送达：{tool_result.estimated_delivery}

如有其他问题，建议您登录账户查看详细物流信息或联系人工客服。"""

    return AgentResponse(
        answer=answer,
        route="logistics_tool",
        intent=intent_result.route_intent,
        detail_intent=intent_result.detail_intent,
        citations=[],  # No citations for logistics tool route
        fallback_triggered=False,
        fallback_reason=None,
        confidence="high",
        retrieved_doc_ids=[],
        order_id=tool_result.order_id,
        tool_used="mock_logistics_tool",
    )


def generate_mock_answer(
    query: str,
    intent_result: IntentResult,
    retrieved_chunks: list["RetrievedChunk"] | None = None,
    tool_result: LogisticsToolResult | None = None,
) -> AgentResponse:
    """
    Unified entry point for mock answer generation.

    Args:
        query: User query
        intent_result: Intent recognition result
        retrieved_chunks: Retrieved evidence chunks (for RAG route)
        tool_result: Logistics tool result (for logistics route)

    Returns:
        AgentResponse with appropriate answer
    """
    # Route to logistics tool answer
    if tool_result and tool_result.success:
        return generate_mock_logistics_answer(query, intent_result, tool_result)

    # Route to RAG answer
    if retrieved_chunks:
        return generate_mock_rag_answer(query, intent_result, retrieved_chunks)

    # Fallback: no evidence and no tool result
    from .fallback_rules import build_fallback_answer
    fallback_answer = build_fallback_answer("no_evidence", intent_result.route_intent)

    return AgentResponse(
        answer=fallback_answer,
        route="fallback",
        intent=intent_result.route_intent,
        detail_intent=intent_result.detail_intent,
        citations=[],
        fallback_triggered=True,
        fallback_reason="no_evidence",
        confidence="low",
        retrieved_doc_ids=[],
        order_id=None,
        tool_used=None,
    )
