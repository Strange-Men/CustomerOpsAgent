"""RAG data schemas for knowledge base and evaluation cases."""

from pydantic import BaseModel, Field


class KnowledgeDocument(BaseModel):
    """A single knowledge base document with metadata."""

    doc_id: str = Field(..., min_length=1, description="Unique document identifier")
    title: str = Field(..., description="Document title")
    category: str = Field(
        ...,
        description="Category: logistics/customs/return/refund/exchange/payment/address/order/coupon/package",
    )
    market: str = Field(..., description="Target market: US/EU/GLOBAL")
    language: str = Field(..., description="Language code: zh/en")
    policy_type: str = Field(
        ...,
        description="Policy type: shipping/return/customs/payment/exchange/address/cancel/coupon",
    )
    priority: int = Field(..., description="Priority: 1=high, 2=medium, 3=low")
    source: str = Field(..., description="Data source identifier")
    content: str = Field(..., min_length=1, description="Document content body")


class EvalCase(BaseModel):
    """A single evaluation case with expected retrieval targets."""

    case_id: str = Field(..., min_length=1, description="Unique case identifier")
    question: str = Field(..., description="Customer question text")
    category: str = Field(..., description="Question category")
    market: str = Field(..., description="Target market: US/EU/GLOBAL")
    language: str = Field(..., description="Language code: zh/en")
    difficulty: str = Field(..., description="Difficulty: easy/medium/hard")
    expected_doc_ids: list[str] = Field(
        ..., min_length=1, description="Expected knowledge doc IDs for this question"
    )
    expected_keywords: list[str] = Field(
        ..., min_length=1, description="Keywords expected in a good answer"
    )
