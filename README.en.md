# CustomerOpsAgent: Cross-Border Customer Support Agent With RAG Evaluation

Chinese version: [README.md](./README.md)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?logo=typescript&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Enabled-8A2BE2)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7?logo=render&logoColor=black)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?logo=vercel&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-293_passed-0A9EDC?logo=pytest&logoColor=white)

## Project Overview

CustomerOpsAgent is an AI Agent system for cross-border e-commerce customer support. Rather than being a simple chatbot, it covers a complete engineering loop: **knowledge base construction → RAG retrieval → Agent routing → answer generation → automated evaluation → Bad Case optimization → real LLM integration → Docker delivery**.

The project builds a layered knowledge base and RAG retrieval system, optimizes recall strategies and prompt templates, and achieves Recall@5 of 90.00% on a self-built evaluation set. It designs a RAG Evaluation Harness to automatically quantify answer quality across retrieval hit rate, citation coverage, answer pass rate, fallback rate, and Bad Case structural pass rate. A total of 131 structured Bad Cases covering customs, refunds, logistics, payments, returns, and other high-frequency scenarios have been built and optimized, improving the answer pass rate from 46.72% to 60.66% — a relative improvement of about 30%.

## Live Demo

| Entry | URL |
|-------|-----|
| Frontend Demo | https://customer-ops-agent.vercel.app/ |
| Backend API | https://customeropsagent.onrender.com |
| API Docs | https://customeropsagent.onrender.com/docs |

> Render free instances may cold start — first visit may need 30–90 seconds.

## Problem and Goal

Cross-border customer support faces repetitive daily inquiries: customs delays, refund timelines, logistics tracking, payment failures, return/exchange policies. These share three characteristics:

1. **Scattered knowledge**. Policy documents, logistics rules, and refund processes are spread across different systems.
2. **Inconsistent replies**. Different agents explain the same issue differently, leading to inconsistent commitments.
3. **Hard to quantify quality**. Traditional solutions have no evaluation loop — there's no way to measure "how good is the answer" or "how much did optimization help."

A plain chatbot produces untraceable free text — users can't see evidence, and developers can't explain why the system chose RAG, a tool, or fallback. This project aims to build a **demoable, explainable, and evaluable** customer support Agent capability system.

## Architecture

```text
User
  ↓
React / Vite / TypeScript Frontend
  ↓  POST /api/agent/chat
FastAPI Backend
  ↓
Agent Workflow
  ├── Intent Recognition (11 intent categories)
  ├── RAG Retriever (BM25 + query expansion + metadata boost)
  ├── Mock Logistics Tool (simulated logistics queries)
  ├── Fallback Rules (10 fallback rules)
  ├── Answer Composer (structured templates)
  └── LLM Adapter
        ├── mock (default)
        ├── deepseek profile
        ├── doubao profile
        └── mimo profile (real LLM verified)
```

DeepSeek / Doubao / Mimo are profiles only. Keys belong in backend environment variables; the frontend never calls model services directly.

## RAG Workflow

### RAG Retrieval System

- **Knowledge Base**: 14 JSONL knowledge documents covering customs/refund/logistics/payment/returns across 12 scenarios.
- **Chunking**: Character-based splitting (max_chars=320, overlap=40) with chunk-level metadata preservation.
- **Baseline Retriever**: Self-implemented BM25 with English tokenization + CJK character-level bigram.
- **Optimized Retriever**: Cross-language synonym expansion, category/market/language inference, metadata-aware score adjustment, and doc-level diversity.

### Agent Workflow

```text
Start → Entity Extraction → Intent Recognition → Route Decision
  ↓
  ├── RAG Route: Retrieval → Evidence Check → Prompt Builder → Answer Generator → Citation Check
  ├── Logistics Route: Mock Tool → Answer Generator
  └── Fallback Route: Fallback Rules → Fallback Answer
  ↓
Response (answer / route / intent / citations / answer_source / llm_model)
```

The workflow covers 11 intent categories (customs / refund / logistics_status / logistics_policy / return / exchange / address / order / payment / package / coupon) with rule-driven disambiguation for multi-intent conflicts.

## Evaluation Results

### Three-Layer Evaluation System

| Layer | Tool | Metrics |
|-------|------|---------|
| Retrieval Eval | `retrieval_eval.py` | Recall@1/3/5, MRR |
| Answer Eval | `answer_eval.py` | Relevance, Groundedness, Completeness, Citation Hit Rate, Answer Pass Rate, Fallback Rate |
| Bad Case Eval | `bad_case_eval.py` | Structural Pass Rate, Citation Coverage, Fallback Rate |

