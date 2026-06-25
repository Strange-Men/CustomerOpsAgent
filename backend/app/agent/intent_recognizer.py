"""
CustomerOps Agent - Intent Recognizer

Intent recognition node for customer service agent workflow.
Rule-based classifier for identifying user intent from query.
"""

from __future__ import annotations

from .schemas import IntentResult

# Intent keyword mappings
# Each key is a detail_intent, value is a list of keywords (zh/en)
INTENT_KEYWORDS: dict[str, list[str]] = {
    "logistics": [
        # Chinese
        "快递", "物流", "配送", "运输", "到达", "送达", "派送",
        "到哪了", "到哪里了", "多久能到", "什么时候到", "什么时候送",
        "发货", "已发货", "未发货", "没发货", "已揽收", "运输中",
        "在途中", "在路上", "派件中", "已签收", "未签收",
        # English
        "shipping", "delivery", "parcel", "transit",
        "where is", "when will", "how long", "track", "tracking",
        "shipped", "dispatched", "delivered", "received",
        "estimated", "arrival", "courier", "carrier",
    ],
    "customs": [
        # Chinese
        "清关", "海关", "报关", "通关", "关税", "税费", "缴税",
        "清关延迟", "清关问题", "海关扣留", "海关检查",
        # English
        "customs", "clearance", "tariff", "duty", "tax",
        "customs delay", "customs hold", "customs inspection",
        "import duty", "customs fee",
    ],
    "return": [
        # Chinese
        "退货", "退回", "退回去", "怎么退", "退货流程", "退货政策",
        "申请退货", "退回商品", "退回地址", "退货原因",
        # English
        "return", "send back", "return policy", "return process",
        "how to return", "return item", "return goods",
    ],
    "refund": [
        # Chinese
        "退款", "退钱", "退费", "退款多久", "退款到账", "退款流程",
        "申请退款", "退款状态", "退款进度", "已退款", "未退款",
        # English
        "refund", "money back", "refund status", "refund process",
        "how long refund", "when refund", "refund policy",
    ],
    "exchange": [
        # Chinese
        "换货", "更换", "换一个", "换个颜色", "换个尺寸", "换货流程",
        "申请换货", "换货政策", "可以换吗", "换颜色", "换尺寸",
        # English
        "exchange", "swap", "replace", "change size", "change color",
        "exchange policy", "exchange process",
    ],
    "address": [
        # Chinese
        "地址", "改地址", "修改地址", "收货地址", "收件地址", "配送地址",
        "地址错了", "地址错误", "换地址", "改收货地址",
        # English
        "address", "change address", "shipping address", "delivery address",
        "wrong address", "update address", "modify address",
    ],
    "order": [
        # Chinese
        "订单", "订单状态", "订单查询", "查订单", "订单取消", "取消订单",
        "订单修改", "修改订单", "订单信息", "订单详情",
        # English
        "order", "order status", "order query", "cancel order",
        "order cancel", "order modify", "order info", "order detail",
    ],
    "payment": [
        # Chinese
        "支付", "付款", "付款失败", "支付失败", "支付问题", "付款问题",
        "没付成功", "付不了", "支付方式", "支付渠道", "扣款", "重复扣款",
        # English
        "payment", "pay", "payment failed", "payment error",
        "payment issue", "payment method", "charged", "double charged",
    ],
    "package": [
        # Chinese
        "破损", "损坏", "丢件", "丢失", "少件", "漏发",
        "包裹破损", "包裹损坏", "包裹丢失", "收到破损", "收到损坏",
        "外包装", "内包装", "商品损坏", "商品破损",
        # English
        "package", "damaged", "broken", "lost", "missing",
        "package damaged", "package lost", "package broken",
        "item damaged", "item broken", "wrong item",
    ],
    "coupon": [
        # Chinese
        "优惠券", "优惠码", "折扣", "促销", "满减", "折扣码",
        "优惠券不能用", "优惠码无效", "优惠券过期", "退款优惠券",
        # English
        "coupon", "discount", "promo", "promo code", "coupon code",
        "coupon not working", "coupon expired", "discount code",
    ],
    "trace": [
        # Chinese
        "溯源", "产地", "检测报告", "产品溯源", "原产地", "生产地",
        "检测", "认证", "质量检测", "产品认证", "来源", "来源证明",
        # English
        "trace", "origin", "certificate", "inspection", "traceability",
        "product origin", "country of origin", "quality certificate",
        "inspection report", "test report",
    ],
}

