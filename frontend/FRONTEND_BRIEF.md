# CustomerOpsAgent Frontend Brief

## 1. Website Purpose

CustomerOpsAgent Frontend is a demo console for showcasing a cross-border e-commerce customer service agent. It displays agent Q&A, RAG citations, metadata, fallback behavior, and answer source information. The frontend is a read-only demonstration interface — it does not manage orders, process payments, or connect to real logistics systems.

## 2. Target Users

- Technical reviewers evaluating the agent architecture
- AI application developers learning RAG + workflow patterns
- Project visitors exploring the demo

## 3. Core Conversion Goal

A visitor should understand within 1 minute:

- This is a cross-border e-commerce customer service agent demo
- The backend supports RAG, mock logistics tool, fallback, and optional LLM adapter
- Default mode is mock — no real logistics API, no real order system
- Frontend is connected to backend API via `/api/agent/chat`
- Model selector sends only public profile names — no API keys in frontend

## 4. MVP Modules

| Module | Description |
|--------|-------------|
| Header | Project name, release tag, mock/LLM status badges |
| Left Info Panel | Project overview, capabilities, limitations |
| Chat Workspace | Real-time chat with backend API, loading/error states |
| Model Selector | Profile selector (Mock / DeepSeek / Doubao) — no key input |
| Example Prompts | Pre-defined sample questions, click to send |
| Metadata Panel | Route, intent, confidence, fallback, llm_profile, answer source |
| Citation Panel | Retrieved document citations and doc IDs |
| Status Bar | System status indicators |

## 5. Content Priority

1. User question and agent answer
2. Route / intent / answer_source
3. Citations / retrieved_doc_ids
4. Fallback / limitations
5. Capability badges

## 6. Visual Direction

**Theme:** Dark SaaS Agent Console + Pink/Purple tech aesthetic.

- **Background:** Deep black / deep blue-black / deep purple-black
- **Accent color:** Pink-purple / purple / fuchsia / violet
- **Cards:** Dark surface, thin border, rounded corners, subtle glow
- **Badges:** Pill style, semi-transparent accent backgrounds
- **Typography:** System sans-serif stack, clear hierarchy
- **Borders:** Thin, semi-transparent accent lines
- **Glow:** Very subtle box-shadow with accent color, not neon pollution

**Do NOT:**

- Use light theme
- Use heavy neon effects
- Use complex 3D or WebGL
- Use GSAP / Framer Motion in M2

## 7. Tech Stack

- Vite 8
- React 19
- TypeScript 6
- Tailwind CSS 4
- fetch — connected to backend API via `VITE_API_BASE_URL`

## 8. Boundaries

**Not implemented in this phase:**

- Authentication / login
- Multi-tenancy
- Real order management
- Real logistics tracking / maps
- Real LLM key configuration UI (keys are backend-only)
- WebSocket / streaming responses
- Language toggle (deferred to Frontend M7.5)

## Deployed Demo Links

- **Frontend Preview**: https://customer-ops-agent.vercel.app/
- **Backend API Base**: https://customeropsagent.onrender.com
- **Backend API Docs**: https://customeropsagent.onrender.com/docs

> Frontend M4 is connected to the backend API. Vercel needs `VITE_API_BASE_URL=https://customeropsagent.onrender.com` environment variable. Model selector sends only public profile names — real API keys stay in Render backend only.

## Language Strategy

**Current issue:**

- M2 static page has mixed Chinese/English content.
- Left panel project description leans English; example questions and answers are Chinese.
- This hurts display consistency.

**Plan:**

- MVP default language: Chinese (target audience is Chinese job-seeking demo).
- Future add language toggle:
  - `zh-CN`: default Chinese
  - `en-US`: English presentation
- Do NOT introduce i18n library now.
- Use local data dictionary structure for copy management first.
- Language toggle button deferred to Frontend M7.5.

**Suggested milestones:**

| Stage | Action |
|-------|--------|
| Frontend M3 | Chat UI static state, unify copy to Chinese |
| Frontend M4 | API integration, prefer Chinese responses |
| Frontend M7.5 | Language Toggle: zh-CN / en-US switch |
| Final polish | Full-page language consistency check |

**Boundaries:**

- No LLM key exposed to frontend
- No auto-translation
- No translation API calls
- No backend changes for i18n
- Frontend display copy switch only

## 9. Frontend M5 Changes

**Goal:** Simplify from three-panel debug layout to single-column chat-first demo.

**Why:** The three-column layout (InfoPanel + ChatWorkspace + MetadataPanel/CitationPanel) was too heavy for project visitors — it looked like a developer debug console, not a demo page.

**What changed:**

- Removed fixed left InfoPanel and right MetadataPanel/CitationPanel
- Single-column layout, max-width 1100px, centered
- Chat console is the primary visual focus
- Hero intro: 2-line project description above chat
- Answer details (route/intent/confidence/source/profile) shown as compact badges below the chat
- Citations in a collapsible section below the chat
- Limitations reduced to a single footer line
- Fixed duplicate answer display (MessageBubble + AnswerCard showing same text)
- Header compacted; StatusBar replaced with inline footer

**What was preserved:**

