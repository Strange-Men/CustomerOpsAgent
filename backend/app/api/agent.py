"""
CustomerOps Agent - Agent Chat API

Exposes the customer service agent workflow as a FastAPI endpoint.
Internally calls run_customer_service_agent() — no workflow logic is duplicated here.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agent.schemas import AgentResponse
from app.agent.workflow import run_customer_service_agent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent", tags=["agent"])


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class AgentChatRequest(BaseModel):
    """Request body for POST /api/agent/chat."""

    user_query: str = Field(
        ...,
        min_length=1,
        description="User's question or request. Must not be empty.",
    )
    order_id: str | None = Field(
        None,
        description="Optional order ID from upstream context.",
    )
    conversation_history: list[str] = Field(
        default_factory=list,
        description="Optional conversation history (max 5 recent messages).",
    )


class AgentChatResponse(BaseModel):
    """Response body for POST /api/agent/chat.

    Mirrors the fields from AgentResponse so the API consumer gets the full
    workflow result without needing to import agent internals.
    """

    answer: str
    route: str
    intent: str
    detail_intent: str
    citations: list[dict]
    fallback_triggered: bool
    fallback_reason: str | None
    confidence: str
    retrieved_doc_ids: list[str]
    order_id: str | None
    tool_used: str | None


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------


@router.post("/chat", response_model=AgentChatResponse)
def agent_chat(request: AgentChatRequest) -> AgentChatResponse:
    """Run the customer service agent workflow and return the result.

    This endpoint is a thin wrapper around ``run_customer_service_agent()``.
    It handles request validation, history trimming, and error mapping —
    but all route / retrieval / answer / fallback logic lives in the
    workflow module.
    """
    try:
        # Trim conversation_history to last 5 messages (workflow also does this,
        # but we enforce it at the API boundary for safety).
        history = request.conversation_history[-5:] if request.conversation_history else []

        result: AgentResponse = run_customer_service_agent(
            user_query=request.user_query,
            order_id=request.order_id,
            conversation_history=history,
        )

        return _to_response(result)

    except Exception:
        logger.exception("Agent workflow failed for query: %s", request.user_query)
        raise HTTPException(
            status_code=500,
            detail="Internal server error: agent workflow failed.",
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_response(result: AgentResponse) -> AgentChatResponse:
    """Convert internal AgentResponse to the API response model."""
    return AgentChatResponse(
        answer=result.answer,
        route=result.route,
        intent=result.intent,
        detail_intent=result.detail_intent,
        citations=[c.model_dump() for c in result.citations],
        fallback_triggered=result.fallback_triggered,
        fallback_reason=result.fallback_reason,
        confidence=result.confidence,
        retrieved_doc_ids=result.retrieved_doc_ids,
        order_id=result.order_id,
        tool_used=result.tool_used,
    )