# Route intent mapping
ROUTE_INTENT_MAP: dict[str, str] = {
    "logistics": "logistics",
    "customs": "aftersale",  # Customs issues go to knowledge base
    "return": "aftersale",
    "refund": "aftersale",
    "exchange": "aftersale",
    "address": "aftersale",
    "order": "aftersale",
    "payment": "aftersale",
    "package": "aftersale",
    "coupon": "aftersale",
    "trace": "trace",
    "unknown": "other",
}

# Priority order for detail intents (higher index = higher priority)
# This is used when multiple intents match
INTENT_PRIORITY: list[str] = [
    "unknown",
    "customs",
    "return",
    "refund",
    "exchange",
    "address",
    "order",
    "payment",
    "package",
    "coupon",
    "logistics",
    "trace",
]


def recognize_intent(query: str) -> IntentResult:
    """
    Recognize user intent from query.

    Rule-based classifier that maps query keywords to intents.
    Supports both Chinese and English keywords.

    Args:
        query: User query string

    Returns:
        IntentResult with route_intent, detail_intent, confidence, matched_keywords
    """
    if not query or not query.strip():
        return IntentResult(
            route_intent="other",
            detail_intent="unknown",
            confidence=0.0,
            matched_keywords=[],
            needs_clarification=False,
        )

    query_lower = query.lower()
    matched_intents: dict[str, list[str]] = {}

    # Check each intent's keywords
    for intent, keywords in INTENT_KEYWORDS.items():
        matched = []
        for keyword in keywords:
            if keyword.lower() in query_lower:
                matched.append(keyword)
        if matched:
            matched_intents[intent] = matched

    # If no intent matched
    if not matched_intents:
        return IntentResult(
            route_intent="other",
            detail_intent="unknown",
            confidence=0.3,
            matched_keywords=[],
            needs_clarification=False,
        )

    # If single intent matched
    if len(matched_intents) == 1:
        detail_intent = list(matched_intents.keys())[0]
        route_intent = ROUTE_INTENT_MAP.get(detail_intent, "other")
        matched_keywords = matched_intents[detail_intent]

        # Confidence based on number of matched keywords
        confidence = min(0.5 + len(matched_keywords) * 0.1, 0.95)

        return IntentResult(
            route_intent=route_intent,
            detail_intent=detail_intent,
            confidence=confidence,
            matched_keywords=matched_keywords,
            needs_clarification=False,
        )

    # Multiple intents matched - use priority
    # Sort by priority (higher index = higher priority)
    sorted_intents = sorted(
        matched_intents.keys(),
        key=lambda x: INTENT_PRIORITY.index(x) if x in INTENT_PRIORITY else -1,
    )

    primary_intent = sorted_intents[-1]  # Highest priority
    route_intent = ROUTE_INTENT_MAP.get(primary_intent, "other")
    matched_keywords = matched_intents[primary_intent]

    # Check if intents are conflicting (different route intents)
    route_intents = set()
    for detail_intent in matched_intents:
        route_intents.add(ROUTE_INTENT_MAP.get(detail_intent, "other"))

    needs_clarification = len(route_intents) > 1

    # Confidence is lower when multiple intents match
    confidence = min(0.4 + len(matched_keywords) * 0.05, 0.8)

    return IntentResult(
        route_intent=route_intent,
        detail_intent=primary_intent,
        confidence=confidence,
        matched_keywords=matched_keywords,
        needs_clarification=needs_clarification,
    )
