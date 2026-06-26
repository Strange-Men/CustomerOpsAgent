"""Bad Case Bank schema for structured quality tracking.

Each bad case represents a typical customer service scenario with
explicit failure types, expected behavior, and optimization status.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Scenario(str, Enum):
    """Customer service scenario categories."""

    customs = "customs"
    refund = "refund"
    logistics = "logistics"
    payment = "payment"
    order = "order"
    package = "package"
    return_ = "return"
    exchange = "exchange"
    address = "address"
    coupon = "coupon"
    out_of_scope = "out_of_scope"
    mixed = "mixed"


class FailureType(str, Enum):
    """Types of quality failures in bad cases."""

    retrieval_miss = "retrieval_miss"
    route_error = "route_error"
    intent_error = "intent_error"
    missing_citation = "missing_citation"
    over_fallback = "over_fallback"
    hallucination_risk = "hallucination_risk"
    rigid_template = "rigid_template"
    incomplete_answer = "incomplete_answer"
    poor_customer_tone = "poor_customer_tone"
    missing_next_step = "missing_next_step"
    out_of_scope_error = "out_of_scope_error"


class BaselineStatus(str, Enum):
    """Baseline quality status before optimization."""

    fail = "fail"
    weak = "weak"
    pass_ = "pass"


class AfterStatus(str, Enum):
    """Quality status after optimization."""

    pending = "pending"
    pass_ = "pass"
    partial = "partial"
    fail = "fail"


class BadCase(BaseModel):
    """A structured bad case for quality tracking and optimization.

    Each case represents a typical customer service question with
    explicit failure types, expected behavior, and optimization status.
    """

    case_id: str = Field(
        ...,
        min_length=1,
        description="Unique case identifier",
    )
    user_query: str = Field(
        ...,
        min_length=1,
        description="Customer question text",
    )
    scenario: str = Field(
        ...,
        description=(
            "Scenario category: customs/refund/logistics/payment/order/"
            "package/return/exchange/address/coupon/out_of_scope/mixed"
        ),
    )
    expected_route: str = Field(
        ...,
        description=(
            "Expected route: logistics_tool/rag_knowledge_base/fallback"
        ),
    )
    expected_intent: str = Field(
        ...,
        description=(
            "Expected high-level intent: logistics/aftersale/trace/other"
        ),
    )
    expected_detail_intent: Optional[str] = Field(
        None,
        description=(
            "Expected detail intent: logistics_status/logistics_policy/"
            "customs/return/refund/exchange/address/order/payment/"
            "package/coupon/trace/unknown"
        ),
    )
    expected_behavior: str = Field(
        ...,
        min_length=1,
        description="What the answer should include or demonstrate",
    )
    required_evidence: list[str] = Field(
        default_factory=list,
        description="Required doc_ids or evidence sources",
    )
    failure_type: list[str] = Field(
        default_factory=list,
        description=(
            "Known failure types: retrieval_miss/route_error/intent_error/"
            "missing_citation/over_fallback/hallucination_risk/rigid_template/"
            "incomplete_answer/poor_customer_tone/missing_next_step/"
            "out_of_scope_error"
        ),
    )
    baseline_status: str = Field(
        default="fail",
        description="Baseline quality status: fail/weak/pass",
    )
    optimization_action: str = Field(
        default="",
        description="Description of optimization applied",
    )
    after_status: str = Field(
        default="pending",
        description="Status after optimization: pending/pass/partial/fail",
    )
    notes: str = Field(
        default="",
        description="Additional notes or context",
    )


# ---------------------------------------------------------------------------
# Constants for validation
# ---------------------------------------------------------------------------

VALID_SCENARIOS = {s.value for s in Scenario}
VALID_FAILURE_TYPES = {f.value for f in FailureType}
VALID_ROUTES = {"logistics_tool", "rag_knowledge_base", "fallback"}
VALID_INTENTS = {"logistics", "aftersale", "trace", "other"}
VALID_DETAIL_INTENTS = {
    "logistics_status", "logistics_policy", "customs", "return", "refund",
    "exchange", "address", "order", "payment", "package", "coupon",
    "trace", "unknown",
}
VALID_BASELINE_STATUSES = {"fail", "weak", "pass"}
VALID_AFTER_STATUSES = {"pending", "pass", "partial", "fail"}


def validate_bad_case(case: BadCase) -> list[str]:
    """Validate a bad case and return list of validation errors.

    Args:
        case: BadCase instance to validate.

    Returns:
        List of validation error messages. Empty if valid.
    """
    errors: list[str] = []

    if case.scenario not in VALID_SCENARIOS:
        errors.append(
            f"Invalid scenario '{case.scenario}'. "
            f"Must be one of: {sorted(VALID_SCENARIOS)}"
        )

    if case.expected_route not in VALID_ROUTES:
        errors.append(
            f"Invalid expected_route '{case.expected_route}'. "
            f"Must be one of: {sorted(VALID_ROUTES)}"
        )

    if case.expected_intent not in VALID_INTENTS:
        errors.append(
            f"Invalid expected_intent '{case.expected_intent}'. "
            f"Must be one of: {sorted(VALID_INTENTS)}"
        )

    if (
        case.expected_detail_intent
        and case.expected_detail_intent not in VALID_DETAIL_INTENTS
    ):
        errors.append(
            f"Invalid expected_detail_intent '{case.expected_detail_intent}'. "
            f"Must be one of: {sorted(VALID_DETAIL_INTENTS)}"
        )

    for ft in case.failure_type:
        if ft not in VALID_FAILURE_TYPES:
            errors.append(
                f"Invalid failure_type '{ft}'. "
                f"Must be one of: {sorted(VALID_FAILURE_TYPES)}"
            )

    if case.baseline_status not in VALID_BASELINE_STATUSES:
        errors.append(
            f"Invalid baseline_status '{case.baseline_status}'. "
            f"Must be one of: {sorted(VALID_BASELINE_STATUSES)}"
        )

    if case.after_status not in VALID_AFTER_STATUSES:
        errors.append(
            f"Invalid after_status '{case.after_status}'. "
            f"Must be one of: {sorted(VALID_AFTER_STATUSES)}"
        )

    return errors
