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

| Variable | Description | Default |
|----------|-------------|---------|
| `CUSTOMEROPS_LLM_MODE` | `mock` or `real` | `mock` |
| `CUSTOMEROPS_LLM_PROVIDER` | LLM provider (currently supports `openai_compatible`) | `openai_compatible` |
| `CUSTOMEROPS_LLM_BASE_URL` | API base URL (e.g., `https://your-provider.example/v1`) | None |
| `CUSTOMEROPS_LLM_API_KEY` | API key (read from env only, never stored in code) | None |
| `CUSTOMEROPS_LLM_MODEL` | Model name (e.g., `your-model-name`) | None |
| `CUSTOMEROPS_LLM_TIMEOUT_SECONDS` | Request timeout in seconds | `20` |

### Example Configuration (PowerShell)

```powershell
$env:CUSTOMEROPS_LLM_MODE="real"
$env:CUSTOMEROPS_LLM_PROVIDER="openai_compatible"
$env:CUSTOMEROPS_LLM_BASE_URL="https://your-provider.example/v1"
$env:CUSTOMEROPS_LLM_API_KEY="your-api-key"
$env:CUSTOMEROPS_LLM_MODEL="your-model-name"
```

> **Note:** Replace placeholders with your actual values. Do not commit real API keys.

### Example Configuration (Bash)

```bash
export CUSTOMEROPS_LLM_MODE=real
export CUSTOMEROPS_LLM_PROVIDER=openai_compatible
export CUSTOMEROPS_LLM_BASE_URL=https://your-provider.example/v1
export CUSTOMEROPS_LLM_API_KEY=your-api-key
export CUSTOMEROPS_LLM_MODEL=your-model-name
```

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
| No env vars set | Uses mock adapter (default) |
| `CUSTOMEROPS_LLM_MODE=real` but missing `API_KEY` or `BASE_URL` | Falls back to mock adapter |
| Real LLM API returns error (timeout, HTTP error, network error) | Falls back to mock answer, marks `answer_source=real_llm_fallback_mock` |
| Unknown provider name | Falls back to mock adapter |

When fallback occurs, the response includes:
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

# Test the endpoint
curl -X POST http://127.0.0.1:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"user_query": "清关延迟怎么办？"}'
```

The response will include `"answer_source": "mock"` by default.

### Optional Real LLM Smoke Test

If you have configured the environment variables (see Section 3), you can test the real LLM adapter:

1. Set the environment variables
2. Start the server: `python -m uvicorn backend.app.main:app --reload`
3. Send a test query: `curl -X POST http://127.0.0.1:8000/api/agent/chat -H "Content-Type: application/json" -d '{"user_query": "清关延迟怎么办？"}'`
4. Check the response: `answer_source` should be `"real_llm"` if successful, or `"real_llm_fallback_mock"` if the real LLM failed

## 7. Limitations

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
