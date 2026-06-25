"""
CustomerOps Agent - Prompt Builder

Prompt construction for customer service agent workflow.
Builds structured prompts for answer generation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .schemas import IntentResult, LogisticsToolResult

if TYPE_CHECKING:
    from backend.app.rag.schemas import RetrievedChunk


def build_customer_service_prompt(
    query: str,
    intent_result: IntentResult,
    retrieved_chunks: list["RetrievedChunk"],
) -> str:
    """
    Build a structured prompt for customer service answer generation.

    This prompt is designed for RAG-based answers (aftersale, trace, etc.).

    Args:
        query: User query
        intent_result: Intent recognition result
        retrieved_chunks: Retrieved evidence chunks

    Returns:
        Structured prompt string
    """
    # Build evidence section
    evidence_lines = []
    for i, chunk in enumerate(retrieved_chunks[:5], 1):
        evidence_lines.append(f"""
--- Evidence {i} ---
doc_id: {chunk.doc_id}
chunk_id: {chunk.chunk_id}
title: {chunk.title}
source: {chunk.source}
category: {chunk.category}
market: {chunk.market}
language: {chunk.language}
content: {chunk.content}
---""")
    evidence_section = "\n".join(evidence_lines)

    # Build prompt
    prompt = f"""你是一个跨境电商客服助手，负责回答客户关于售后、物流、退货、退款等问题。

## 用户问题
{query}

## 意图识别结果
- 高层意图: {intent_result.route_intent}
- 详细意图: {intent_result.detail_intent}
- 置信度: {intent_result.confidence:.2f}

## 知识库证据
{evidence_section}

## 回答规则
1. **只能基于上述证据回答**。如果证据不足，回复"抱歉，当前知识库中未找到相关信息，建议您联系人工客服。"
2. **不要编造信息**。只使用证据中明确提到的内容。
3. **必须给出引用**。每个核心断言至少引用一个 doc_id。
4. **不要索要敏感信息**。不要要求用户提供密码、验证码、完整银行卡号。
5. **语气要求**：礼貌、简洁、专业、安抚。先安抚客户，再说明情况，最后提供解决方案或建议。
6. **如果无法确定**：回复"抱歉，我无法确认这个问题的答案，建议您联系人工客服。"

## 回答格式
请基于上述证据，用客服语气回答用户问题。回答中请引用相关文档的 doc_id。
"""
    return prompt


def build_logistics_prompt(
    query: str,
    tool_result: LogisticsToolResult,
) -> str:
    """
    Build a structured prompt for logistics answer generation.

    This prompt is designed for logistics tool-based answers.

    Args:
        query: User query
        tool_result: Logistics tool result

    Returns:
        Structured prompt string
    """
    # Build trace section
    trace_section = ""
    if tool_result.trace:
        trace_lines = [f"  - {t}" for t in tool_result.trace]
        trace_section = "\n".join(trace_lines)

    prompt = f"""你是一个跨境电商客服助手，负责回答客户关于物流配送的问题。

## 用户问题
{query}

## 物流查询结果
- 订单号: {tool_result.order_id}
- 状态: {tool_result.status}
- 预计送达: {tool_result.estimated_delivery}
- 物流轨迹:
{trace_section}

## 回答规则
1. **只能基于物流查询结果回答**。不要编造物流信息。
2. **必须说明信息来自物流查询**。例如"根据物流查询结果"或"物流信息显示"。
3. **不要索要敏感信息**。不要要求用户提供密码、验证码、完整银行卡号。
4. **语气要求**：礼貌、简洁、专业、安抚。先安抚客户，再告知物流状态，最后说明预计时间。
5. **如果查询失败**：建议客户稍后重试或联系人工客服。

## 回答格式
请基于物流查询结果，用客服语气回答用户问题。回答中请说明信息来源。
"""
    return prompt
