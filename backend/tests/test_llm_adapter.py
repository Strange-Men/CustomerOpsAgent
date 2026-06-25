"""
CustomerOps Agent - LLM Adapter Tests

Tests for the optional real LLM adapter layer.
All tests use monkeypatch / fake clients — no real API calls are made.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.llm.config import LLMConfig, load_llm_config, load_llm_config_for_profile, ALLOWED_PROFILES
from app.llm.factory import create_llm_adapter
from app.llm.mock_adapter import MockLLMAdapter
from app.llm.openai_compatible_adapter import OpenAICompatibleAdapter
from app.llm.schemas import LLMGenerationRequest, LLMMessage

# ============================================================
# Test 1: Default LLM mode is mock
# ============================================================


def test_default_llm_mode_is_mock(monkeypatch: pytest.MonkeyPatch):
    """Without any CUSTOMEROPS_LLM_* env vars, factory returns MockLLMAdapter."""
    # Clear all relevant env vars
    for key in [
        "CUSTOMEROPS_LLM_MODE",
        "CUSTOMEROPS_LLM_PROVIDER",
        "CUSTOMEROPS_LLM_BASE_URL",
        "CUSTOMEROPS_LLM_API_KEY",
        "CUSTOMEROPS_LLM_MODEL",
        "CUSTOMEROPS_LLM_TIMEOUT_SECONDS",
    ]:
        monkeypatch.delenv(key, raising=False)

    adapter = create_llm_adapter()
    assert isinstance(adapter, MockLLMAdapter)


# ============================================================
# Test 2: Real mode missing config falls back to mock
# ============================================================


def test_real_mode_missing_config_falls_back_to_mock(monkeypatch: pytest.MonkeyPatch):
    """CUSTOMEROPS_LLM_MODE=real but missing key/base_url → factory returns mock."""
    monkeypatch.setenv("CUSTOMEROPS_LLM_MODE", "real")
    monkeypatch.delenv("CUSTOMEROPS_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("CUSTOMEROPS_LLM_API_KEY", raising=False)
    monkeypatch.delenv("CUSTOMEROPS_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("CUSTOMEROPS_LLM_MODEL", raising=False)

    adapter = create_llm_adapter()
    assert isinstance(adapter, MockLLMAdapter)


# ============================================================
# Test 3: OpenAI-compatible adapter does not leak API key
# ============================================================


def test_openai_compatible_request_building_does_not_leak_api_key(
    monkeypatch: pytest.MonkeyPatch,
):
    """The adapter sends the API key in Authorization header but never in error messages."""
    secret_key = "sk-super-secret-key-12345"
    config = LLMConfig(
        mode="real",
        provider="openai_compatible",
        base_url="https://fake-api.example.com/v1",
        api_key=secret_key,
        model="test-model",
        timeout_seconds=10,
    )

    adapter = OpenAICompatibleAdapter(config)

    # Capture the request that would be sent
    captured_request: dict = {}

    class FakeResponse:
        status_code = 500
        text = "Internal Server Error"

        def json(self):
            return {"error": "something went wrong"}

        def raise_for_status(self):
            import httpx

            raise httpx.HTTPStatusError(
                "Server error",
                request=httpx.Request("POST", "https://fake-api.example.com/v1/chat/completions"),
                response=httpx.Response(500),
            )

    class FakeClient:
        def post(self, url, json, headers, timeout):
            captured_request["url"] = url
            captured_request["headers"] = headers
            captured_request["json"] = json
            return FakeResponse()

    # Monkeypatch httpx.post
    import httpx

    def fake_post(url, json=None, headers=None, timeout=None):
        captured_request["url"] = url
        captured_request["headers"] = headers
        captured_request["json"] = json
        return FakeResponse()

    monkeypatch.setattr(httpx, "post", fake_post)

    request = LLMGenerationRequest(
        messages=[LLMMessage(role="user", content="test")],
    )

    result = adapter.generate(request)

    # Verify: Authorization header contains the key
    assert captured_request["headers"]["Authorization"] == f"Bearer {secret_key}"

    # Verify: error message does NOT contain the key
    assert result.fallback_used is True
    assert result.error_reason is not None
    assert secret_key not in result.error_reason


# ============================================================
# Test 4: Mock adapter is deterministic
# ============================================================


def test_mock_adapter_is_deterministic():
    """Mock adapter returns the same output for the same input across multiple calls."""
    adapter = MockLLMAdapter()
    request = LLMGenerationRequest(
        messages=[
            LLMMessage(role="system", content="test"),
            LLMMessage(role="user", content="退款多久到账？"),
        ],
    )

    results = [adapter.generate(request) for _ in range(5)]

    # All results should be identical
    texts = [r.text for r in results]
    assert len(set(texts)) == 1, "Mock adapter should be deterministic"
    assert all(r.provider == "mock" for r in results)
    assert all(r.is_real_llm is False for r in results)
    assert all(r.fallback_used is False for r in results)


# ============================================================
# Test 5: LLM prompt does not include eval fields
# ============================================================


def test_llm_prompt_does_not_include_eval_fields():
    """Static scan: LLM and agent source files must not contain eval ground-truth fields."""
    forbidden_terms = [
        "expected_keywords",
        "expected_doc_ids",
        "eval_cases_full",
        "case_id",
    ]

    # Scan LLM package
    llm_dir = Path(__file__).resolve().parent.parent / "app" / "llm"
    for py_file in llm_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        for term in forbidden_terms:
            assert term not in content, (
                f"LLM file '{py_file.name}' contains forbidden eval term '{term}'"
            )

    # Scan agent package (excluding test files)
    agent_dir = Path(__file__).resolve().parent.parent / "app" / "agent"
    for py_file in agent_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        for term in forbidden_terms:
            assert term not in content, (
                f"Agent file '{py_file.name}' contains forbidden eval term '{term}'"
            )


# ============================================================
# Test 6: Agent response contains answer_source
# ============================================================


def test_agent_response_contains_answer_source():
    """Default workflow returns answer_source='mock'."""
    from app.agent.workflow import run_customer_service_agent

    result = run_customer_service_agent("清关延迟怎么办？")
    assert hasattr(result, "answer_source")
    assert result.answer_source == "mock"


# ============================================================
# Test 7: Real LLM failure falls back to mock
# ============================================================


def test_real_llm_failure_falls_back_to_mock(monkeypatch: pytest.MonkeyPatch):
    """When real LLM adapter fails, workflow falls back to mock with answer_source=real_llm_fallback_mock."""
    # Set profile-specific env vars to enable real mode for deepseek
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL", "https://fake-api.example.com/v1")
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_API_KEY", "sk-fake-key")
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_MODEL", "test-model")

    # Monkeypatch httpx.post to simulate failure
    import httpx

    def fake_post(url, json=None, headers=None, timeout=None):
        raise httpx.ConnectError("Connection refused")

    monkeypatch.setattr(httpx, "post", fake_post)

    from app.agent.workflow import run_customer_service_agent

    result = run_customer_service_agent("清关延迟怎么办？", llm_profile="deepseek")

    # Should not crash, should fall back to mock
    assert result.answer_source == "real_llm_fallback_mock"
    assert result.answer  # Should have a non-empty answer from mock
    assert result.llm_profile == "deepseek"
    assert result.route == "rag_knowledge_base"


# ============================================================
# Test 8: API response includes answer_source
# ============================================================


def test_api_response_includes_answer_source():
    """POST /api/agent/chat response includes answer_source field."""
    from app.main import app

    client = TestClient(app)
    response = client.post(
        "/api/agent/chat",
        json={"user_query": "清关延迟怎么办？"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer_source" in data
    assert data["answer_source"] == "mock"
    assert "llm_provider" in data
    assert "llm_model" in data


# ============================================================
# Additional tests for completeness
# ============================================================


def test_load_llm_config_defaults(monkeypatch: pytest.MonkeyPatch):
    """load_llm_config returns safe defaults when no env vars are set."""
    for key in [
        "CUSTOMEROPS_LLM_MODE",
        "CUSTOMEROPS_LLM_PROVIDER",
        "CUSTOMEROPS_LLM_BASE_URL",
        "CUSTOMEROPS_LLM_API_KEY",
        "CUSTOMEROPS_LLM_MODEL",
        "CUSTOMEROPS_LLM_TIMEOUT_SECONDS",
    ]:
        monkeypatch.delenv(key, raising=False)

    config = load_llm_config()
    assert config.mode == "mock"
    assert config.is_real_mode is False
    assert config.is_config_complete is False


def test_load_llm_config_real_mode(monkeypatch: pytest.MonkeyPatch):
    """load_llm_config reads real mode env vars correctly."""
    monkeypatch.setenv("CUSTOMEROPS_LLM_MODE", "real")
    monkeypatch.setenv("CUSTOMEROPS_LLM_PROVIDER", "openai_compatible")
    monkeypatch.setenv("CUSTOMEROPS_LLM_BASE_URL", "https://api.example.com/v1")
    monkeypatch.setenv("CUSTOMEROPS_LLM_API_KEY", "sk-test-key")
    monkeypatch.setenv("CUSTOMEROPS_LLM_MODEL", "test-model")
    monkeypatch.setenv("CUSTOMEROPS_LLM_TIMEOUT_SECONDS", "30")

    config = load_llm_config()
    assert config.mode == "real"
    assert config.is_real_mode is True
    assert config.is_config_complete is True
    assert config.base_url == "https://api.example.com/v1"
    assert config.api_key == "sk-test-key"
    assert config.model == "test-model"
    assert config.timeout_seconds == 30


def test_factory_with_explicit_config():
    """Factory works with explicitly provided config (no env vars needed)."""
    config = LLMConfig(
        mode="mock",
        provider="openai_compatible",
        base_url=None,
        api_key=None,
        model=None,
        timeout_seconds=20,
    )
    adapter = create_llm_adapter(config)
    assert isinstance(adapter, MockLLMAdapter)


def test_factory_unknown_provider_falls_back_to_mock():
    """Unknown provider falls back to mock adapter."""
    config = LLMConfig(
        mode="real",
        provider="unknown_provider",
        base_url="https://api.example.com/v1",
        api_key="sk-test-key",
        model="test-model",
        timeout_seconds=20,
    )
    adapter = create_llm_adapter(config)
    assert isinstance(adapter, MockLLMAdapter)


def test_api_response_answer_source_in_all_routes():
    """All route types return answer_source in API response."""
    from app.main import app

    client = TestClient(app)

    # RAG route (customs)
    resp = client.post("/api/agent/chat", json={"user_query": "清关延迟怎么办？"})
    assert resp.status_code == 200
    assert resp.json()["answer_source"] == "mock"

    # Logistics route
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "我的订单123456到哪了？", "order_id": "123456"},
    )
    assert resp.status_code == 200
    assert resp.json()["answer_source"] == "mock"

    # Fallback route
    resp = client.post("/api/agent/chat", json={"user_query": "你能帮我写论文吗？"})
    assert resp.status_code == 200
    assert resp.json()["answer_source"] == "mock"


# ============================================================
# Profile-based config tests
# ============================================================


def test_profile_whitelist():
    """ALLOWED_PROFILES contains exactly mock, deepseek, doubao."""
    assert "mock" in ALLOWED_PROFILES
    assert "deepseek" in ALLOWED_PROFILES
    assert "doubao" in ALLOWED_PROFILES
    assert len(ALLOWED_PROFILES) == 3


def test_load_config_for_profile_mock():
    """load_llm_config_for_profile('mock') always returns mock config."""
    config = load_llm_config_for_profile("mock")
    assert config.mode == "mock"
    assert config.is_real_mode is False


def test_load_config_for_profile_deepseek_missing_config(monkeypatch: pytest.MonkeyPatch):
    """deepseek profile with missing env vars falls back to mock config."""
    for key in [
        "CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL",
        "CUSTOMEROPS_LLM_DEEPSEEK_API_KEY",
        "CUSTOMEROPS_LLM_DEEPSEEK_MODEL",
    ]:
        monkeypatch.delenv(key, raising=False)

    config = load_llm_config_for_profile("deepseek")
    assert config.mode == "mock"
    assert config.is_real_mode is False


def test_load_config_for_profile_doubao_missing_config(monkeypatch: pytest.MonkeyPatch):
    """doubao profile with missing env vars falls back to mock config."""
    for key in [
        "CUSTOMEROPS_LLM_DOUBAO_BASE_URL",
        "CUSTOMEROPS_LLM_DOUBAO_API_KEY",
        "CUSTOMEROPS_LLM_DOUBAO_MODEL",
    ]:
        monkeypatch.delenv(key, raising=False)

    config = load_llm_config_for_profile("doubao")
    assert config.mode == "mock"
    assert config.is_real_mode is False


def test_load_config_for_profile_deepseek_complete_config(monkeypatch: pytest.MonkeyPatch):
    """deepseek profile with complete env vars returns real config."""
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_API_KEY", "sk-fake-key")
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_MODEL", "deepseek-chat")

    config = load_llm_config_for_profile("deepseek")
    assert config.mode == "real"
    assert config.is_real_mode is True
    assert config.is_config_complete is True
    assert config.base_url == "https://api.deepseek.com/v1"
    assert config.api_key == "sk-fake-key"
    assert config.model == "deepseek-chat"


def test_load_config_for_profile_unknown_falls_back_to_mock():
    """Unknown profile name falls back to mock config."""
    config = load_llm_config_for_profile("unknown_profile")
    assert config.mode == "mock"
    assert config.is_real_mode is False


def test_load_config_for_profile_case_insensitive():
    """Profile name is case-insensitive."""
    config = load_llm_config_for_profile("Mock")
    assert config.mode == "mock"

    config = load_llm_config_for_profile("MOCK")
    assert config.mode == "mock"


def test_profile_deepseek_no_key_leak_in_config(monkeypatch: pytest.MonkeyPatch):
    """Profile config stores API key internally but never sends it to frontend."""
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_API_KEY", "sk-super-secret-12345")
    monkeypatch.setenv("CUSTOMEROPS_LLM_DEEPSEEK_MODEL", "deepseek-chat")

    config = load_llm_config_for_profile("deepseek")
    # Config stores the key (for internal use by adapter) but it is never
    # included in API responses — verified by test_api_no_key_leaked_in_response.
    assert config.api_key == "sk-super-secret-12345"


# ============================================================
# Profile-based API tests
# ============================================================


def test_api_default_request_without_profile_uses_mock():
    """POST /api/agent/chat without llm_profile defaults to mock."""
    from app.main import app

    client = TestClient(app)
    resp = client.post("/api/agent/chat", json={"user_query": "清关延迟怎么办？"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["answer_source"] == "mock"
    assert data["llm_profile"] == "mock"


def test_api_explicit_mock_profile():
    """POST /api/agent/chat with llm_profile='mock' uses mock."""
    from app.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "清关延迟怎么办？", "llm_profile": "mock"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["answer_source"] == "mock"
    assert data["llm_profile"] == "mock"


def test_api_deepseek_profile_missing_config_falls_back_to_mock(monkeypatch: pytest.MonkeyPatch):
    """llm_profile='deepseek' with no env vars falls back to mock gracefully."""
    for key in [
        "CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL",
        "CUSTOMEROPS_LLM_DEEPSEEK_API_KEY",
        "CUSTOMEROPS_LLM_DEEPSEEK_MODEL",
    ]:
        monkeypatch.delenv(key, raising=False)

    from app.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "清关延迟怎么办？", "llm_profile": "deepseek"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_profile"] == "deepseek"
    assert data["answer_source"] == "mock"  # Fallback to mock
    assert data["answer"]  # Has a non-empty answer


def test_api_doubao_profile_missing_config_falls_back_to_mock(monkeypatch: pytest.MonkeyPatch):
    """llm_profile='doubao' with no env vars falls back to mock gracefully."""
    for key in [
        "CUSTOMEROPS_LLM_DOUBAO_BASE_URL",
        "CUSTOMEROPS_LLM_DOUBAO_API_KEY",
        "CUSTOMEROPS_LLM_DOUBAO_MODEL",
    ]:
        monkeypatch.delenv(key, raising=False)

    from app.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "退款多久到账？", "llm_profile": "doubao"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_profile"] == "doubao"
    assert data["answer_source"] == "mock"


def test_api_invalid_profile_returns_422():
    """Invalid llm_profile returns 422."""
    from app.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "test", "llm_profile": "gpt-4"},
    )
    assert resp.status_code == 422


def test_api_response_includes_llm_profile():
    """Response always includes llm_profile field."""
    from app.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "清关延迟怎么办？", "llm_profile": "mock"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "llm_profile" in data
    assert data["llm_profile"] == "mock"


def test_api_no_key_leaked_in_response():
    """API response never contains API key text."""
    from app.main import app

    client = TestClient(app)
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "清关延迟怎么办？", "llm_profile": "mock"},
    )
    assert resp.status_code == 200
    data = resp.json()
    response_text = str(data)
    assert "sk-" not in response_text
    assert "api_key" not in response_text
    assert "API_KEY" not in response_text


def test_api_no_key_leaked_in_error_text(monkeypatch: pytest.MonkeyPatch):
    """Error responses never contain API key text."""
    from app.main import app

    client = TestClient(app)
    # Force an error by sending invalid profile via raw request
    resp = client.post(
        "/api/agent/chat",
        json={"user_query": "test", "llm_profile": "invalid"},
    )
    # 422 error
    assert resp.status_code == 422
    error_text = str(resp.json())
    assert "sk-" not in error_text


def test_cors_allows_localhost_origin():
    """CORS allows localhost:5173 origin."""
    from app.main import app

    client = TestClient(app)
    resp = client.options(
        "/api/agent/chat",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    # CORS preflight should return 200
    assert resp.status_code == 200


def test_cors_allows_vercel_origin():
    """CORS allows Vercel frontend origin."""
    from app.main import app

    client = TestClient(app)
    resp = client.options(
        "/api/agent/chat",
        headers={
            "Origin": "https://customer-ops-agent.vercel.app",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert resp.status_code == 200
