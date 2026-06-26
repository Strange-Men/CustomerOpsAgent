# Real Mimo LLM Smoke Report

## 1. Smoke Info

| Item | Value |
|------|-------|
| Date | 2026-06-26 |
| Render Backend | https://customeropsagent.onrender.com |
| Vercel Frontend | https://customer-ops-agent.vercel.app/ |
| Profile tested | `mimo` |
| Comparison profile | `mock` |

## 2. Environment Variables (names only, no values)

The following env vars are expected in Render backend:

| Variable | Purpose |
|----------|---------|
| `CUSTOMEROPS_LLM_MIMO_BASE_URL` | Mimo API base URL |
| `CUSTOMEROPS_LLM_MIMO_API_KEY` | Mimo API key |
| `CUSTOMEROPS_LLM_MIMO_MODEL` | Mimo model name |
| `CUSTOMEROPS_LLM_TIMEOUT_SECONDS` | Request timeout |

**Note:** No real API keys are stored in code, docs, frontend, or Git history.

## 3. API Smoke Results

### 3.1 Single Query Test (Mimo profile)

**Query:** "清关延迟一般是什么原因？请用客服口吻回答，并说明依据。"

| Field | Value |
|-------|-------|
| intent | `aftersale` |
| detail_intent | `customs` |
| route | `rag_knowledge_base` |
| answer_source | `real_llm_fallback_mock` |
| llm_profile | `mimo` |
| llm_provider | `openai_compatible` |
| llm_model | `None` |
| fallback_triggered | `false` |
| citations | 5 |
| retrieved_doc_ids | 5 |

**Interpretation:**
- The real Mimo LLM adapter was **actually invoked** (not skipped).
- `answer_source=real_llm_fallback_mock` means the API call was attempted but failed, so the system fell back to the mock answer template.
- `llm_provider=openai_compatible` confirms the adapter was created and the HTTP request was made.
- `llm_model=None` suggests the `CUSTOMEROPS_LLM_MIMO_MODEL` env var may not be set on Render, or the API error prevented model info from being returned.

### 3.2 Multi-Scenario Tests (Mimo profile)

| Query | Intent | Route | Answer Source | Fallback | Citations |
|-------|--------|-------|---------------|----------|-----------|
| 清关延迟一般是什么原因？ | aftersale/customs | rag_knowledge_base | real_llm_fallback_mock | No | 5 |
| 退款多久到账？ | aftersale/refund | rag_knowledge_base | real_llm_fallback_mock | No | 5 |
| 我的订单123456到哪了？ | logistics/logistics_status | logistics_tool | real_llm_fallback_mock | No | 0 |
| 支付失败怎么办？ | aftersale/payment | rag_knowledge_base | real_llm_fallback_mock | No | 5 |
| 你能帮我写论文吗？ | other/unknown | fallback | mock | Yes | 0 |

**Key observations:**
- All business queries correctly routed to RAG or logistics tool.
- All business queries attempted the real Mimo LLM (answer_source=real_llm_fallback_mock).
- Out-of-scope query correctly rejected without attempting real LLM.
- Intent classification, RAG retrieval, and mock logistics tool all work correctly.

### 3.3 Multi-Scenario Tests (Mock profile)

| Query | Intent | Route | Answer Source | Fallback | Citations |
|-------|--------|-------|---------------|----------|-----------|
| 清关延迟一般是什么原因？ | aftersale/customs | rag_knowledge_base | mock | No | 5 |
| 退款多久到账？ | aftersale/refund | rag_knowledge_base | mock | No | 5 |
| 支付失败怎么办？ | aftersale/payment | rag_knowledge_base | mock | No | 5 |

## 4. Mock vs Mimo Comparison

### Query 1: "清关延迟一般是什么原因？"

| Aspect | Mock | Mimo |
|--------|------|------|
| answer_source | `mock` | `real_llm_fallback_mock` |
| Intent/route | customs / rag | customs / rag |
| Citations | 5 | 5 |
| Naturalness | Template-based, structured | Same (fallback to mock) |
| Customer tone | Adequate | Same (fallback to mock) |

### Query 2: "退款多久到账？"

| Aspect | Mock | Mimo |
|--------|------|------|
| answer_source | `mock` | `real_llm_fallback_mock` |
| Intent/route | refund / rag | refund / rag |
| Citations | 5 | 5 |
| Naturalness | Template-based | Same (fallback to mock) |

### Query 3: "支付失败怎么办？"

| Aspect | Mock | Mimo |
|--------|------|------|
| answer_source | `mock` | `real_llm_fallback_mock` |
| Intent/route | payment / rag | payment / rag |
| Citations | 5 | 5 |
| Naturalness | Template-based | Same (fallback to mock) |

**Conclusion:** Since Mimo API calls failed and fell back to mock, the answer quality is identical. The Mimo integration infrastructure is correct, but the actual LLM response was not obtained.

## 5. Frontend Smoke