### Key Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| Recall@5 | **90.00%** | Top-5 retrieval hits expected document |
| Answer Pass Rate | 46.72% → **60.66%** | Relative improvement about 30% |
| Citation Hit Rate | 83.61% → **95.90%** | +12.29pp |
| Fallback Rate | 13.11% → **0.82%** | -12.29pp |
| Bad Case Bank | **131 cases** | 11 customer support scenarios |
| Bad Case Pass | **128 / 131** | 97.71% structural pass rate |
| pytest | **293 passed** | Full backend test suite |
| ruff | **All checks passed** | Code quality |

### Optimization Path

- **v1.3.0 before (baseline)**: pass rate 46.72%, citation hit rate 83.61%, fallback rate 13.11%
- **v1.3.0 after**: pass rate 60.66%, citation hit rate 95.90%, fallback rate 0.82%
- **v1.4.0**: Built 131-case Bad Case Bank + bad_case_eval harness
- **Reports**: [docs/RAG_QUALITY_IMPROVEMENT_REPORT.md](docs/RAG_QUALITY_IMPROVEMENT_REPORT.md) · [docs/BAD_CASE_BANK_REPORT.md](docs/BAD_CASE_BANK_REPORT.md)

## Bad Case Bank

| Scenario | Count | Description |
|----------|-------|-------------|
| logistics | 15 | Shipping, timelines, tracking |
| customs | 15 | Customs delays, inspections, duties |
| package | 15 | Damage, loss, claims |
| mixed | 15 | Multi-intent compound scenarios |
| payment | 10 | Payment failures, risk control |
| coupon | 10 | Coupon usage, expiration |
| exchange | 9 | Exchange process, timelines |
| address | 9 | Address modifications |
| out_of_scope | 9 | Out-of-scope questions |
| return | 8 | Return conditions, process |
| refund | 8 | Refund timelines, status |
| order | 8 | Order cancellation, coupon refund |

## Real LLM Profile

The system supports real LLM integration via backend environment variables. Mimo profile has been verified:

- `answer_source=real_llm`, `llm_model=mimo-v2.5-pro`
- Real key stored only in Render backend env vars; frontend sends only `llm_profile`
- Falls back to mock when real model is not configured
- Report: [docs/REAL_MIMO_SMOKE_REPORT.md](docs/REAL_MIMO_SMOKE_REPORT.md)

## Docker Compose

Run both frontend and backend with Docker Compose — no manual Python/Node setup required:

```bash
docker compose build --no-cache
docker compose up -d
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:8080 |
| Backend API Docs | http://localhost:8000/docs |

Default mode uses mock profile — no real LLM key needed. Stop: `docker compose down`.

See [docs/DOCKER_RUNBOOK.md](docs/DOCKER_RUNBOOK.md) for details.

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

## Testing

```powershell
$env:PYTHONPATH="backend"
pytest -v
ruff check backend/app/rag/schemas.py backend/app/rag/loader.py backend/app/rag/chunker.py backend/app/rag/retriever.py backend/app/rag/optimized_retriever.py backend/app/eval/retrieval_eval.py backend/app/eval/answer_eval.py backend/app/eval/bad_case_eval.py backend/app/eval/bad_case_schema.py backend/app/agent backend/app/api backend/app/llm backend/tests
cd frontend
npm run build
```

Current results: pytest 293 passed, ruff All checks passed, frontend build passed, Docker Compose verified locally.

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

`llm_profile` options: mock / deepseek / doubao / mimo. Falls back to mock when real model is not configured. Do not send API keys in requests.

## Security Boundaries

- No LLM API key is stored in the frontend.
- The frontend sends only `llm_profile`; the backend restricts profiles through a whitelist.
- Missing real model configuration falls back to mock.
- No real logistics API is connected — uses mock logistics tool.
- No real order system is connected.
- `.env` is not committed to Git; real keys are configured via Render environment variables only.

## Status & Roadmap

**Current version**: v1.6.0-final-docs

| Phase | Status | Description |
|-------|--------|-------------|
| M0–M6 | ✅ | RAG + Eval + Agent Workflow + API + LLM Adapter |
| Frontend M1–M7 | ✅ | React scaffold → single-column chat → API integration → online smoke |
| v1.3.0-quality | ✅ | RAG quality optimization, pass rate +13.94pp |
| v1.4.0-badcase | ✅ | 131 Bad Case Bank + evaluation harness |
| v1.4.1-real-mimo | ✅ | Mimo real LLM profile verified |
| v1.5.0-docker | ✅ | Docker Compose local runtime |
| v1.6.0-final-docs | ✅ | Final docs and delivery summary |

Optional next:

- Expand knowledge base document scale
- Connect real logistics tool API
- Case-level before/after tracking
- Multilingual knowledge base migration
