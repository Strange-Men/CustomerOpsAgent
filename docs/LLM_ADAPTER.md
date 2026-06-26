# LLM Adapter

## 1. Scope

This document describes the **optional** real LLM adapter for CustomerOpsAgent.

- **Default behavior**: The system uses a mock answer generator (template-based, no real LLM calls).
- **Optional behavior**: When explicitly configured via environment variables, the system can call a real LLM API for answer generation.
- **No API key = no real LLM**: If environment variables are not set, the system runs normally with mock answers. No errors, no degradation.
- **No real logistics API**: This adapter only handles text generation. It does not connect to logistics tracking or order systems.
- **No production deployment**: This is a demo/development feature, not production-grade.

## 2. Modes

| Mode | Description | Default |
|------|-------------|---------|
| `mock` | Template-based answers, no external API calls | ✅ Yes |
| `real` | Calls a real LLM API (requires configuration) | No |

## 3. Environment Variables

### Profile-Based Configuration (M4+)

The frontend sends only a public `llm_profile` name (mock / deepseek / doubao / mimo). The backend resolves it to the correct env vars.

| Variable | Description | Default |
|----------|-------------|---------|
| `CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL` | DeepSeek API base URL | None |
| `CUSTOMEROPS_LLM_DEEPSEEK_API_KEY` | DeepSeek API key | None |
| `CUSTOMEROPS_LLM_DEEPSEEK_MODEL` | DeepSeek model name | None |
| `CUSTOMEROPS_LLM_DOUBAO_BASE_URL` | Doubao API base URL | None |
| `CUSTOMEROPS_LLM_DOUBAO_API_KEY` | Doubao API key | None |
| `CUSTOMEROPS_LLM_DOUBAO_MODEL` | Doubao model name | None |
| `CUSTOMEROPS_LLM_MIMO_BASE_URL` | Mimo API base URL | None |
| `CUSTOMEROPS_LLM_MIMO_API_KEY` | Mimo API key | None |
| `CUSTOMEROPS_LLM_MIMO_MODEL` | Mimo model name | None |
| `CUSTOMEROPS_LLM_TIMEOUT_SECONDS` | Request timeout in seconds | `20` |
| `CUSTOMEROPS_ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | localhost + Vercel |

### Legacy Global Configuration (still supported)

| Variable | Description | Default |
|----------|-------------|---------|
| `CUSTOMEROPS_LLM_MODE` | `mock` or `real` | `mock` |
| `CUSTOMEROPS_LLM_PROVIDER` | LLM provider (currently supports `openai_compatible`) | `openai_compatible` |
| `CUSTOMEROPS_LLM_BASE_URL` | API base URL | None |
| `CUSTOMEROPS_LLM_API_KEY` | API key (read from env only, never stored in code) | None |
| `CUSTOMEROPS_LLM_MODEL` | Model name | None |

### Example Configuration (Render Environment Variables)

```
CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
CUSTOMEROPS_LLM_DEEPSEEK_API_KEY=<your-key>
CUSTOMEROPS_LLM_DEEPSEEK_MODEL=deepseek-chat
CUSTOMEROPS_LLM_DOUBAO_BASE_URL=<your-doubao-base-url>
CUSTOMEROPS_LLM_DOUBAO_API_KEY=<your-key>
CUSTOMEROPS_LLM_DOUBAO_MODEL=<your-model>
CUSTOMEROPS_LLM_MIMO_BASE_URL=<your-mimo-base-url>
CUSTOMEROPS_LLM_MIMO_API_KEY=<your-key>
CUSTOMEROPS_LLM_MIMO_MODEL=<your-model>
```

> **Note:** These are set in Render backend environment variables only. The frontend never sees these keys.

## 4. Safety

- **API key is never stored in code** — read from environment variables only.
- **API key is never logged** — the config loader logs whether the key is "set" or "missing", but never the key value.
- **API key is never in prompts** — the LLM prompt contains only user query, intent, evidence, and safety rules.
- **API key is never in error messages** — HTTP errors are sanitized to remove any potential key leakage.
- **Tests do not call real APIs** — all tests use monkeypatch and fake HTTP clients.

## 5. Fallback Behavior

The system has multiple layers of fallback to ensure it always works:

| Scenario | Behavior |
|----------|----------|
| `llm_profile=mock` or no profile | Uses mock adapter (default) |
| `llm_profile=deepseek` but env vars missing | Falls back to mock, `llm_profile=deepseek` preserved |
| `llm_profile=doubao` but env vars missing | Falls back to mock, `llm_profile=doubao` preserved |
| `llm_profile=mimo` but env vars missing | Falls back to mock, `llm_profile=mimo` preserved |
| Real LLM API returns error (timeout, HTTP error, network error) | Falls back to mock answer, marks `answer_source=real_llm_fallback_mock` |
| Unknown profile name | Returns 422 error |
| No env vars set (legacy) | Uses mock adapter (default) |

When fallback occurs, the response includes:
- `llm_profile`: The requested profile (e.g., `"deepseek"`)
- `answer_source`: Set to `"real_llm_fallback_mock"` to indicate fallback was used
- `llm_provider`: The provider that was attempted
- `llm_model`: The model that was attempted (if known)

## 6. Smoke Test

### Default Mock Smoke Test

The default mock smoke test works without any environment variables:

```bash
pytest backend/tests/test_llm_adapter.py -v
```

### API Smoke Test

```bash
# Start the server
python -m uvicorn backend.app.main:app --reload

