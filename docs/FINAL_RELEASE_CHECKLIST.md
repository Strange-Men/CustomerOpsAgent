# Final Release Checklist

**Version:** v1.0.0-demo  
**Date:** 2026-06-25  
**Status:** Demo Release Ready

---

## 1. Release Scope

**Project:** CustomerOpsAgent - Cross-border E-commerce Customer Service RAG Agent Demo

**Core Capabilities:**
- RAG knowledge base loading and chunking
- Baseline BM25 retriever
- Optimized retriever with enhanced recall
- Retrieval evaluation harness
- 122-case full evaluation dataset
- Node-based customer service agent workflow
- Mock logistics tool for order tracking simulation
- Fallback rules for edge cases
- Answer quality evaluation system
- Answer workflow optimization
- FastAPI Agent API smoke demo

**Release Type:** Demo release - functional prototype for demonstration and evaluation purposes. **Not a production system.**

---

## 2. Completed Milestones

| Milestone | Description | Status |
|-----------|-------------|--------|
| M0 | Scope / Design Lock | ✅ Completed |
| M1 | Schema + Seed Data | ✅ Completed |
| M2 | Loader + Chunker | ✅ Completed |
| M3 | Baseline Retriever | ✅ Completed |
| M4 | Retrieval Eval Harness | ✅ Completed |
| M5 | Optimized Retriever | ✅ Completed |
| M6 | Full Eval Set | ✅ Completed |
| M6.5 | Agent Workflow Design | ✅ Completed |
| M7 | Node-based Agent Workflow | ✅ Completed |
| M8 | Answer Quality Evaluation | ✅ Completed |
| M9 | Answer Workflow Optimization | ✅ Completed |
| M9.5 | Answer Quality Polish | ✅ Completed |
| M10 | Agent API Smoke Demo | ✅ Completed |
| M10.5 | Final Release Checklist | ✅ Completed |
| M11 | Optional Real LLM Adapter | ✅ Completed |

---

## 3. Verification Commands

### Run All Tests

```bash
pytest backend/tests/test_data_schema.py backend/tests/test_loader_chunker.py backend/tests/test_retriever.py backend/tests/test_retrieval_eval.py backend/tests/test_optimized_retriever.py backend/tests/test_full_eval_dataset.py backend/tests/test_agent_workflow.py backend/tests/test_answer_eval.py backend/tests/test_answer_workflow_optimization.py backend/tests/test_agent_api.py -v
```

### Run Ruff Linter

```bash
ruff check backend/app/rag/schemas.py backend/app/rag/loader.py backend/app/rag/chunker.py backend/app/rag/retriever.py backend/app/rag/optimized_retriever.py backend/app/eval/retrieval_eval.py backend/app/eval/answer_eval.py backend/app/agent backend/app/api backend/tests/test_agent_api.py backend/tests/test_agent_workflow.py backend/tests/test_answer_eval.py backend/tests/test_answer_workflow_optimization.py
```

### Run Retrieval Evaluation

`retrieval_eval.py` uses `app.*` imports, so the `backend` directory must be added to `PYTHONPATH` when running it from the repository root.

PowerShell:
```powershell
$env:PYTHONPATH="backend"; python -m app.eval.retrieval_eval
```

CMD:
```cmd
set PYTHONPATH=backend && python -m app.eval.retrieval_eval
```

Git Bash / Linux / macOS:
```bash
PYTHONPATH=backend python -m app.eval.retrieval_eval
```

### Run Answer Evaluation

```bash
python -m backend.app.eval.answer_eval
```

### Run API Smoke Demo

**Step 1: Start the server**
```bash
python -m uvicorn backend.app.main:app --reload
```

**Step 2: Test the endpoint**
```bash
curl -X POST http://127.0.0.1:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "我的包裹到哪里了？订单号是 CB20241201001"}'
```

**Expected Response:**
```json
{
  "answer": "根据订单号 CB20241201001 查询，您的包裹状态如下：...",
  "sources": ["logistics_api"],
  "confidence": 0.95,
  "tool_calls": ["logistics_tracking"]
}
```

---

## 4. Final Metrics

### Retrieval Performance (M6)

| Metric | Baseline | Optimized |
|--------|----------|-----------|
| Recall@5 | 75.41% | **98.36%** |
| MRR | - | **0.9108** |
| Failed Cases | - | **2** |

### Answer Quality (M9.5)

| Metric | Value |
|--------|-------|
| Answer Pass Rate | 46.72% |
| Fallback Rate | 13.11% |
| Citation Hit Rate | 83.61% |
| Avg Relevance | 0.7566 |
| Avg Groundedness | 0.8328 |
| Avg Completeness | 0.5464 |

### API Quality (M10)

| Metric | Value |
|--------|-------|
| Pytest | **220 passed** |
| Ruff | **All checks passed** |
| API Smoke Test | **Passed** |

---

## 5. Safety Checklist

- [x] **No real LLM API by default** - Using mock answer generator; real LLM is optional, requires explicit env config
- [x] **No real logistics API** - Using mock logistics tool
- [x] **No real order system** - Using seed data only
- [x] **No API key / app_key** - No external service credentials stored
- [x] **No eval leakage** - Evaluation expected fields not exposed to agent workflow
- [x] **Local-only study notes** - `docs/RAG_HANDS_ON_REVIEW.md` excluded from Git via `.git/info/exclude`
- [x] **No private content in public docs** - No interview Q&A, resume packaging, or study notes in tracked documents

---

## 6. Known Limitations

1. **Mock Answer Generator by Default** - Uses predefined response templates, not real LLM generation. Real LLM is optional.
2. **Optional Real LLM Adapter** - Can be enabled via env vars, defaults to mock. Not configured = not used.
3. **Mock Logistics Tool** - Simulates API responses, not connected to real logistics systems
3. **Answer Quality** - Pass rate (46.72%) indicates demo quality, not production-grade performance
4. **Rule-based Intent Recognition** - May have edge cases with complex or ambiguous queries
5. **No User Session Persistence** - Each request is stateless, no conversation history maintained
6. **No Production Deployment** - Designed for local development and demo purposes only
7. **Limited Domain Coverage** - Optimized for customs and logistics queries, may not generalize to other domains

---

## 7. Release Tag

**Tag:** `v1.0.0-demo`  
**Commit:** Will be marked by Git tag after final commit  
**Annotation:** CustomerOpsAgent demo release: RAG Agent API smoke demo

---

## Checklist Summary

- [x] All milestones completed (M0-M11)
- [x] All tests passing (220 tests)
- [x] Ruff linter passing
- [x] Retrieval evaluation passing (98.36% Recall@5)
- [x] Answer evaluation completed
- [x] API smoke demo working
- [x] Safety checklist verified
- [x] Documentation complete
- [x] Release tag created
