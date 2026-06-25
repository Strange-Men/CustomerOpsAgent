"""
CustomerOps Agent - Logistics Tool

Mock logistics plugin for customer service agent workflow.
Simulates logistics API calls without real external dependencies.
"""

from __future__ import annotations

from .schemas import LogisticsToolResult


def query_mock_logistics(order_id: str | None) -> LogisticsToolResult:
    """
    Query mock logistics information for an order.

    This is a mock implementation that simulates logistics API responses.
    No real external APIs are called.

    Args:
        order_id: Order ID to query

    Returns:
        LogisticsToolResult with simulated logistics data
    """
    # Case 1: No order ID provided
    if not order_id:
        return LogisticsToolResult(
            success=False,
            order_id=None,
            status=None,
            trace=[],
            estimated_delivery=None,
            reason="missing_order_id",
        )

    # Case 2: Simulate tool failure for special prefixes
    if order_id.upper().startswith("FAIL"):
        return LogisticsToolResult(
            success=False,
            order_id=order_id,
            status=None,
            trace=[],
            estimated_delivery=None,
            reason="tool_timeout",
        )

    # Case 3: Successful mock logistics query
    return LogisticsToolResult(
        success=True,
        order_id=order_id,
        status="in_transit",
        trace=[
            "包裹已到达目的地分拣中心",
            "正在安排末端派送",
        ],
        estimated_delivery="预计 2-4 个工作日内送达",
        reason=None,
    )