# Test with mock profile (default)
curl -X POST http://127.0.0.1:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"user_query": "清关延迟怎么办？", "llm_profile": "mock"}'

# Test with deepseek profile (falls back to mock if not configured)
curl -X POST http://127.0.0.1:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"user_query": "清关延迟怎么办？", "llm_profile": "deepseek"}'

# Test with mimo profile (falls back to mock if not configured)
curl -X POST http://127.0.0.1:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"user_query": "清关延迟怎么办？", "llm_profile": "mimo"}'
```

The response will include `"answer_source": "mock"` and `"llm_profile": "mock"` by default.

### Optional Real LLM Smoke Test

If you have configured the environment variables (see Section 3), you can test the real LLM adapter:

1. Set the environment variables
2. Start the server: `python -m uvicorn backend.app.main:app --reload`
3. Send a test query: `curl -X POST http://127.0.0.1:8000/api/agent/chat -H "Content-Type: application/json" -d '{"user_query": "清关延迟怎么办？"}'`
4. Check the response: `answer_source` should be `"real_llm"` if successful, or `"real_llm_fallback_mock"` if the real LLM failed

## 7. Online Smoke Results (2026-06-26)

Tested on Render: https://customeropsagent.onrender.com

| Test | Profile | Result |
|------|---------|--------|
| Mock (default) | mock | ✅ answer_source=mock, llm_profile=mock |
| DeepSeek (no key) | deepseek | ✅ Falls back to mock, llm_profile=deepseek preserved |
| Doubao (no key) | doubao | ✅ Falls back to mock, llm_profile=doubao preserved |
| Mimo (no key) | mimo | ✅ Falls back to mock, llm_profile=mimo preserved |
| Invalid profile | openai | ✅ HTTP 422 |
| No key leak in response | all | ✅ No API key in any response field |

### Real Mimo Smoke (2026-06-26)

Mimo environment variables were configured on Render. The adapter was actually invoked and the HTTP request was made, but the API call failed (answer_source=real_llm_fallback_mock). See `docs/REAL_MIMO_SMOKE_REPORT.md` for details.

| Test | Profile | Result |
|------|---------|--------|
| Customs query | mimo | ⚠️ answer_source=real_llm_fallback_mock, API call failed |
| Refund query | mimo | ⚠️ answer_source=real_llm_fallback_mock, API call failed |
| Order tracking | mimo | ⚠️ answer_source=real_llm_fallback_mock, API call failed |
| Payment query | mimo | ⚠️ answer_source=real_llm_fallback_mock, API call failed |
| Out-of-scope | mimo | ✅ answer_source=mock (correctly rejected, no API call) |
| Mock still works | mock | ✅ answer_source=mock |

**Diagnosis:** The Mimo env vars are correctly read (config resolves to real mode), but the API call fails. Likely cause: base_url format, API key validity, or model name mismatch. Check Render logs for the specific error.

## 8. Limitations

- **Text generation only**: The adapter generates text responses. It does not support streaming, tool calling, or multi-turn conversation persistence.
- **Single provider**: Currently only supports OpenAI-compatible `/chat/completions` endpoints.
- **No production guarantees**: This is a demo feature. Error handling, retry logic, and rate limiting are minimal.
- **No real logistics**: The adapter does not connect to real logistics tracking or order management systems.
- **No conversation memory**: Each request is stateless. The adapter does not maintain conversation history.

## 8. Architecture

```
User Query
    ↓
Agent Workflow
    ↓
Prompt Builder (constructs prompt from query + intent + evidence)
    ↓
LLM Adapter Factory (reads config, selects adapter)
    ↓
├── MockLLMAdapter (default, template-based)
└── OpenAICompatibleAdapter (optional, calls real API)
    ↓
AgentResponse (answer + answer_source + llm_provider + llm_model)
```

The LLM adapter is a **drop-in replacement** for the mock answer generator's text generation step. It does not affect:
- Intent recognition
- Route decision
- Retrieval
- Evidence evaluation
- Fallback rules
- Citation validation
