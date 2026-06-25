"""
CustomerOps Agent - Agent API Tests

Tests for the POST /api/agent/chat endpoint.
Covers customs, refund, logistics, fallback, empty query, history, and security.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ============================================================
# Customs query
# ============================================================


def test_agent_chat_customs_query():
    """Customs query returns rag_knowledge_base route with citations."""
    response = client.post(
        "/api/agent/chat",
        json={"user_query": "清关延迟怎么办？"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["route"] == "rag_knowledge_base"
    assert data["detail_intent"] == "customs"
    assert data["fallback_triggered"] is False
    assert len(data["citations"]) > 0
    assert data["answer"]


# ============================================================
# Refund query
# ============================================================


def test_agent_chat_refund_query():
    """Refund query returns rag_knowledge_base route with answer."""
    response = client.post(
        "/api/agent/chat",
        json={"user_query": "退款多久到账？"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["route"] == "rag_knowledge_base"
    assert data["detail_intent"] in ("refund", "policy")
    assert data["answer"]


# ============================================================
# Logistics query with order_id
# ============================================================


def test_agent_chat_logistics_with_order_id():
    """Logistics query with order_id uses mock logistics tool."""
    response = client.post(
        "/api/agent/chat",
        json={"user_query": "我的订单123456到哪了？", "order_id": "123456"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["route"] == "logistics_tool"
    assert data["order_id"] == "123456"
    assert data["tool_used"] == "mock_logistics_tool"


# ============================================================
# Logistics query without order_id (fallback)
# ============================================================


def test_agent_chat_logistics_without_order_id_fallback():
    """Logistics status query without order_id triggers missing_order_id fallback."""
    response = client.post(
        "/api/agent/chat",
        json={"user_query": "我的快递到哪了？"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fallback_triggered"] is True
    assert data["fallback_reason"] == "missing_order_id"


# ============================================================
# Out-of-scope fallback
# ============================================================


def test_agent_chat_out_of_scope_fallback():
    """Out-of-scope query triggers fallback."""
    response = client.post(
        "/api/agent/chat",
        json={"user_query": "你能帮我写论文吗？"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fallback_triggered"] is True


# ============================================================
# Empty query rejection
# ============================================================


def test_agent_chat_rejects_empty_query():
    """Empty user_query returns 422."""
    response = client.post(
        "/api/agent/chat",
        json={"user_query": ""},
    )
    assert response.status_code == 422


# ============================================================
# History limiting
# ============================================================


def test_agent_chat_history_limited():
    """Conversation history exceeding 5 items is accepted without error."""
    history = [f"message {i}" for i in range(10)]
    response = client.post(
        "/api/agent/chat",
        json={
            "user_query": "退款多久到账？",
            "conversation_history": history,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"]


# ============================================================
# API file does not import eval data
# ============================================================


def test_agent_api_does_not_import_eval_cases():
    """The API file must not reference eval data or ground-truth fields."""
    api_file = Path(__file__).resolve().parent.parent / "app" / "api" / "agent.py"
    content = api_file.read_text(encoding="utf-8")
    forbidden = [
        "eval_cases_seed",
        "eval_cases_full",
        "expected_doc_ids",
        "expected_keywords",
        "case_id",
    ]
    for term in forbidden:
        assert term not in content, f"API file must not contain '{term}'"


# ============================================================
# Public docs safety
# ============================================================


def test_public_docs_do_not_contain_private_interview_content():
    """Public docs must not contain interview/resume/personal study content."""
    docs_dir = Path(__file__).resolve().parent.parent.parent / "docs"
    forbidden_terms = [
        "面试讲法",
        "面试 Q&A",
        "面试题",
        "手撕",
        "复习",
        "个人学习",
        "简历包装",
        "求职话术",
        "一分钟表达",
        "面试官",
    ]
    for md_file in docs_dir.glob("*.md"):
        # Skip the local-only study notes file
        if md_file.name == "RAG_HANDS_ON_REVIEW.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        for term in forbidden_terms:
            assert term not in content, (
                f"Public doc '{md_file.name}' contains forbidden term '{term}'"
            )
