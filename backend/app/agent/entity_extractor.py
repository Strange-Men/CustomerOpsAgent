"""
CustomerOps Agent - Entity Extractor

Variable extraction node for customer service agent workflow.
Extracts order IDs and other variables from user queries.
"""

from __future__ import annotations

import re

from .schemas import ExtractedVariables


def extract_order_id(query: str) -> str | None:
    """
    Extract order ID from user query.

    Supports:
    - Chinese: 订单123456, 单号123456, 订单号：123456
    - English: order 123456, order id: ABC123456, tracking number: TRK123456
    - Alphanumeric: CN20250618001, ABC123456
    - At least 6 digits for pure numeric order IDs
    """
    if not query or not query.strip():
        return None

    # Pattern 1: Chinese order ID patterns
    # 订单123456, 单号123456, 订单号：123456, 订单号: 123456
    zh_patterns = [
        r'订单[号]?[：:\s]*([A-Za-z0-9]{6,})',
        r'单号[：:\s]*([A-Za-z0-9]{6,})',
        r'快递[单号]?[：:\s]*([A-Za-z0-9]{6,})',
    ]

    for pattern in zh_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Pattern 2: English order ID patterns
    # order 123456, order id: ABC123456, order id ABC123456
    en_patterns = [
        r'order\s*(?:id|number)?[：:\s]*([A-Za-z0-9]{6,})',
        r'tracking\s*(?:number|id)?[：:\s]*([A-Za-z0-9]{6,})',
        r'parcel\s*(?:number|id)?[：:\s]*([A-Za-z0-9]{6,})',
        r'shipment\s*(?:number|id)?[：:\s]*([A-Za-z0-9]{6,})',
    ]

    for pattern in en_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Pattern 3: Standalone alphanumeric order ID (at least 6 chars)
    # CN20250618001, ABC123456, TRK123456
    standalone_pattern = r'\b([A-Z]{2,}[0-9]{4,}[A-Z0-9]*)\b'
    match = re.search(standalone_pattern, query, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Pattern 4: Standalone numeric order ID (at least 6 digits)
    standalone_numeric = r'\b(\d{6,})\b'
    match = re.search(standalone_numeric, query)
    if match:
        return match.group(1).strip()

    return None


def extract_customer_variables(
    query: str,
    existing_order_id: str | None = None,
) -> ExtractedVariables:
    """
    Extract customer variables from query.

    Args:
        query: User query
        existing_order_id: Order ID from upstream conversation context

    Returns:
        ExtractedVariables with order_id and has_order_id
    """
    # Try to extract order ID from query
    order_id = extract_order_id(query)

    # If not found in query, use existing order ID
    if order_id is None and existing_order_id:
        order_id = existing_order_id

    return ExtractedVariables(
        order_id=order_id,
        has_order_id=order_id is not None,
    )
