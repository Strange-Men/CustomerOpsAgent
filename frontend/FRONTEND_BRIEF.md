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
- API integration will be added in Frontend M4

## 4. MVP Modules

| Module | Description |
|--------|-------------|
| Header | Project name, release tag, mock/LLM status badges |
| Left Info Panel | Project overview, capabilities, limitations |
| Chat Workspace | Static message display with example prompts |
| Example Prompts | Pre-defined sample questions |
| Metadata Panel | Route, intent, confidence, fallback, answer source |
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
- fetch — deferred to Frontend M4

## 8. Boundaries

**Not implemented in this phase:**

- API integration (Frontend M4)
- Authentication / login
- Multi-tenancy
- Real order management
- Real logistics tracking / maps
- Real LLM key configuration UI
- WebSocket / streaming responses
- Deployment

## Deployed Demo Links

- **Frontend Preview**: https://customer-ops-agent.vercel.app/
- **Backend API Base**: https://customeropsagent.onrender.com
- **Backend API Docs**: https://customeropsagent.onrender.com/docs

> Frontend M2 is static. API integration will be added in Frontend M4. `VITE_API_BASE_URL` should point to the Render backend in M4: `VITE_API_BASE_URL=https://customeropsagent.onrender.com`

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

## 9. Acceptance Criteria for M2

- `npm run build` passes
- Page renders dark + pink-purple visual theme
- Three-column static layout is visible
- No API calls (no fetch, no real endpoints)
- No backend modifications
- No secrets or API keys committed
- `mystudy/` directory not committed