- Model selector (Mock / DeepSeek / Doubao)
- Real API call to `/api/agent/chat`
- `sendAgentMessage` only sends `llm_profile`, never keys
- Answer metadata: `answer_source`, `llm_profile`, `route`, `intent`, `confidence`
- Citations and `retrieved_doc_ids`
- Loading / error / fallback states
- Dark + pink-purple visual theme
- Mobile responsive

## 10. Acceptance Criteria for M4

- `npm run build` passes
- Frontend sends real requests to `/api/agent/chat`
- Model selector sends only public profile names (mock / deepseek / doubao)
- No API keys in frontend code or build output
- Loading / error / fallback states handled
- Metadata panel shows llm_profile, answer_source, llm_provider, llm_model
- Unconfigured profiles fall back to mock gracefully
- `mystudy/` directory not committed

## 11. Frontend M6 Changes

**Goal:** Status feedback, responsive polish, and final visual cleanup.

**Why:** M5 simplified the layout to single-column chat-first, but spacing was loose, version numbers inconsistent, and mobile needed a pass.

**What changed:**

- Reduced top whitespace: main padding-top tightened, Hero section compressed
- ChatConsole internal spacing tightened: model selector, message area, input area, example prompts
- ModelSelector compacted: removed description line, inline horizontal layout
- ChatInput reduced from 3 rows to 2, smaller buttons and help text
- AnswerDetails made lighter: compact badge row, collapsible citations limited to 3, fallback hints more concise
- AnswerCard inline badges compacted: removed answer_source duplicate
- Citations card simplified: fewer metadata fields, tighter padding
- Version numbers unified to v1.2.0-demo across constants.ts and project.ts
- Error messages made user-friendly: no stack traces, no internal details
- Loading state text: "Agent 正在分析问题…"
- Empty state: "选择示例问题，或输入跨境电商客服问题。"
- Fallback: "已触发兜底回答" with reason; profile mismatch: "该模型档案未启用或未配置，已降级 Mock"
- Header: flex-wrap for mobile, smaller padding
- Footer: lighter text, smaller font
- Mobile: 375px width no horizontal overflow

**What was preserved:**

- Model selector (Mock / DeepSeek / Doubao)
- Real API call to `/api/agent/chat`
- `sendAgentMessage` only sends `llm_profile`, never keys
- Answer metadata: `answer_source`, `llm_profile`, `route`, `intent`, `confidence`
- Citations and `retrieved_doc_ids`
- Loading / error / fallback states
- Dark + pink-purple visual theme

**Next steps:**

- M7: online smoke verification, final docs, release checklist, tag

## 12. Frontend M6.5 Changes

**Goal:** README merge commit + long answer collapse/compact badges.

**Why:** RAG long answers stretched the chat area vertically, hurting readability. README bilingual improvements from the previous round needed to be committed together.

**What changed:**

- Long answers (>280 chars) default to collapsed state with max-height 220px
- Bottom gradient fade indicates truncated content
- "展开全文 / 收起" toggle button for long answers
- Short answers show no expand button — unaffected by collapse logic
- Badge row already minimal (profile, route, confidence, fallback-only-when-triggered)
- No new dependencies, no complex animations
- README.md and README.en.md bilingual improvements committed together

**What was preserved:**

- All API calls unchanged (`/api/agent/chat`)
- Response data not truncated — only UI folding
- Citations, metadata, fallback badges all intact
- Model selector fully functional
- Mobile responsive

## 13. Frontend M7 — Online Smoke + Release

**Goal:** Online smoke verification, final docs, release checklist, tag.

**Smoke results (2026-06-26):**

- Render backend: 7/7 API tests passed (mock customs, refund, logistics, deepseek fallback, doubao fallback, invalid 422, non-business fallback)
- CORS: Verified for Vercel origin
- Vercel frontend: Page accessible, JS/CSS assets verified
- Security: No API keys in frontend or docs
- All 254 pytest tests pass, ruff passes, `npm run build` passes

**Release tag:** v1.2.0-demo

**Known limitation:** Windows curl may not encode Chinese characters correctly for API testing. Use Python urllib for Chinese queries.

## 14. Real Mimo Smoke (v1.4.1)

**Goal:** Verify real Mimo LLM profile via Render backend environment variables.

**Results (2026-06-26):**

- Mimo env vars configured on Render backend
- Frontend ModelSelector correctly includes Mimo option
- API calls with `llm_profile=mimo` reach the backend and invoke the real LLM adapter
- `answer_source=real_llm_fallback_mock` — the Mimo API was actually called but failed, falling back to mock
- `llm_provider=openai_compatible` — adapter was created and HTTP request was made
- `llm_model=None` — model env var may not be set
- Intent classification, RAG retrieval, mock logistics tool all work correctly
- Mock profile still works normally
- No API key leakage in frontend, response, or docs

**Frontend handling:** When `answer_source=real_llm_fallback_mock`, the UI shows "真实模型不可用，已降级 Mock" hint.

**Status:** Infrastructure verified correct. API configuration needs user-side verification (check Render logs for specific error). See `docs/REAL_MIMO_SMOKE_REPORT.md`.
