"""
CustomerOps Agent - Workflow Orchestrator

Main workflow for customer service agent.
Orchestrates the node-based agent workflow:
Start Node → Variable Extraction → Intent Recognition → Route Decision → Tool/RAG → Fallback → End
"""

from __future__ import annotations

from .entity_extractor import extract_customer_variables
from .fallback_rules import (
    build_fallback_answer,
    evaluate_evidence,
    should_fallback,
)
from .intent_recognizer import recognize_intent
from .logistics_tool import query_mock_logistics
from .mock_answer_generator import generate_mock_answer
from .prompt_builder import build_customer_service_prompt, build_logistics_prompt
from .schemas import AgentResponse


def run_customer_service_agent(
    user_query: str,
    order_id: str | None = None,
    conversation_history: list[str] | None = None,
    top_k: int = 5,
) -> AgentResponse:
    """
    Run the customer service agent workflow.

    This is the main entry point for the lightweight customer service agent.
    It orchestrates the node-based workflow:

    1. Start Node: Receive user_query, optional order_id, optional conversation_history
    2. Variable Extraction Node: Extract order ID and other variables
    3. Intent Recognition Node: Identify user intent
    4. Route Decision: Route to logistics tool, RAG knowledge base, or fallback
    5. Tool/RAG Node: Execute appropriate route
    6. Fallback Node: Handle errors and edge cases
    7. End Node: Return final response

    Args:
        user_query: User's question or request
        order_id: Optional order ID from upstream conversation context
        conversation_history: Optional conversation history (max 5 recent messages)
        top_k: Number of top results to retrieve from knowledge base

    Returns:
        AgentResponse with answer, route, intent, citations, and metadata
    """
    # ============================================================
    # Start Node
    # ============================================================
    # Limit conversation history to most recent 5 messages
    if conversation_history:
        conversation_history = conversation_history[-5:]

    # ============================================================
    # Variable Extraction Node
    # ============================================================
    variables = extract_customer_variables(
        query=user_query,
        existing_order_id=order_id,
    )

    # ============================================================
    # Intent Recognition Node
    # ============================================================
    intent_result = recognize_intent(user_query)

    # ============================================================
    # Route Decision
    # ============================================================

    # Route 1: Logistics Tool Route (logistics_status: real tracking queries)
    if intent_result.route_intent == "logistics" and intent_result.detail_intent == "logistics_status":
        # Call mock logistics tool
        tool_result = query_mock_logistics(variables.order_id)

        if tool_result.success:
            # Tool success: Generate logistics answer
            # Build prompt for answer generation (used by mock_answer_generator)
            build_logistics_prompt(user_query, tool_result)
            response = generate_mock_answer(
                query=user_query,
                intent_result=intent_result,
                tool_result=tool_result,
            )
            return response
        else:
            # Tool failed: Fallback
            fallback_reason = tool_result.reason or "logistics_tool_failed"
            fallback_answer = build_fallback_answer(fallback_reason, intent_result.route_intent)

            return AgentResponse(
                answer=fallback_answer,
                route="fallback",
                intent=intent_result.route_intent,
                detail_intent=intent_result.detail_intent,
                citations=[],
                fallback_triggered=True,
                fallback_reason=fallback_reason,
                confidence="low",
                retrieved_doc_ids=[],
                order_id=variables.order_id,
                tool_used=None,
            )

    # Route 2: RAG Knowledge Base Route (aftersale, trace)
    elif intent_result.route_intent in ["aftersale", "trace"]:
        # Import retriever here to avoid circular imports
        from backend.app.rag.optimized_retriever import build_default_optimized_retriever

        # Build retriever and search
        retriever = build_default_optimized_retriever()
        retrieved_chunks = retriever.search(user_query, top_k=top_k)

        # Evaluate evidence
        evidence = evaluate_evidence(retrieved_chunks, intent_result)

        # Check if fallback should be triggered
        fallback, fallback_reason = should_fallback(
            query=user_query,
            intent_result=intent_result,
            evidence=evidence,
            variables=variables,
        )

        if fallback:
            fallback_answer = build_fallback_answer(fallback_reason, intent_result.route_intent)

            return AgentResponse(
                answer=fallback_answer,
                route="fallback",
                intent=intent_result.route_intent,
                detail_intent=intent_result.detail_intent,
                citations=[],
                fallback_triggered=True,
                fallback_reason=fallback_reason,
                confidence="low",
                retrieved_doc_ids=[c.doc_id for c in retrieved_chunks],
                order_id=variables.order_id,
                tool_used=None,
            )

        # Evidence check passed: Generate RAG answer
        # Build prompt for answer generation (used by mock_answer_generator)
        build_customer_service_prompt(user_query, intent_result, retrieved_chunks)
        response = generate_mock_answer(
            query=user_query,
            intent_result=intent_result,
            retrieved_chunks=retrieved_chunks,
        )

        # Citation check: Ensure citations come from retrieved chunks
        retrieved_chunk_ids = set(c.chunk_id for c in retrieved_chunks)
        valid_citations = [
            c for c in response.citations
            if c.chunk_id in retrieved_chunk_ids
        ]

        # Update response with validated citations
        response.citations = valid_citations
        response.retrieved_doc_ids = list(dict.fromkeys(c.doc_id for c in retrieved_chunks))

        return response

    # Route 3: Fallback Route (other intent)
    else:
        fallback_reason = "unknown_intent"
        fallback_answer = build_fallback_answer(fallback_reason, intent_result.route_intent)

        return AgentResponse(
            answer=fallback_answer,
            route="fallback",
            intent=intent_result.route_intent,
            detail_intent=intent_result.detail_intent,
            citations=[],
            fallback_triggered=True,
            fallback_reason=fallback_reason,
            confidence="low",
            retrieved_doc_ids=[],
            order_id=variables.order_id,
            tool_used=None,
        )


def _format_output(response: AgentResponse, query: str) -> str:
    """Format agent response for CLI output."""
    lines = [
        "=" * 60,
        "CustomerOps Agent - Workflow Result",
        "=" * 60,
        f"Query: {query}",
        f"Route: {response.route}",
        f"Intent: {response.intent}",
        f"Detail Intent: {response.detail_intent}",
        f"Order ID: {response.order_id or 'N/A'}",
        f"Fallback Triggered: {response.fallback_triggered}",
        f"Fallback Reason: {response.fallback_reason or 'N/A'}",
        f"Tool Used: {response.tool_used or 'N/A'}",
        f"Confidence: {response.confidence}",
        "-" * 60,
        "Answer:",
        response.answer,
        "-" * 60,
    ]

    if response.citations:
        lines.append("Citations:")
        for i, c in enumerate(response.citations, 1):
            lines.append(f"  {i}. {c.doc_id} ({c.title}) - {c.source}")
    else:
        lines.append("Citations: None")

    if response.retrieved_doc_ids:
        lines.append(f"Retrieved Doc IDs: {', '.join(response.retrieved_doc_ids)}")
    else:
        lines.append("Retrieved Doc IDs: None")

    lines.append("=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    import io

    # Set stdout to UTF-8 encoding for Windows
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print("Usage: python -m backend.app.agent.workflow <query>")
        print("Example: python -m backend.app.agent.workflow '我的订单123456的快递到哪了？'")
        sys.exit(1)

    query = sys.argv[1]
    result = run_customer_service_agent(query)
    print(_format_output(result, query))
