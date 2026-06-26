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

    Prioritizes diverse doc_ids: prefers one citation per unique doc_id
    before adding duplicates from the same doc.

    Args:
        retrieved_chunks: Retrieved evidence chunks

    Returns:
        List of Citation objects (up to 5, preferring diverse doc_ids)
    """
    citations = []
    seen_doc_ids: set[str] = set()
    max_citations = 5

    # First pass: one citation per unique doc_id (preserving order)
    for chunk in retrieved_chunks:
        if len(citations) >= max_citations:
            break
        if chunk.doc_id not in seen_doc_ids:
            seen_doc_ids.add(chunk.doc_id)
            citations.append(Citation(
                doc_id=chunk.doc_id,
                chunk_id=chunk.chunk_id,
                title=chunk.title,
                source=chunk.source,
                category=chunk.category,
                market=chunk.market,
                language=chunk.language,
            ))

    # Second pass: fill remaining slots with any chunks
    for chunk in retrieved_chunks:
        if len(citations) >= max_citations:
            break
        if chunk.chunk_id not in {c.chunk_id for c in citations}:
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


def _extract_evidence_sentences(
    retrieved_chunks: list["RetrievedChunk"],
    max_chunks: int = 3,
    max_chars_per_chunk: int = 400,
) -> str:
    """
    Extract key evidence sentences from multiple retrieved chunks.

    Uses content from top N chunks to improve keyword coverage.

    Args:
        retrieved_chunks: Retrieved evidence chunks
        max_chunks: Maximum number of chunks to use
        max_chars_per_chunk: Maximum characters per chunk content

    Returns:
        Combined evidence text from multiple chunks
    """
    evidence_parts = []
    seen_content = set()

    for chunk in retrieved_chunks[:max_chunks]:
        content = chunk.content.strip()
        if not content:
            continue
        # Deduplicate similar content
        content_key = content[:50]
        if content_key in seen_content:
            continue
        seen_content.add(content_key)

        # Truncate if too long
        if len(content) > max_chars_per_chunk:
            # Try to find a sentence boundary
            truncated = content[:max_chars_per_chunk]
            last_period = max(truncated.rfind("。"), truncated.rfind("；"), truncated.rfind("."))
            if last_period > max_chars_per_chunk // 2:
                content = truncated[:last_period + 1]
            else:
                content = truncated + "..."

        evidence_parts.append(content)

    return "\n\n".join(evidence_parts)


def generate_mock_rag_answer(
    query: str,
    intent_result: IntentResult,
    retrieved_chunks: list["RetrievedChunk"],
) -> AgentResponse:
    """
    Generate a mock answer for RAG-based routes.

    This is a template-based implementation that does not call real LLM APIs.
    Uses content from multiple retrieved chunks for better evidence coverage.

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

    # Extract evidence from multiple chunks
    evidence_text = _extract_evidence_sentences(retrieved_chunks, max_chunks=3)

    # Build answer based on intent with improved evidence coverage
    detail_intent = intent_result.detail_intent

    if detail_intent == "customs":
        answer = (
            f"您好，关于清关问题，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"清关延迟通常由海关抽检、申报信息不完整或节假日等因素导致，一般延迟 3-15 个工作日属正常范围。\n"
            f"建议您：1）通过物流追踪号查看包裹状态；2）如超过 15 个工作日未放行，联系人工客服协助处理。"
        )
    elif detail_intent == "return":
        answer = (
            f"您好，关于退货政策，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"建议您在签收后规定时间内申请退货，保持商品原包装完好。\n"
            f"如需操作，请登录账户在订单详情页提交退货申请，或联系人工客服协助。"
        )
    elif detail_intent == "refund":
        answer = (
            f"您好，关于退款问题，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"退款到账时间取决于支付方式，一般为 3-10 个工作日。\n"
            f"如涉及退货退款，请先完成退货流程，退款将在商品验收后启动。\n"
            f"如需查询退款进度，建议联系人工客服并提供订单号。"
        )
    elif detail_intent == "exchange":
        answer = (
            f"您好，关于换货政策，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"如需申请换货，建议您在签收后规定时间内登录账户操作，或联系人工客服协助处理。"
        )
    elif detail_intent == "address":
        answer = (
            f"您好，关于地址修改，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"如需修改收货地址，请尽快登录账户操作。已发货订单可能无法修改地址，建议联系人工客服确认。"
        )
    elif detail_intent == "order":
        # Check if query also mentions refund (multi-intent: order cancel + refund)
        query_lower = query.lower()
        if any(kw in query_lower for kw in ["退款", "退钱", "refund", "money back"]):
            answer = (
                f"您好，关于订单取消及退款，以下是相关信息：\n\n"
                f"{evidence_text}\n\n"
                f"订单取消后，退款将按原支付路径退回，具体到账时间以支付平台处理为准。\n"
                f"如有其他问题，请联系人工客服并提供订单号。"
            )
        else:
            answer = (
                f"您好，关于订单问题，以下是相关信息：\n\n"
                f"{evidence_text}\n\n"
                f"如有其他问题，请联系人工客服并提供订单号以便查询。"
            )
    elif detail_intent == "payment":
        answer = (
            f"您好，关于支付问题，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"如遇支付异常，建议您：1）检查支付方式是否支持跨境交易；2）确认扣款状态；3）如重复扣款，请联系人工客服并提供银行流水。"
        )
    elif detail_intent == "package":
        answer = (
            f"您好，关于包裹问题，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"如包裹显示已签收但未收到，或存在损坏/丢失情况，建议您：\n"
            f"1）检查是否由他人代收；2）联系物流方确认；3）如确认丢包或损坏，请联系人工客服申请理赔。"
        )
    elif detail_intent == "coupon":
        answer = (
            f"您好，关于优惠券问题，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"如优惠券无法使用，请检查是否在有效期内、是否满足使用条件。\n"
            f"如有其他问题，请联系人工客服。"
        )
    elif detail_intent == "trace":
        answer = (
            f"您好，关于产品溯源信息，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"如需更详细的溯源或检测报告信息，建议您查看产品包装或联系人工客服。"
        )
    elif detail_intent == "logistics_policy":
        query_lower = query.lower()
        is_delay = any(kw in query_lower for kw in [
            "还没到", "还没收到", "一个月", "三周", "两周", "太慢", "比美国慢",
            "hasn't arrived", "not arrived", "two weeks", "three weeks", "delay",
            "taking too long", "late",
        ])
        if is_delay:
            answer = (
                f"您好，关于物流配送时效，以下是相关信息：\n\n"
                f"{evidence_text}\n\n"
                f"跨境物流受目的地、清关等因素影响，实际配送时间可能比标准时效延长 3-5 个工作日。\n"
                f"如您的包裹长时间未到达，建议：1）通过物流追踪号查看最新状态；2）联系人工客服查询。"
            )
        else:
            answer = (
                f"您好，关于物流配送，以下是相关信息：\n\n"
                f"{evidence_text}\n\n"
                f"如有其他物流问题，建议联系人工客服或提供订单号以便查询。"
            )
    else:
        answer = (
            f"您好，根据当前知识库，以下是相关信息：\n\n"
            f"{evidence_text}\n\n"
            f"如有其他问题，请联系人工客服获取帮助。"
        )

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
