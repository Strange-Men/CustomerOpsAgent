# Real Mimo LLM Smoke Report

## 1. Smoke Info

| Item | Value |
|------|-------|
| Date | 2026-06-26 |
| Version | v1.4.1-real-mimo |
| Render Backend | https://customeropsagent.onrender.com |
| Vercel Frontend | https://customer-ops-agent.vercel.app/ |
| Profile tested | `mimo` |
| Comparison profile | `mock` |

## 2. Environment Variables (names only, no values)

The following env vars are configured in Render backend:

| Variable | Purpose |
|----------|---------|
| `CUSTOMEROPS_LLM_MIMO_BASE_URL` | Mimo API base URL |
| `CUSTOMEROPS_LLM_MIMO_API_KEY` | Mimo API key |
| `CUSTOMEROPS_LLM_MIMO_MODEL` | Mimo model name |
| `CUSTOMEROPS_LLM_TIMEOUT_SECONDS` | Request timeout |
| `CUSTOMEROPS_ALLOWED_ORIGINS` | CORS allowed origins |

**Note:** No real API keys are stored in code, docs, frontend, or Git history. Real key is only in Render backend env vars.

## 3. API Smoke Results

### 3.1 Single Query Test (Mimo profile)

**Query:** "退款多久到账"

| Field | Value |
|-------|-------|
| intent | `aftersale` |
| detail_intent | `refund` |
| route | `rag_knowledge_base` |
| answer_source | **`real_llm`** ✅ |
| llm_profile | `mimo` |
| llm_provider | `openai_compatible` |
| llm_model | **`mimo-v2.5-pro`** ✅ |
| fallback_triggered | `false` |
| citations | 5 |
| retrieved_doc_ids | 5 |

**Result:** Mimo 真实 API 调用成功，返回了由 mimo-v2.5-pro 生成的回答。

### 3.2 Multi-Scenario Tests (Mimo profile)

| Query | Intent | Route | Answer Source | llm_model | Fallback | Citations |
|-------|--------|-------|---------------|-----------|----------|-----------|
| 清关延迟一般是什么原因？ | aftersale/customs | rag_knowledge_base | **real_llm** | mimo-v2.5-pro | No | 5 |
| 退款多久到账 | aftersale/refund | rag_knowledge_base | **real_llm** | mimo-v2.5-pro | No | 5 |
| 支付失败怎么办 | aftersale/payment | rag_knowledge_base | **real_llm** | mimo-v2.5-pro | No | 5 |
| 我的订单123456到哪了 | logistics/logistics_status | logistics_tool | **real_llm** | mimo-v2.5-pro | No | 0 |
| 你能帮我写论文吗 | other/unknown | fallback | mock | null | Yes | 0 |

**Key observations:**
- 所有业务查询均成功调用真实 Mimo LLM（answer_source=real_llm）。
- `llm_model` 正确显示 `mimo-v2.5-pro`。
- 超出范围的查询正确拒绝，不调用真实 LLM。
- Intent 分类、RAG 检索、Mock 物流工具均正常工作。

### 3.3 Multi-Scenario Tests (Mock profile)

| Query | Intent | Route | Answer Source | llm_model | Fallback | Citations |
|-------|--------|-------|---------------|-----------|----------|-----------|
| 清关延迟一般是什么原因？ | aftersale/customs | rag_knowledge_base | mock | null | No | 5 |
| 退款多久到账 | aftersale/refund | rag_knowledge_base | mock | null | No | 5 |
| 支付失败怎么办 | aftersale/payment | rag_knowledge_base | mock | null | No | 5 |

Mock profile 仍然正常工作。

## 4. Mock vs Mimo Comparison

### Query 1: "清关延迟一般是什么原因？"

| Aspect | Mock | Mimo |
|--------|------|------|
| answer_source | `mock` | **`real_llm`** |
| llm_model | null | **`mimo-v2.5-pro`** |
| Intent/route | customs / rag | customs / rag |
| Citations | 5 | 5 |
| Naturalness | Template-based, structured | More natural, conversational |
| Customer tone | Adequate | Better, more like real customer service |

