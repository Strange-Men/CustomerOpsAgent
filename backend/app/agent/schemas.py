"""
CustomerOps Agent - Agent Layer Schemas

Data structures for the lightweight customer service agent workflow.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RouteType(str, Enum):
    """Route types for customer service agent workflow."""

    logistics_tool = "logistics_tool"
    rag_knowledge_base = "rag_knowledge_base"
    fallback = "fallback"


class CustomerIntent(BaseModel):
    """Two-layer intent design for customer service."""

    # High-level route intent
    route_intent: str = Field(
        ...,
        description="High-level route intent: logistics, aftersale, trace, other",
    )
    # Detailed intent for prompt and citation context
    detail_intent: str = Field(
        ...,
        description="Detailed intent: logistics_status, logistics_policy, customs, return, refund, exchange, address, order, payment, package, coupon, trace, unknown",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Intent recognition confidence, 0 to 1",
    )
    matched_keywords: list[str] = Field(
        default_factory=list,
        description="Keywords that matched during intent recognition",
    )
    needs_clarification: bool = Field(
        default=False,
        description="Whether clarification is needed due to multiple intents",
    )


class ExtractedVariables(BaseModel):
    """Variables extracted from user query."""

    order_id: Optional[str] = Field(
        None,
        description="Extracted order ID",
    )
    has_order_id: bool = Field(
        False,
        description="Whether order ID was found",
    )


class IntentResult(BaseModel):
    """Result of intent recognition."""

    route_intent: str = Field(
        ...,
        description="High-level route intent: logistics, aftersale, trace, other",
    )
    detail_intent: str = Field(
        ...,
        description="Detailed intent: logistics_status, logistics_policy, customs, return, refund, exchange, address, order, payment, package, coupon, trace, unknown",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Intent recognition confidence",
    )
    matched_keywords: list[str] = Field(
        default_factory=list,
        description="Keywords that matched during intent recognition",
    )
    needs_clarification: bool = Field(
        default=False,
        description="Whether clarification is needed",
    )


class LogisticsToolResult(BaseModel):
    """Result from mock logistics tool."""

    success: bool = Field(
        ...,
        description="Whether the tool call was successful",
    )
    order_id: Optional[str] = Field(
        None,
        description="Order ID queried",
    )
    status: Optional[str] = Field(
        None,
        description="Logistics status",
    )
    trace: list[str] = Field(
        default_factory=list,
        description="Logistics trace events",
    )
    estimated_delivery: Optional[str] = Field(
        None,
        description="Estimated delivery time",
    )
    reason: Optional[str] = Field(
        None,
        description="Failure reason if success=False",
    )


class Citation(BaseModel):
    """Citation from retrieved chunks."""

    doc_id: str = Field(
        ...,
        description="Document ID",
    )
    chunk_id: str = Field(
        ...,
        description="Chunk ID",
    )
    title: str = Field(
        ...,
        description="Document title",
    )
    source: str = Field(
        ...,
        description="Document source",
    )
    category: str = Field(
        ...,
        description="Document category",
    )
    market: str = Field(
        ...,
        description="Target market",
    )
    language: str = Field(
        ...,
        description="Language code",
    )


class EvidenceCheckResult(BaseModel):
    """Result of evidence check."""

    has_evidence: bool = Field(
        ...,
        description="Whether sufficient evidence was found",
    )
    confidence: str = Field(
        ...,
        description="Evidence confidence: high, medium, low",
    )
    reasons: list[str] = Field(
        default_factory=list,
        description="Reasons for evidence check result",
    )
    usable_chunks_count: int = Field(
        0,
        description="Number of usable chunks",
    )


class AgentResponse(BaseModel):
    """Final response from customer service agent."""

    answer: str = Field(
        ...,
        description="Generated answer",
    )
    route: str = Field(
        ...,
        description="Route taken: logistics_tool, rag_knowledge_base, fallback",
    )
    intent: str = Field(
        ...,
        description="High-level route intent",
    )
    detail_intent: str = Field(
        ...,
        description="Detailed intent",
    )
    citations: list[Citation] = Field(
        default_factory=list,
        description="Citations from retrieved chunks",
    )
    fallback_triggered: bool = Field(
        default=False,
        description="Whether fallback was triggered",
    )
    fallback_reason: Optional[str] = Field(
        None,
        description="Reason for fallback",
    )
    confidence: str = Field(
        ...,
        description="Overall confidence: high, medium, low",
    )
    retrieved_doc_ids: list[str] = Field(
        default_factory=list,
        description="Document IDs retrieved",
    )
    order_id: Optional[str] = Field(
        None,
        description="Order ID if extracted",
    )
    tool_used: Optional[str] = Field(
        None,
        description="Tool used (e.g., mock_logistics_tool)",
    )
    answer_source: str = Field(
        default="mock",
        description="Answer source: mock, real_llm, real_llm_fallback_mock",
    )
    llm_profile: Optional[str] = Field(
        None,
        description="LLM profile used: mock, deepseek, doubao, mimo",
    )
    llm_provider: Optional[str] = Field(
        None,
        description="LLM provider used (e.g., openai_compatible)",
    )
    llm_model: Optional[str] = Field(
        None,
        description="LLM model name used",
    )
