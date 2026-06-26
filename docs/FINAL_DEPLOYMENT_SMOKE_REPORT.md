# Final Deployment Smoke Report

**Date:** 2026-06-26
**Commit:** c72e55a (Polish README and compact chat answers)
**Release Candidate:** v1.2.0-demo

## 1. Deployment URLs

| Service | URL |
|---------|-----|
| Render Backend | https://customeropsagent.onrender.com |
| Vercel Frontend | https://customer-ops-agent.vercel.app/ |
| API Docs | https://customeropsagent.onrender.com/docs |

## 2. Render Backend Smoke

### 2.1 /docs Endpoint

- **URL:** https://customeropsagent.onrender.com/docs
- **Result:** ✅ HTTP 200, FastAPI Swagger UI loads
- **OpenAPI spec:** ✅ Valid OpenAPI 3.1.0, title "CustomerOps Agent"

### 2.2 Mock Profile — Customs Query

- **Request:** `POST /api/agent/chat` with `llm_profile=mock`, `user_query="清关延迟怎么办？"`
- **Result:** ✅ HTTP 200
- **Response:**
  - `intent`: customs
  - `route`: rag_knowledge_base
  - `fallback_triggered`: false
  - `citations`: present (customs_global_delay_001, shipping_eu_standard_001, etc.)
  - `answer_source`: mock
  - `llm_profile`: mock

### 2.3 Mock Profile — Refund Query

- **Request:** `user_query="退款多久到账？"`, `llm_profile=mock`
- **Result:** ✅ HTTP 200
- **Response:** intent=refund, route=rag_knowledge_base, citations present

### 2.4 Mock Profile — Logistics with Order ID

- **Request:** `user_query="我的订单123456到哪了？"`, `order_id="123456"`, `llm_profile=mock`
- **Result:** ✅ HTTP 200
- **Response:** intent=logistics_status, route=logistics_tool, fallback=false

### 2.5 DeepSeek Fallback (No Key Configured)

- **Request:** `user_query="退款多久到账？"`, `llm_profile=deepseek`
- **Result:** ✅ HTTP 200
- **Response:**
  - `answer_source`: mock (fallback used)
  - `llm_profile`: deepseek (preserved)
  - No crash, no key leak

### 2.6 Doubao Fallback (No Key Configured)

- **Request:** `user_query="我的订单123456到哪了？"`, `order_id="123456"`, `llm_profile=doubao`
- **Result:** ✅ HTTP 200
- **Response:**
  - `answer_source`: mock (fallback used)
  - `llm_profile`: doubao (preserved)
  - No crash, no key leak

### 2.7 Invalid Profile (422)

- **Request:** `user_query="清关延迟怎么办？"`, `llm_profile=openai`
- **Result:** ✅ HTTP 422
- **Behavior:** Rejects unknown profiles, does not accept arbitrary values

### 2.8 Non-Business Query

- **Request:** `user_query="你能帮我写论文吗？"`, `llm_profile=mock`
- **Result:** ✅ HTTP 200
- **Response:** intent=unknown, route=fallback, fallback_triggered=true
- **Behavior:** Correctly triggers fallback for out-of-scope queries

### 2.9 Response Field Completeness

All required fields present in response:
- ✅ answer
- ✅ route
- ✅ intent
- ✅ detail_intent
- ✅ citations
- ✅ fallback_triggered
- ✅ fallback_reason
- ✅ confidence
- ✅ retrieved_doc_ids
- ✅ order_id
- ✅ tool_used
- ✅ answer_source
- ✅ llm_profile
- ✅ llm_provider
- ✅ llm_model

## 3. CORS Verification

- **Preflight request:** OPTIONS with Origin=https://customer-ops-agent.vercel.app
- **Result:** ✅
  - `access-control-allow-origin`: https://customer-ops-agent.vercel.app
  - `access-control-allow-methods`: POST, GET, OPTIONS
  - `access-control-allow-headers`: Accept, Accept-Language, Content-Language, Content-Type

## 4. Vercel Frontend Smoke

### 4.1 Page Accessibility

- **URL:** https://customer-ops-agent.vercel.app/
- **Result:** ✅ HTTP 200
- **Content:** Valid React SPA shell (HTML + JS + CSS assets)

### 4.2 Asset Verification

| Asset | Status |
|-------|--------|
| JS bundle | ✅ 206,627 bytes, contains api/agent/chat, mock, deepseek, doubao, collaps, citations |
| CSS bundle | ✅ Hash matches local build (B3YVSatg) |
| Favicon | ✅ Referenced in HTML |

### 4.3 Browser Smoke (Manual Verification Required)

The following tests should be verified in a browser:

1. **Mock profile — Customs query**
   - Profile: Mock
   - Question: "清关延迟怎么办？"
   - Expected: Long answer, default collapsed, expand/collapse toggle works, citations shown

2. **Mock profile — Short query**
   - Profile: Mock
   - Question: "你好"
   - Expected: Short answer, no expand button, UI stable

3. **DeepSeek profile — Fallback**
   - Profile: DeepSeek
   - Question: "退款多久到账？"
   - Expected: Falls back to mock, page doesn't crash, shows source/profile info

4. **Doubao profile — Fallback**
   - Profile: Doubao
   - Question: "我的订单123456到哪了？"
   - Expected: Falls back to mock, page doesn't crash

5. **Non-business query**
   - Profile: Mock
   - Question: "你能帮我写论文吗？"
   - Expected: Fallback/escalation answer, doesn't write essays

## 5. Known Limitations

- **Render cold start:** First request may take 30-90 seconds if service was idle
- **Mock answers only by default:** Real LLM requires backend env vars
- **No real logistics:** Logistics tool returns mock data
- **No real order system:** Order queries are simulated
- **No WebSocket/streaming:** Request-response only
- **No conversation persistence:** Each request is stateless
- **No i18n:** Single language per response (Chinese/English based on query)
- **Vercel/Render latency:** Cross-region requests may add 200-500ms

## 6. Conclusion

**Overall Status: PASS**

All automated smoke tests passed:
- Render backend: 7/7 API tests passed
- CORS: Verified
- Vercel frontend: Accessible, assets verified
- Security: No secrets found
- Profile validation: 422 for invalid profiles

**Browser smoke tests** require manual verification but the API layer is confirmed working.

**Release recommendation:** Ready for `v1.2.0-demo` tag.
