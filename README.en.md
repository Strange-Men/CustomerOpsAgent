# CustomerOpsAgent: Cross-Border Customer Support Agent With RAG Evaluation

Chinese version: [README.md](./README.md)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?logo=typescript&logoColor=white)
![Tailwind_CSS](https://img.shields.io/badge/Tailwind_CSS-UI-06B6D4?logo=tailwindcss&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Enabled-8A2BE2)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7?logo=render&logoColor=black)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?logo=vercel&logoColor=white)
![Mock_Default](https://img.shields.io/badge/Mock-Default-orange)

## Project Overview

CustomerOpsAgent is an AI Agent demo for cross-border e-commerce customer support. It handles common scenarios such as customs delays, refund timelines, and logistics questions with RAG retrieval, intent routing, a mock logistics tool, fallback behavior, and safe model profile selection.

The frontend is a dark pink-purple Agent Console built with React/Vite, and the backend exposes a FastAPI API. The default mode is mock, so the demo can run without real model keys; DeepSeek and Doubao are optional backend-configured profiles.

## Demo Links

- Frontend Demo: https://customer-ops-agent.vercel.app/
- Backend API: https://customeropsagent.onrender.com
- API Docs: https://customeropsagent.onrender.com/docs

Frontend API integration is complete. Online smoke should still be judged by the upcoming M4.5 verification result. Render free instances may cold start and need a short wait.

## Highlights

- RAG retrieval with citations and `retrieved_doc_ids`.
- Agent Workflow with intent, detail intent, routing, and fallback.
- Safe model selector: the frontend sends only `llm_profile`, never API keys.
- Mock-first demo: the full flow can run without real model keys.
- Split frontend/backend stack: FastAPI + React/Vite.
- Deployable demo links: Render backend + Vercel frontend.
- Evaluation loop: retrieval eval, answer eval, pytest, and ruff.

## Background

Cross-border customer support often involves customs delays, refunds, logistics lookup, and policy questions. A plain chatbot is hard to evaluate because answers may lack evidence and the routing process is invisible.

## Goal

Build a demo customer support Agent that helps visitors understand within 1 minute:

- How a user question enters the Agent.
- How the system routes to RAG, tool, or fallback.
- How answers carry citations, metadata, and `answer_source`.
- How model selection works without exposing keys.

## Implementation

- Backend API: FastAPI endpoint `/api/agent/chat`.
- RAG retrieval: knowledge base lookup with citation support.
- Workflow: `intent`, `detail_intent`, and `route` handling.
- Tool route: mock logistics lookup.
- LLM Adapter: mock default plus OpenAI-compatible real LLM option.
- Model profiles: `mock`, `deepseek`, and `doubao` through `llm_profile`.
- Frontend: React + Vite + TypeScript + Tailwind Agent Console.
- Deployment: Render backend and Vercel frontend.

## Results

- Backend tests: 254 passed.
- Ruff: All checks passed.
- Retrieval Eval: 20 cases, Recall@5 90%, MRR 0.785.
- Answer Eval: 122 cases, citation hit rate 83.61%, pass rate 46.72%.
- Local smoke: mock / deepseek fallback / invalid profile 422 passed.
- Frontend build: passed.
- Render + Vercel demo preview links are available.

The Answer Eval pass rate of 46.72% is the current baseline, shown transparently as a quality signal and improvement target.

## Architecture

```text
User
  ↓
React / Vite Frontend
  ↓  POST /api/agent/chat
FastAPI Backend
  ↓
Agent Workflow
  ├── Intent Routing
  ├── RAG Retriever
  ├── Mock Logistics Tool
  ├── Fallback Handler
  └── LLM Adapter
        ├── mock
        ├── deepseek profile
        └── doubao profile
```

DeepSeek and Doubao are profiles only. Keys belong in backend environment variables, and the frontend does not call model services directly.

## API Example

```bash
curl -X POST "https://customeropsagent.onrender.com/api/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "清关延迟怎么办？",
    "order_id": null,
    "conversation_history": [],
    "llm_profile": "mock"
  }'
```

- `llm_profile` options: `mock`, `deepseek`, `doubao`.
- If real model env vars are not configured, `deepseek` and `doubao` fall back to mock.
- Do not send API keys in requests.

## Local Development

Backend:

```powershell
cd D:\Claude_workfile\CustomerOpsAgent
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Frontend environment:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Vercel environment:

```text
VITE_API_BASE_URL=https://customeropsagent.onrender.com
```

`VITE_API_BASE_URL` is a public API base URL. DeepSeek / Doubao keys must not be placed in Vercel; LLM keys belong only in Render backend environment variables.

## Evaluation

```powershell
pytest
ruff check
cd frontend
npm run build
```

Current results:

- pytest: 254 passed
- ruff: All checks passed
- frontend build: passed
- retrieval eval baseline: 20 cases, Recall@5 90%, MRR 0.785
- answer eval baseline: 122 cases, citation hit rate 83.61%, pass rate 46.72%

## Security Boundaries

- No LLM API key is stored in the frontend.
- Users cannot input API keys in the frontend.
- The frontend sends only `llm_profile`.
- The backend restricts profiles through a whitelist.
- Missing real model configuration falls back to mock.
- No real logistics API is connected.
- No real order system is connected.
- Default mock mode can run with no key.

## Status & Roadmap

Current status:

- Backend: v1.1.0-demo + Frontend M4.
- Frontend: API integration + model profile selector complete.
- Next: M4.5 online smoke, then M5 Metadata + Citations display polish.

Roadmap:

- M4.5: online Render + Vercel smoke verification.
- M5: Metadata + Citations display polish.
- M6: fallback / error / empty state polish.
- M7: responsive and visual polish.
- M7.5: zh-CN / en-US language toggle.
- M8: final docs and release checklist.
- M9: fresh clone + deployment final verification.