| Check | Result |
|-------|--------|
| Page accessible | ✅ HTTP 200 (via Python urllib) |
| Page title | ✅ "CustomerOpsAgent｜跨境电商客服 Agent" |
| Model selector has Mimo | ✅ (verified in ModelSelector.tsx) |
| Backend URL configured | ✅ `https://customeropsagent.onrender.com` |
| llm_profile sent to backend | ✅ Only public profile name, no API key |
| answer_source=real_llm_fallback_mock handled | ✅ Shows "真实模型不可用，已降级 Mock" |
| No API key in frontend code | ✅ Verified |

**Note:** curl on Windows had IPv6 timeout issues; Python urllib works correctly.

## 6. Security Check

| Check | Result |
|-------|--------|
| API key in response body | ✅ Not found |
| API key in frontend code | ✅ Not found |
| API key in docs/README | ✅ Not found |
| .env committed to Git | ✅ Not committed (gitignore verified) |
| mystudy/ committed | ✅ Not committed (git/info/exclude) |
| .agents/ committed | ✅ Not committed (git/info/exclude) |

## 7. Test & Build Results

| Check | Result |
|-------|--------|
| pytest (full suite) | ✅ 293 passed in 2.87s |
| ruff check | ✅ All checks passed |
| frontend build | ✅ Built in 260ms |

## 8. Known Limitations

1. **Mimo API call failed** — The real LLM was attempted but the API returned an error, causing fallback to mock answers. Root cause is likely one of:
   - `CUSTOMEROPS_LLM_MIMO_BASE_URL` format mismatch (e.g., needs `/v1` suffix)
   - `CUSTOMEROPS_LLM_MIMO_API_KEY` invalid or expired
   - `CUSTOMEROPS_LLM_MIMO_MODEL` not set or incorrect model name
   - Mimo API endpoint format not fully OpenAI-compatible

2. **`llm_model=None`** — The model field is empty, suggesting the model env var may not be configured on Render.

3. **curl encoding on Windows** — curl corrupts Chinese characters in JSON on Windows. Use Python urllib for Chinese query testing.

## 9. Diagnosis: Why Mimo Fallback to Mock

The workflow code (`workflow.py:56-65`) shows:
```python
config = load_llm_config_for_profile(llm_profile)
if not config.is_real_mode:
    mock_response.answer_source = "mock"
    return mock_response
```

Since `answer_source=real_llm_fallback_mock` (not `mock`), the config **did** resolve to `mode="real"` and `is_config_complete=True`. This means:
- ✅ `CUSTOMEROPS_LLM_MIMO_BASE_URL` is set
- ✅ `CUSTOMEROPS_LLM_MIMO_API_KEY` is set
- ⚠️ `CUSTOMEROPS_LLM_MIMO_MODEL` may or may not be set (llm_model=None in response)

The adapter was created and the HTTP request was made to `{base_url}/chat/completions`. The failure is at the API call level (timeout, HTTP error, or response format mismatch).

**Recommended next steps for the user:**
1. Check Render logs for the specific error message (look for "LLM request failed" or "LLM API returned HTTP" warnings)
2. Verify `CUSTOMEROPS_LLM_MIMO_BASE_URL` ends with the correct path (e.g., `/v1`)
3. Verify `CUSTOMEROPS_LLM_MIMO_API_KEY` is valid and not expired
4. Set `CUSTOMEROPS_LLM_MIMO_MODEL` to the correct model name
5. Test the Mimo API endpoint directly with curl to verify it accepts OpenAI-compatible requests

## 10. Conclusion

**Status: PARTIAL PASS**

| Criterion | Result |
|-----------|--------|
| Render deployed and accessible | ✅ PASS |
| Mimo env vars read by backend | ✅ PASS (config resolved to real mode) |
| Mimo API actually called | ✅ PASS (adapter invoked, HTTP request made) |
| Mimo API returned valid response | ❌ FAIL (fell back to mock) |
| answer_source reflects real LLM | ⚠️ PARTIAL (`real_llm_fallback_mock`, not `real_llm`) |
| llm_model shows Mimo model | ❌ FAIL (None) |
| Frontend Mimo selector works | ✅ PASS |
| Mock profile still works | ✅ PASS |
| Fallback on Mimo failure works | ✅ PASS |
| No API key leakage | ✅ PASS |
| pytest / ruff / build | ✅ PASS |

**Tag decision:** `v1.4.1-real-mimo` tag is **NOT created** because the real Mimo LLM did not return a valid response. The infrastructure is correct and the API was actually called, but the call failed at the API level.

**What worked:**
- The full pipeline (intent → RAG → prompt → adapter → response) executed correctly
- The Mimo profile resolved to real mode and attempted the actual API call
- Fallback to mock worked seamlessly when the API failed
- No secrets leaked anywhere

**What needs fixing:**
- Mimo API configuration on Render (likely base_url format, API key, or model name)
- Possible need for a dedicated Mimo adapter if the API is not fully OpenAI-compatible
