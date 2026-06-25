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
    "logistics_status": [
        # Chinese - real logistics tracking queries (need order_id)
        "到哪了", "到哪里了", "什么时候到", "什么时候送",
        "快递到", "包裹到", "在哪了", "在哪里了",
        "已发货", "未发货", "没发货", "已揽收", "运输中",
        "在途中", "在路上", "派件中", "已签收", "未签收",
        "查快递", "查物流", "查包裹", "查配送",
        "快递进度", "物流进度", "包裹进度",
        # English - tracking queries
        "where is my", "where is the", "when will it arrive",
        "track my order", "tracking status", "track my package",
        "has it shipped", "not shipped yet", "in transit",
        "out for delivery", "delivered", "not delivered",
        "order status", "parcel status", "shipment status",
    ],
    "logistics_policy": [
        # Chinese - logistics policy/timeframe queries (don't need order_id)
        "物流多久", "配送时效", "运输时效", "物流时效",
        "多久能到", "几天到", "多少天", "发货时间",
        "加急", "快递费", "运费", "包邮", "免邮",
        "从哪里发货", "发货地", "仓库", "配送方式",
        "标准物流", "快速物流", "经济物流",
        "物流政策", "配送政策", "物流规则",
        # Chinese - shipping delay expressions (not lost/damaged)
        "还没到", "还没收到", "多久了还没", "一个月了还没",
        "三周了还没", "两周了还没", "快一个月", "快三周",
        "太慢了", "为什么还没到", "怎么还没到", "比美国慢",
        # English - policy queries
        "shipping time", "delivery time", "how long does shipping",
        "how long does delivery", "shipping cost", "free shipping",
        "express shipping", "standard shipping", "economy shipping",
        "shipping policy", "delivery policy", "shipping rate",
        "where do you ship from", "warehouse", "dispatch time",
        "expedited", "rush delivery", "shipping method",
        # English - shipping delay expressions (not lost/damaged)
        "hasn't arrived", "has not arrived", "still hasn't arrived",
        "still not arrived", "not arrived", "taking too long",
        "shipping delay", "delivery delay", "why hasn't",
        "package still hasn't", "still hasn't", "how long does it take",
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
        "可以取消", "能取消吗", "取消吗", "取消政策",
        # English
        "order", "order status", "order query", "cancel order",
        "order cancel", "order modify", "order info", "order detail",
        "can i cancel", "cancel policy", "cancellation",
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
        "碎了", "碎了怎么办", "赔偿", "理赔", "补发",
        "没收到包裹", "包裹没收到", "丢包",
        "还没收到", "没收到货", "一个月了还没",
        "丢了", "包裹丢了", "找不到包裹", "包裹找不到",
        # English
        "package", "damaged", "broken", "lost", "missing",
        "package damaged", "package lost", "package broken",
        "item damaged", "item broken", "wrong item",
        "compensation", "claim", "replacement",
        "not received", "haven't received", "never arrived",
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
    "logistics_status": "logistics",
    "logistics_policy": "aftersale",  # Policy queries go to RAG knowledge base
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
# logistics_status has high priority because tracking queries should be recognized
# even when they contain generic words like "订单" or "包裹"
INTENT_PRIORITY: list[str] = [
    "unknown",
    "customs",
    "return",
    "exchange",
    "address",
    "payment",
    "coupon",
    "trace",
    "order",
    "refund",
    "logistics_policy",
    "package",
    "logistics_status",
]


# Package-specific keywords that override logistics_status classification
_PACKAGE_OVERRIDE_KEYWORDS = [
    "丢", "碎", "坏", "赔偿", "理赔", "没收到", "破损", "损坏",
    "少件", "漏发", "错发", "wrong", "damaged", "broken", "missing",
    "lost", "compensation", "claim", "never received", "not received",
]

# Policy-related keywords that indicate a policy question, not a status query
_POLICY_OVERRIDE_KEYWORDS = [
    "取消", "退款", "退货", "换货", "政策", "规则", "多久到账",
    "怎么退", "怎么取消", "可以取消", "能取消", "cancel", "refund",
    "return", "exchange", "policy",
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

    # Multiple intents matched - apply disambiguation rules

    # Rule 1: If logistics_status and package both match, check for package-specific keywords
    if "logistics_status" in matched_intents and "package" in matched_intents:
        has_package_override = any(
            kw in query_lower for kw in _PACKAGE_OVERRIDE_KEYWORDS
        )
        # Check for delay indicators — delay should NOT be overridden to package
        delay_indicators = [
            "一个月", "三周", "两周", "一周", "很久", "太慢", "太久了",
            "快一个月", "快三周", "快两周",
            "two weeks", "three weeks", "a month", "weeks",
            "hasn't arrived", "has not arrived", "still hasn't",
            "not arrived", "taking too long", "shipping delay",
        ]
        has_delay = any(ind in query_lower for ind in delay_indicators)
        if has_package_override and not has_delay:
            # Package issue takes precedence over logistics tracking
            primary_intent = "package"
            matched_keywords = matched_intents["package"]
            route_intent = ROUTE_INTENT_MAP.get(primary_intent, "other")
            confidence = min(0.5 + len(matched_keywords) * 0.1, 0.9)
            return IntentResult(
                route_intent=route_intent,
                detail_intent=primary_intent,
                confidence=confidence,
                matched_keywords=matched_keywords,
                needs_clarification=False,
            )
        elif has_delay:
            # Shipping delay → logistics_policy (not package)
            primary_intent = "logistics_policy"
            matched_keywords = matched_intents.get("logistics_policy", matched_intents.get("logistics_status", []))
            route_intent = ROUTE_INTENT_MAP.get(primary_intent, "aftersale")
            confidence = min(0.5 + len(matched_keywords) * 0.1, 0.9)
            return IntentResult(
                route_intent=route_intent,
                detail_intent=primary_intent,
                confidence=confidence,
                matched_keywords=matched_keywords,
                needs_clarification=False,
            )

    # Rule 1b: If logistics_policy and refund both match, check if it's a refund query
    # "退款多久能到账" matches both "退款" (refund) and "多久能到" (logistics_policy)
    # When refund keywords are present, refund intent should take precedence
    if "logistics_policy" in matched_intents and "refund" in matched_intents:
        refund_keywords = ["退款", "退钱", "退费", "refund", "money back"]
        has_refund = any(kw in query_lower for kw in refund_keywords)
        if has_refund:
            primary_intent = "refund"
            matched_keywords = matched_intents["refund"]
            route_intent = ROUTE_INTENT_MAP.get(primary_intent, "aftersale")
            confidence = min(0.5 + len(matched_keywords) * 0.1, 0.9)
            return IntentResult(
                route_intent=route_intent,
                detail_intent=primary_intent,
                confidence=confidence,
                matched_keywords=matched_keywords,
                needs_clarification=False,
            )

    # Rule 2: If logistics_status matches with order/refund/return, check for policy keywords
    policy_intents = {"order", "refund", "return", "exchange"}
    if "logistics_status" in matched_intents:
        matched_policy_intents = policy_intents & set(matched_intents.keys())
        if matched_policy_intents:
            has_policy = any(
                kw in query_lower for kw in _POLICY_OVERRIDE_KEYWORDS
            )
            has_tracking = any(
                kw in query_lower
                for kw in ["到哪了", "到哪里了", "在哪了", "在哪里了", "track", "where is"]
            )
            if has_policy and not has_tracking:
                # Policy query takes precedence over logistics_status
                # Use the highest-priority policy intent
                sorted_policy = sorted(
                    matched_policy_intents,
                    key=lambda x: INTENT_PRIORITY.index(x) if x in INTENT_PRIORITY else -1,
                )
                primary_intent = sorted_policy[-1]
                matched_keywords = matched_intents[primary_intent]
                route_intent = ROUTE_INTENT_MAP.get(primary_intent, "other")
                confidence = min(0.5 + len(matched_keywords) * 0.1, 0.9)
                return IntentResult(
                    route_intent=route_intent,
                    detail_intent=primary_intent,
                    confidence=confidence,
                    matched_keywords=matched_keywords,
                    needs_clarification=False,
                )

    # Rule 3: If logistics_status and order both match, check for tracking keywords
    if "logistics_status" in matched_intents and "order" in matched_intents:
        tracking_keywords = ["到哪了", "到哪里了", "在哪了", "在哪里了", "track", "where is"]
        has_tracking = any(kw in query_lower for kw in tracking_keywords)
        if has_tracking:
            # Tracking query takes precedence over generic order query
            primary_intent = "logistics_status"
            matched_keywords = matched_intents["logistics_status"]
            route_intent = ROUTE_INTENT_MAP.get(primary_intent, "other")
            confidence = min(0.5 + len(matched_keywords) * 0.1, 0.9)
            return IntentResult(
                route_intent=route_intent,
                detail_intent=primary_intent,
                confidence=confidence,
                matched_keywords=matched_keywords,
                needs_clarification=False,
            )

    # Rule 4: If logistics_status/logistics_policy and package both match,
    # check for delay indicators vs damage/loss indicators.
    # "包裹一个月没到" is logistics delay, not package lost.
    # "包裹破损/丢失" is package issue.
    logistics_intents_in_match = {"logistics_status", "logistics_policy"} & set(matched_intents.keys())
    if logistics_intents_in_match and "package" in matched_intents:
        # Delay indicators: shipping is slow, not lost/damaged
        delay_indicators = [
            "一个月", "三周", "两周", "一周", "很久", "太慢", "太久了",
            "还没到", "还没收到", "多久了", "为什么还没", "怎么还没",
            "比美国慢", "比欧洲慢",
            "two weeks", "three weeks", "a month", "weeks", "long time",
            "hasn't arrived", "has not arrived", "still hasn't",
            "still not arrived", "not arrived", "taking too long",
            "shipping delay", "delivery delay",
        ]
        # Damage/loss indicators: actual package issue
        damage_indicators = [
            "丢", "碎", "坏", "破损", "损坏", "丢失", "少件", "漏发",
            "错发", "赔偿", "理赔", "补发",
            "damaged", "broken", "lost", "missing", "wrong",
            "compensation", "claim", "replacement",
        ]
        has_delay = any(ind in query_lower for ind in delay_indicators)
        has_damage = any(ind in query_lower for ind in damage_indicators)

        if has_delay and not has_damage:
            # Shipping delay → logistics_policy (RAG, no order_id needed)
            primary_intent = "logistics_policy"
            matched_keywords = matched_intents.get("logistics_policy", matched_intents.get("logistics_status", []))
            route_intent = ROUTE_INTENT_MAP.get(primary_intent, "aftersale")
            confidence = min(0.5 + len(matched_keywords) * 0.1, 0.9)
            return IntentResult(
                route_intent=route_intent,
                detail_intent=primary_intent,
                confidence=confidence,
                matched_keywords=matched_keywords,
                needs_clarification=False,
            )

    # Default: use priority ordering
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