### Query 2: "退款多久到账"

| Aspect | Mock | Mimo |
|--------|------|------|
| answer_source | `mock` | **`real_llm`** |
| llm_model | null | **`mimo-v2.5-pro`** |
| Intent/route | refund / rag | refund / rag |
| Citations | 5 | 5 |
| Naturalness | Template-based | More natural, organized |

### Query 3: "支付失败怎么办"

| Aspect | Mock | Mimo |
|--------|------|------|
| answer_source | `mock` | **`real_llm`** |
| llm_model | null | **`mimo-v2.5-pro`** |
| Intent/route | payment / rag | payment / rag |
| Citations | 5 | 5 |
| Naturalness | Template-based | More natural, structured with numbered steps |

**Conclusion:** Mimo 真实 LLM 成功返回了比 Mock 更自然、更像真实客服的回答。回答组织了依据，使用了客服口吻，并正确引用了知识库文档。

## 5. Frontend Smoke

| Check | Result |
|-------|--------|
| Page accessible | ✅ HTTP 200 |
| Model selector has Mimo | ✅ (verified in ModelSelector.tsx) |
| LLMProfile type includes "mimo" | ✅ (verified in types.ts) |
| RELEASE_TAG updated | ✅ "v1.4.1-real-mimo" |
| Backend URL configured | ✅ `https://customeropsagent.onrender.com` |
| llm_profile sent to backend | ✅ Only public profile name, no API key |
| No API key in frontend code | ✅ Verified |

## 6. Security Check

| Check | Result |
|-------|--------|
| API key in response body | ✅ Not found |
| API key in frontend code | ✅ Not found |
| API key in docs/README | ✅ Not found |
| .env committed to Git | ✅ Not committed (gitignore verified) |
| mystudy/ committed | ✅ Not committed |
| .agents/ committed | ✅ Not committed |

## 7. Test & Build Results

| Check | Result |
|-------|--------|
| pytest (agent_api + llm_adapter) | ✅ 44 passed |
| pytest (full suite) | ✅ 293 passed in 1.86s |
| ruff check | ✅ All checks passed |
| frontend build | ✅ Built in 217ms |

## 8. Technical Notes

1. **Windows curl encoding issue** — curl on Windows corrupts Chinese characters in JSON `-d` parameter. Use file-based input (`-d @file.json`) or Python urllib for Chinese query testing.

2. **Fallback route does not call real LLM** — When intent is classified as "other" (out-of-scope), the workflow goes to the fallback route which directly returns mock without attempting real LLM. This is by design: out-of-scope queries should be rejected, not answered by LLM.

3. **Intent classification** — The rule-based intent recognizer correctly classifies business queries (customs, refund, payment, logistics) and rejects out-of-scope queries (paper writing).

## 9. Conclusion

**Status: PASS** ✅

| Criterion | Result |
|-----------|--------|
| Render deployed and accessible | ✅ PASS |
| Mimo env vars read by backend | ✅ PASS |
| Mimo API actually called | ✅ PASS |
| Mimo API returned valid response | ✅ PASS |
| answer_source = real_llm | ✅ PASS |
| llm_model = mimo-v2.5-pro | ✅ PASS |
| Frontend Mimo selector works | ✅ PASS |
| Mock profile still works | ✅ PASS |
| Fallback on out-of-scope works | ✅ PASS |
| No API key leakage | ✅ PASS |
| pytest / ruff / build | ✅ PASS |

**Tag decision:** `v1.4.1-real-mimo` tag **created** because all criteria passed.

**What was verified:**
- 真实 Mimo LLM profile 通过 Render 后端环境变量配置成功
- `answer_source=real_llm` 确认真实 API 调用成功
- `llm_model=mimo-v2.5-pro` 确认模型名正确返回
- 回答比 Mock 更自然，有客服口吻，组织了依据
- 前端仅传 `llm_profile`，不接触任何密钥
- 模型切换与密钥安全解耦
