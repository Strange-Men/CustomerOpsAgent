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

The primary readers are technical reviewers evaluating the Agent architecture, AI application developers studying RAG + workflow patterns, and project visitors who want to try the demo quickly.

## Demo Links

- Frontend Demo: https://customer-ops-agent.vercel.app/
- Backend API: https://customeropsagent.onrender.com
- API Docs: https://customeropsagent.onrender.com/docs

Online smoke verified (M7). Render free instances may cold start — first visit may need 30–90 seconds.

## Highlights

- RAG retrieval with citations and `retrieved_doc_ids`.
- Agent Workflow with intent, detail intent, routing, and fallback.
- Safe model selector: the frontend sends only `llm_profile`, never API keys.
- Mock-first demo: the full flow can run without real model keys.
- Split frontend/backend stack: FastAPI + React/Vite.
- Deployable demo links: Render backend + Vercel frontend.
- Evaluation loop: retrieval eval, answer eval, pytest, and ruff.

## Background

Cross-border customer support often involves customs delays, refunds, logistics lookup, package exceptions, and policy questions. These requests usually require intent detection, policy evidence, optional order context, and an explainable final answer.

A plain chatbot can easily become untraceable free text: users cannot see the evidence, and developers cannot easily explain why the system selected RAG, a tool route, or fallback. This project therefore focuses on a demoable, explainable, and evaluable Agent workflow instead of presenting itself as a real business system.

## Goal

Build a demo customer support Agent that helps visitors understand the end-to-end decision flow within 1 minute, with four task types:

- Business task: cover core support scenarios such as customs delays, refund timelines, and logistics questions.
- Technical task: build an Agent Workflow with RAG retrieval, intent routing, tool usage, and fallback.
- Experience task: let the frontend display answer, route, intent, citations, `retrieved_doc_ids`, and `answer_source`.
- Constraint task: never store, input, or send real model keys from the frontend; keep the full mock flow runnable without real keys.

The key questions are:

- How a user question enters the Agent.
- How the system routes to RAG, tool, or fallback.
- How answers carry citations, metadata, and `answer_source`.
- How model selection works without exposing keys.

## Implementation

The project follows a “core flow → core capabilities → safe adapter → frontend display → deployment verification” path:

- Core flow: FastAPI exposes `/api/agent/chat`; the API wraps the workflow without duplicating Agent logic.
- Intent and routing: the workflow handles `intent`, `detail_intent`, and `route`, choosing RAG, mock logistics, or fallback.
- RAG evidence chain: retrieval returns citations and `retrieved_doc_ids`, addressing the “answer without evidence” problem.
- Tool simulation: the mock logistics tool keeps the tool route demonstrable without connecting to a real logistics API.
- Model adapter: the LLM Adapter defaults to mock, optionally supports OpenAI-compatible real LLMs, and falls back to mock when real config is missing.
- Safe selection: the frontend sends only `llm_profile`; the backend restricts profiles to `mock`, `deepseek`, `doubao`, and `mimo`.
- Frontend display: React + Vite + TypeScript + Tailwind show Q&A, model profile, fallback, and metadata.
- Deployment: backend on Render, frontend on Vercel; online smoke verified (M7).

## Results

- Engineering quality: backend tests 254 passed, Ruff All checks passed, and frontend build passed.
- Retrieval result: Retrieval Eval 20 cases, Recall@5 90%, MRR 0.785. Recall@5 measures whether expected documents appear in the top-5 results, while MRR indicates how early relevant documents appear.
- Answer result: Answer Eval 122 cases, citation hit rate 95.90%, pass rate 60.66%, fallback rate 0.82%. v1.3.0 improved citation hit rate by +12.29pp and pass rate by +13.94pp over baseline.
- Bad Case Bank: 131 structured bad cases across 11 scenarios (customs/refund/logistics/payment/order/package/return/exchange/address/coupon/out_of_scope). Bad case eval structural pass rate 97.71%, citation coverage 97.54%.
- Safety and demoability: local smoke passed for mock, deepseek fallback, and invalid profile 422; the full flow can run without real model keys.
- Real Mimo verification: Real Mimo LLM profile verified via Render backend env vars. Real key stored only in Render; frontend sends only `llm_profile`, no key exposure. answer_source=real_llm, llm_model=mimo-v2.5-pro, answers more natural than Mock.
- Access: Render + Vercel demo links available; online smoke verified (M7).

Reader value:

- For developers: a reusable FastAPI + RAG + workflow + adapter structure.
- For reviewers: observable route, intent, citations, `answer_source`, and evaluation metrics.
- For visitors: a direct frontend demo of Agent Q&A and fallback behavior.

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
        ├── doubao profile
        └── mimo profile
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

- `llm_profile` options: `mock`, `deepseek`, `doubao`, `mimo`.
- If real model env vars are not configured, `deepseek`, `doubao`, and `mimo` fall back to mock.
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
- answer eval: 122 cases, citation hit rate 95.90%, pass rate 60.66%, fallback rate 0.82%
- bad case eval: 131 cases, pass rate 97.71%, citation coverage 97.54%, covering 11 scenarios

Metric notes:

- Recall@5: whether the expected document appears in the top-5 retrieved documents.
- MRR: mean reciprocal rank of the first matching document, used for ranking quality.
- citation hit rate: whether cited documents match expected evidence.
- answer pass rate: the pass rate under the current answer eval rules, used as the improvement baseline.

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

- Backend: v1.3.0-quality.
- Frontend: M7 complete, online smoke verified.
- Release tag: v1.2.0-demo (preserved), v1.3.0-quality (pending verification).

Roadmap (completed):

- M0–M6: RAG + Eval + Agent Workflow + API + LLM Adapter.
- Frontend M1–M6.5: React scaffold → single-column chat → API integration → responsive → long answer collapse.
- Frontend M7: online smoke, final docs, release checklist, tag.

Optional next:

- zh-CN / en-US language toggle.
- Real Logistics Adapter.
