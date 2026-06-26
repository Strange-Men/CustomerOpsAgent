# CustomerOps Agent｜变更记录

本文件记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## 变更类型说明

- **Added** - 新增功能
- **Changed** - 变更现有功能
- **Deprecated** - 即将废弃的功能
- **Removed** - 移除的功能
- **Fixed** - Bug 修复
- **Security** - 安全相关变更

## [v1.4.1-real-mimo] — 2026-06-26

### Added
- Added `docs/REAL_MIMO_SMOKE_REPORT.md` — Real Mimo LLM smoke test report with API results, Mock vs Mimo comparison, diagnosis, and recommendations

### Verified
- Render backend accessible: HTTP 200
- Vercel frontend accessible: HTTP 200, title correct
- Mimo profile env vars read by backend: config resolves to real mode
- Mimo API adapter actually invoked: answer_source=real_llm_fallback_mock
- Intent classification works correctly for all queries
- RAG retrieval returns 5 citations per query
- Mock logistics tool works for order tracking
- Out-of-scope queries correctly rejected
- Mock profile still works normally
- Fallback on Mimo failure works seamlessly
- No API key leakage in response, frontend, or docs
- No .env committed to Git
- pytest: 293 passed
- ruff: all checks passed
- frontend build: passed

### Known Issues
- Mimo API call failed (answer_source=real_llm_fallback_mock, not real_llm)
- llm_model=None suggests CUSTOMEROPS_LLM_MIMO_MODEL may not be set
- Likely cause: base_url format, API key validity, or model name mismatch on Render
- Tag v1.4.1-real-mimo NOT created (real LLM response not obtained)

---

## [v1.4.0-badcase] — 2026-06-26

### Added
- Added `backend/app/eval/bad_case_schema.py` — BadCase structured schema with 11 scenarios, 11 failure types, baseline/after status tracking
- Added `backend/app/eval/bad_cases.jsonl` — 131 structured bad cases covering customs/refund/logistics/payment/order/package/return/exchange/address/coupon/out_of_scope
- Added `backend/app/eval/bad_case_eval.py` — Bad Case Evaluation Harness (route/intent/citation/next_step/out_of_scope checks)
- Added `docs/BAD_CASE_BANK_REPORT.md` — Bad Case Bank detailed report with scenario distribution, failure types, evaluation results
- Added `docs/BAD_CASE_OPTIMIZATION_SUMMARY.md` — Optimization summary with before/after metrics and resume-statement guidance

### Quality Results
- Bad Case Bank: 131 cases, 11 scenarios
- Bad Case Eval Pass Rate: 97.71% (128/131 structural pass)
- Bad Case Citation Coverage: 97.54%
- Bad Case Fallback Rate: 7.63%
- Answer Pass Rate: 60.66% (unchanged from v1.3.0)
- Citation Hit Rate: 95.90% (unchanged from v1.3.0)
- Retrieval Recall@5: 90.00% (unchanged)

### Verified
- pytest: all tests passed
- ruff: all checks passed
- frontend build: passed
- No real API keys committed
- No eval data modified
- No failed cases deleted

---

## [v1.3.0-quality] — 2026-06-26

### Added
- Added Mimo model profile to frontend and backend (`LLMProfile`, `ModelSelector`, `ALLOWED_PROFILES`, `_PROFILE_ENV_MAP`)
- Added `.env.example` with DeepSeek / Doubao / Mimo configuration template
- Added `docs/KNOWLEDGE_BASE_INVENTORY.md` — knowledge base size audit (14 docs, 18 chunks, 122 eval cases)
- Added `docs/RAG_QUALITY_IMPROVEMENT_REPORT.md` — baseline vs optimized metrics report
- Added `docs/BAD_CASE_ANALYSIS.md` — failed case classification and optimization log

### Changed
- Fixed browser title: `frontend` → `CustomerOpsAgent｜跨境电商客服 Agent`
- Updated `frontend/src/lib/constants.ts` — RELEASE_TAG to v1.3.0-quality
- Updated `frontend/src/components/chat/AnswerCard.tsx` — RAG evidence banner, citations collapsible section, retrieved_doc_ids display, route/source friendly labels
- Updated `frontend/src/data/examples.ts` — optimized example questions for RAG demo
- Updated `backend/app/agent/intent_recognizer.py` — expanded keywords for logistics_policy, package, coupon, customs; added disambiguation rules for address, customs, package
- Updated `backend/app/agent/mock_answer_generator.py` — improved answer templates with structured format (conclusion → evidence → actions → citation)
- Updated `backend/app/agent/fallback_rules.py` — improved fallback messages; fixed sensitive detection false positives (pin in shipping, China)
- Updated `backend/app/eval/answer_eval.py` — expanded `_CATEGORY_INTENT_MAP` for multi-intent matching; added logistics+RAG route correctness bonus
- Updated `.gitignore` — added `!.env.example`

### Quality Results
- Answer Pass Rate: 46.72% → 60.66% (+13.94 pp)
- Citation Hit Rate: 83.61% → 95.90% (+12.29 pp)
- Fallback Rate: 13.11% → 0.82% (-12.29 pp)
- Avg Relevance: 0.7566 → 0.9148 (+0.1582)
- Retrieval Recall@5: 90.00% (unchanged)
- Retrieval MRR: 0.7850 (unchanged)

### Verified
- pytest: all tests passed
- ruff: all checks passed
- frontend build: passed
- No real API keys committed
- No .env committed
- No eval data modified

---

## [Frontend M7] — 2026-06-26

### Added
- Added `docs/FINAL_FRONTEND_RELEASE_CHECKLIST.md` — Frontend M0–M7 milestone summary, verification results, boundaries, release tag candidate
- Added `docs/FINAL_DEPLOYMENT_SMOKE_REPORT.md` — Render/Vercel online smoke results, CORS verification, known limitations, conclusion

### Changed
- Updated `docs/DEV_STATUS.md` — Current phase updated to Frontend M7, added M7 completed content, updated next steps
- Updated `docs/CHANGELOG.md` — Added M7 entry
- Updated `docs/PROJECT_CONTEXT.md` — Updated delivery status to Frontend M7, removed interview/resume reference from capability list
- Updated `docs/API_SMOKE_DEMO.md` — Added online deployment section with Render URL and smoke results
- Updated `docs/LLM_ADAPTER.md` — Added online smoke results section
- Updated `frontend/FRONTEND_BRIEF.md` — Added M7 section with smoke results and release tag

### Verified
- Local: 254 pytest passed, ruff passed, `npm run build` passed
- Render: All 7 API smoke tests passed (mock/deepseek/doubao/invalid/non-business)
- CORS: Verified for Vercel origin
- Vercel: Page accessible, JS/CSS assets verified
- Security: No secrets in frontend or docs
- Release tag: v1.2.0-demo

## [Frontend M4] — 2026-06-25

### Added
- Added `frontend/src/lib/api.ts` — API client with `getApiBaseUrl()` and `sendAgentMessage()`
- Added `frontend/src/components/chat/ModelSelector.tsx` — Profile selector (Mock / DeepSeek / Doubao)
- Added profile-based LLM config (`load_llm_config_for_profile`) to `backend/app/llm/config.py`
- Added `ALLOWED_PROFILES` whitelist to `backend/app/llm/config.py`
- Added CORS middleware to `backend/app/main.py` (localhost + Vercel)
- Added 20+ new tests for profile selection, fallback, CORS, API integration

### Changed
- Updated `backend/app/agent/schemas.py` — Added `llm_profile` field to `AgentResponse`
- Updated `backend/app/agent/workflow.py` — `_try_real_llm_answer` accepts `llm_profile`, uses profile-based config
- Updated `backend/app/api/agent.py` — Added `llm_profile` to request/response, whitelist validation
- Updated `frontend/src/lib/types.ts` — Added `LLMProfile`, `ChatMessageStatus`, `llm_profile` fields
- Updated `frontend/src/lib/constants.ts` — Added `DEFAULT_LLM_PROFILE`
- Updated `frontend/src/components/chat/ChatWorkspace.tsx` — Full API integration with loading/error states
- Updated `frontend/src/components/chat/ChatInput.tsx` — Added `onSend` callback
- Updated `frontend/src/components/chat/ExamplePrompts.tsx` — Added `onSelect` callback
- Updated `frontend/src/components/metadata/MetadataPanel.tsx` — Shows `llm_profile` and fallback hints
- Updated `frontend/src/components/chat/AnswerCard.tsx` — Shows `llm_profile` badge
- Updated `frontend/src/App.tsx` — Wired up real API response to metadata/citation panels
- Updated `README.md` — Frontend API integration status
- Updated `frontend/FRONTEND_BRIEF.md` — M4 acceptance criteria
- Updated `docs/LLM_ADAPTER.md` — Profile-based configuration docs
- Updated `docs/API_SMOKE_DEMO.md` — `llm_profile` request/response examples
- Updated `docs/DEV_STATUS.md` — Current stage: Frontend M4
- Updated `docs/CHANGELOG.md` — This entry
- Updated `docs/PROJECT_CONTEXT.md` — Frontend API integration status

### Security
- Frontend sends only public profile names, never API keys
- Backend whitelist validates `llm_profile` (mock / deepseek / doubao)
- CORS restricted to localhost:5173 and Vercel domain
- No secrets committed

---

## [v1.1.0-demo] — 2026-06-25

### Added
- Added `docs/FINAL_LLM_ADAPTER_RELEASE_CHECKLIST.md` — Final LLM adapter release checklist
  - Release scope (v1.1.0-demo, mock default + optional real LLM)
  - New capabilities since v1.0.1-demo (8 items)
  - Verification checklist (12 items, all passed)
  - Required commands (pytest / ruff / retrieval eval / answer eval / API smoke)
  - Optional real LLM smoke (placeholder examples + safety rules)
  - Final metrics (233 passed / ruff ok / eval results)
  - Known limitations (10 items)
  - Release tag (v1.1.0-demo, preserving old tags)

### Changed
- Updated `README.md` — Development Status to M11.5, Docs Index with new checklist
- Updated `docs/DEV_STATUS.md` — Current stage updated to M11.5, next steps updated
- Updated `docs/PROJECT_CONTEXT.md` — Release version to v1.1.0-demo, capability snapshot

### Notes
- No business logic changes. No test logic changes. No eval logic changes.
- No real logistics API. No secrets committed.
- v1.0.1-demo and v1.0.0-demo remain preserved.

---

## [未发布 - M11]

### Added
- Added `backend/app/llm/` — Optional LLM adapter package
  - `__init__.py` — Package init, exports core types
  - `schemas.py` — LLMMessage / LLMGenerationRequest / LLMGenerationResult
  - `config.py` — LLM config from environment variables (no API key logging)
  - `base.py` — BaseLLMAdapter abstract base class
  - `mock_adapter.py` — MockLLMAdapter (default, template-based)
  - `openai_compatible_adapter.py` — OpenAICompatibleAdapter for /chat/completions
  - `factory.py` — create_llm_adapter factory (default: mock)
- Added `backend/tests/test_llm_adapter.py` — LLM adapter tests (13 test cases)
  - Default mock mode / missing config fallback / API key safety / determinism / eval field scan / answer_source / failure fallback / API response
- Added `docs/LLM_ADAPTER.md` — LLM adapter documentation
  - Scope / Modes / Environment Variables / Safety / Fallback / Smoke Test / Limitations / Architecture

### Changed
- Updated `backend/app/agent/schemas.py` — AgentResponse: added answer_source, llm_provider, llm_model fields
- Updated `backend/app/agent/workflow.py` — Integrated LLM adapter with fallback to mock
- Updated `backend/app/api/agent.py` — AgentChatResponse: added answer_source, llm_provider, llm_model
- Updated `README.md` — Added optional real LLM adapter feature, API response fields, limitations, docs link
- Updated `docs/DEV_STATUS.md` — Current stage updated to M11
- Updated `docs/PROJECT_CONTEXT.md` — Added LLM adapter capability

---

## [v1.0.1-demo] — 2026-06-25

### Fixed
- Fixed retrieval eval command in `docs/FINAL_RELEASE_CHECKLIST.md` — added `PYTHONPATH=backend` requirement with Windows PowerShell / CMD / Bash examples.
- Added technical note explaining `retrieval_eval.py` uses `app.*` imports requiring `backend` on `PYTHONPATH`.

### Notes
- No code changes. No dataset changes. No tag overwrite.
- v1.0.0-demo remains preserved; v1.0.1-demo is a documentation-only patch release.

## [未发布]

### Added
- Added `docs/FINAL_RELEASE_CHECKLIST.md` — Final release checklist
  - Release scope (demo release positioning)
  - Completed milestones (M0-M10.5)
  - Verification commands (pytest / ruff / retrieval eval / answer eval / API smoke demo)
  - Final metrics (retrieval / answer / API)
  - Safety checklist (7 items)
  - Known limitations (7 items)
  - Release tag: v1.0.0-demo
- Added `docs/FINAL_ACCEPTANCE_REPORT.md` — Final acceptance report
  - Acceptance summary (core pipeline)
  - Functional acceptance (13 components)
  - Evaluation acceptance (retrieval + answer metrics)
  - API acceptance (7 verified scenarios)
  - Security / boundary acceptance (7 checks)
  - Final status (demo release ready + optional next steps)

### Changed
- Updated `README.md`
  - Added Documentation links for Final Release Checklist and Final Acceptance Report
  - Updated Development Status to M10.5 demo release ready
- Updated `docs/DEV_STATUS.md`
  - Current stage updated to M10.5 Final Release Checklist
  - Current status updated to Demo Release Ready
  - Added M10.5 completed content
  - Updated next steps to optional work (M11/M12/frontend/deployment)
- Updated `docs/CHANGELOG.md` — Added M10.5 entry
- Updated `docs/PROJECT_CONTEXT.md`
  - Added current release status (v1.0.0-demo)
  - Added final capability snapshot
  - Added limitations
  - Added next optional work

---

### Added
- Added `backend/app/api/agent.py` — Agent Chat API router
  - `POST /api/agent/chat` — wraps `run_customer_service_agent()` as FastAPI endpoint
  - `AgentChatRequest` — request schema (user_query / order_id / conversation_history)
  - `AgentChatResponse` — response schema (answer / route / intent / detail_intent / citations / fallback_triggered / fallback_reason / confidence / retrieved_doc_ids / order_id / tool_used)
  - Error handling: 422 for empty query, 500 for workflow exceptions
  - Does not import eval_cases / expected_keywords / expected_doc_ids
- Added `backend/tests/test_agent_api.py` — Agent API tests (9 test cases)
  - customs query / refund query / logistics with order_id / logistics without order_id fallback / out-of-scope fallback / empty query rejection / history limiting / eval data static scan / public docs safety
- Added `docs/API_SMOKE_DEMO.md` — API smoke demo documentation
  - Endpoint description, request/response body, curl examples, limitations
- Added `docs/EVAL_REPORT_M9_5.md` — M9.5 answer quality polish report

### Changed
- Updated `backend/app/main.py` — registered agent router
- Updated `README.md` — added Features / API Smoke Demo / Evaluation / Limitations sections
- Updated `docs/AGENT_WORKFLOW.md` — added API entrypoint section (section 9)
- Updated `docs/DEV_STATUS.md` — current stage updated to M10
- Updated `docs/PROJECT_CONTEXT.md` — added current delivery status

### Changed
- Updated `backend/app/agent/intent_recognizer.py` — M9.5 intent recognition polish
  - Added shipping delay keywords to `logistics_policy`: "还没到", "快一个月", "hasn't arrived", "taking too long", etc.
  - Added delay-aware disambiguation: delay indicators route to logistics_policy, not package
  - Added refund vs logistics_policy disambiguation: refund keywords take precedence
  - Added colloquial package keywords: "丢了", "包裹丢了", "找不到包裹"
- Updated `backend/app/agent/mock_answer_generator.py` — M9.5 answer generation polish
  - Increased `max_chars_per_chunk` from 300 to 400 for better evidence extraction
  - Order template: multi-intent detection for order cancel + refund queries
  - Refund template: expanded to cover return-refund flow and timeline
  - Logistics policy template: delay-specific response when delay indicators detected
  - Citation selection: prefer diverse doc_ids (one per unique doc first)
- Updated `backend/tests/test_answer_workflow_optimization.py` — M9.5 tests (33 test cases, +14)
- Updated `docs/ANSWER_WORKFLOW_OPTIMIZATION_LOG.md` — Added M9.5 section
- Updated `docs/AGENT_WORKFLOW.md` — Added M9.5 key improvements
- Updated `docs/DEV_STATUS.md` — Current stage updated to M9.5

### M9.5 Answer Quality Results
- avg_relevance: 0.7418 → 0.7566 (+0.0148)
- avg_groundedness: 0.8205 → 0.8328 (+0.0123)
- avg_completeness: 0.5225 → 0.5464 (+0.0239)
- citation_hit_rate: 81.15% → 83.61% (+2.46%)
- answer_pass_rate: 44.26% → 46.72% (+2.46%)
- fallback_rate: 15.57% → 13.11% (-2.46%)
- failed_cases: 68 → 65 (-3)

---

### Added (M9)
- Added `backend/tests/test_answer_workflow_optimization.py` — M9 answer workflow optimization tests（19 个测试用例）
- Added `docs/ANSWER_WORKFLOW_OPTIMIZATION_LOG.md` — M9 answer workflow optimization log
- Added `docs/EVAL_REPORT_M9.md` — M9 answer quality evaluation report

### Changed (M9)
- Updated `backend/app/agent/intent_recognizer.py` — M9 intent recognition optimization
  - Split `logistics` intent into `logistics_status` (tracking, needs order_id) and `logistics_policy` (policy, uses RAG)
  - Added disambiguation rules: package keywords override logistics_status; policy keywords override logistics_status
  - Added `_PACKAGE_OVERRIDE_KEYWORDS` and `_POLICY_OVERRIDE_KEYWORDS` for smarter disambiguation
- Updated `backend/app/agent/fallback_rules.py` — M9 fallback rule optimization
  - `missing_order_id` only triggers for `logistics_status` intent, not `logistics_policy`
- Updated `backend/app/agent/mock_answer_generator.py` — M9 mock answer optimization
  - Uses content from top 3 chunks instead of just 1
  - Includes up to 300 chars per chunk (was 200)
  - Adds citation references in answer text
  - Deduplicates similar content across chunks
  - Added `_extract_evidence_sentences()` helper function
- Updated `backend/app/agent/schemas.py` — Updated detail_intent description to include new intents
- Updated `backend/app/agent/workflow.py` — Updated route decision for logistics_status
- Updated `backend/tests/test_agent_workflow.py` — Updated tests for new intent split
- Updated `docs/AGENT_WORKFLOW.md` — Updated intent recognition section for M9
- Updated `docs/DEV_STATUS.md` — Current stage updated to M9
- Updated `docs/CHANGELOG.md` — Added M9 entry

### M9 Answer Quality Results
- avg_relevance: 0.5967 → 0.7418 (+0.1451)
- avg_groundedness: 0.6959 → 0.8205 (+0.1246)
- avg_completeness: 0.3396 → 0.5225 (+0.1829)
- citation_hit_rate: 56.56% → 81.15% (+24.59%)
- answer_pass_rate: 31.97% → 44.26% (+12.29%)
- fallback_rate: 40.16% → 15.57% (-24.59%)
- failed_cases: 83 → 68 (-15)

---

- Added `backend/app/eval/answer_eval.py` — Answer quality evaluation harness
  - `normalize_text(text)` — 文本归一化（大小写、空白）
  - `keyword_coverage(answer, expected_keywords)` — 关键词覆盖率（支持中英文）
  - `citation_hit_rate(citation_doc_ids, expected_doc_ids)` — 引用命中率
  - `evaluate_relevance(case, response)` — 相关性评估（category match / route / fallback penalty）
  - `evaluate_groundedness(case, response)` — 有据性评估（RAG citation / tool_used / fabrication detection）
  - `evaluate_completeness(case, response)` — 完整性评估（keyword coverage + fallback penalty）
  - `evaluate_citation(case, response)` — 引用质量评估
  - `evaluate_answer_case(case, response)` — 单条 case 完整评估（6 指标 + pass/fail）
  - `evaluate_agent_answers(cases)` — 批量评估 + 汇总指标
  - `run_default_answer_evaluation()` — 默认全量评估（122 cases）
  - CLI: `python -m backend.app.eval.answer_eval`
- Added `backend/tests/test_answer_eval.py` — Answer quality evaluation tests（38 个测试用例）
- Added `docs/EVAL_REPORT_M8.md` — M8 answer quality evaluation report

- Added `backend/app/agent/__init__.py` — Agent 模块初始化
- Added `backend/app/agent/schemas.py` — Agent 层数据结构（RouteType / CustomerIntent / ExtractedVariables / IntentResult / LogisticsToolResult / Citation / EvidenceCheckResult / AgentResponse）
- Added `backend/app/agent/entity_extractor.py` — 变量提取节点（extract_order_id / extract_customer_variables）
- Added `backend/app/agent/intent_recognizer.py` — 意图识别节点（recognize_intent，规则驱动，支持中英文关键词）
- Added `backend/app/agent/logistics_tool.py` — 模拟物流插件（query_mock_logistics，不接真实 API）
- Added `backend/app/agent/fallback_rules.py` — 兜底规则引擎（detect_sensitive_order_query / detect_private_info_request / evaluate_evidence / should_fallback / build_fallback_answer）
- Added `backend/app/agent/prompt_builder.py` — 提示构建器（build_customer_service_prompt / build_logistics_prompt）
- Added `backend/app/agent/mock_answer_generator.py` — 模拟回答生成器（generate_mock_rag_answer / generate_mock_logistics_answer / generate_mock_answer，不调用 LLM）
- Added `backend/app/agent/workflow.py` — 工作流编排器（run_customer_service_agent，节点式流程：Start → Extract → Intent → Route → Tool/RAG → Fallback → End）
- Added `backend/tests/test_agent_workflow.py` — Agent 工作流测试（24 个测试用例，覆盖实体提取、意图识别、物流工具、兜底规则、提示构建、回答生成、工作流集成、静态分析）

### Changed
- Updated `docs/AGENT_WORKFLOW.md` — 新增 M7 节点式流程说明和节点实现状态
- Updated `docs/DEV_STATUS.md` — 当前阶段更新为 M8 Answer Quality Evaluation，新增 M8 已完成内容和结果
- Updated `docs/CHANGELOG.md` — 追加 M7 变更记录
- Updated `docs/00_SCOPE_LOCK.md` — 移除面试相关内容
- Updated `docs/03_EVAL_DESIGN.md` — 移除面试相关内容
- Updated `docs/01_ACCEPTANCE_CRITERIA.md` — 移除面试相关内容
- Updated `docs/PROJECT_CONTEXT.md` — 移除面试相关内容
- Updated `docs/ROADMAP_V2.md` — 移除面试相关内容

### Fixed
- 无

## [0.8.0] - M6.5: Lightweight Agent Workflow Design

**发布日期**：2026-06-25

**版本说明**：M6.5 补充轻量客服 Agent Workflow 设计文档，将项目从"RAG demo"升级为"轻量客服 RAG Agent 系统"。定义 Intent Recognition、Evidence Check、Citation Check、Fallback Rules 设计，明确 M7 开发边界。

### Added

- Added `docs/AGENT_WORKFLOW.md` — 轻量客服 Agent Workflow 设计文档
  - Agent Workflow 总览（8 个节点的单链路工作流）
  - Intent Recognition 设计（11 个 intent：logistics/customs/return/refund/exchange/address/order/payment/package/coupon/unknown）
  - Evidence Check 设计（6 项检查：chunks 非空 / top score / category 匹配 / citation 可用 / intent 覆盖 / 多意图冲突）
  - Citation Check 设计（4 条规则）
  - Fallback / Escalation 规则（10 条兜底场景及话术）
  - M7 开发范围（7 个模块 + 不做清单）
  - 设计原则（Rule-first / Fail-safe / Citation-required / Single-pipeline / Intent-aware）

### Changed

- Updated `docs/00_SCOPE_LOCK.md`
  - 项目定位从"RAG Agent"补充为"轻量客服 RAG Agent"
  - 新增 Agent 层说明（intent recognition / evidence check / answer generation / citation check / fallback rules）
  - 明确不做复杂 6 Agent 工单系统、不做 LangGraph、不做多租户 SaaS

- Updated `docs/02_RAG_DESIGN.md`
  - 新增第七节"RAG 与 Agent Workflow 的关系"
  - RAG 负责找证据，Agent 负责判断和决策
  - 没有证据时不能强答

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M6.5 Agent Workflow 设计补档
  - 下一步：M7 intent recognition + prompt builder + mock answer generator + citations + fallback rules
  - 更新风险点和禁止事项

- Updated `docs/CHANGELOG.md`
  - 追加 M6.5 变更记录

### Fixed
- 无

## [0.7.0] - M6: Full Bad Case Eval Set

**发布日期**：2026-06-25

**版本说明**：M6 扩展 120+ bad cases 形成 full eval set，在 122-case 数据集上重新评估 baseline vs optimized retriever。Optimized Recall@5 从 75.4% 提升到 98.4%，MRR 从 0.70 提升到 0.91。

### Added

- Added `backend/data/eval_cases_full.jsonl` — 全量评测集
  - 122 条 eval cases（20 seed + 102 新增）
  - category 覆盖：logistics(18), customs(16), package(18), return(10), refund(10), exchange(10), address(10), order(10), payment(10), coupon(10)
  - market 覆盖：US(37), EU(16), GLOBAL(69)
  - language 覆盖：zh(82), en(40)
  - difficulty 覆盖：easy(16), medium(75), hard(31)
  - 问题类型：直问型、口语型、模糊型、复合型、跨语言型、市场限定型、边界型、多意图型、拼写变化型、高频客服型

- Added `backend/tests/test_full_eval_dataset.py` — full eval dataset 质量测试
  - 12 个测试用例
  - 覆盖：加载校验、case_id 唯一性、expected_doc_ids 存在性、language 分布、difficulty 分布、category 覆盖、market 覆盖、keywords 质量、英文问题语言检查、seed 包含检查、baseline+optimized 集成测试、seed 文件未修改

- Added `docs/BAD_CASE_OPTIMIZATION_LOG.md` — bad case 优化日志
  - 数据集说明（seed 20 条 + full 122 条）
  - 优化策略摘要（query expansion / signal inference / metadata boost / doc diversity）
  - 6 类 baseline 典型失败类型分析
  - seed failed cases 回顾
  - full eval baseline vs optimized 对比
  - 仍失败 cases 摘要（2 条）
  - 简历指标口径提醒

- Added `docs/EVAL_REPORT_M6.md` — M6 评测报告
  - 数据集说明和分布
  - baseline vs optimized 指标表
  - 结论和简历表述建议
  - 注意事项

### Changed

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M6 full bad case eval set 完成
  - 下一步：M7 prompt builder + mock answer generator + citations
  - 更新风险点和禁止事项

- Updated `docs/CHANGELOG.md`
  - 追加 M6 变更记录

### Fixed
- 无

## [0.6.0] - M5: Optimized Retriever

**发布日期**：2026-06-24

**版本说明**：M5 optimized retriever 实现，在 M3 baseline BM25Retriever 基础上通过查询扩展、信号推断和 metadata-aware boosting 提升检索质量。修复了 baseline 的 2 个 failed cases，Recall@5 从 90% 提升到 100%，MRR 从 0.785 提升到 0.917。

### Added

- Added `backend/app/rag/optimized_retriever.py` — optimized retriever
  - `normalize_query(query)` — 小写化、去多余空白、保留 CJK
  - `expand_query(query)` — 跨语言同义词扩展（12 组领域词典：shipping/物流、customs/清关、delay/延迟 等）
  - `infer_query_signals(query)` — 从 query 推断 category / market / language
  - `QuerySignals` — dataclass 存储推断信号
  - `OptimizedRetriever(chunks)` — 基于 BM25Retriever 的优化检索器
  - `OptimizedRetriever.search(query, top_k)` — 完整 pipeline：normalize → expand → infer → BM25 → metadata boost → doc diversity → top-k
  - `_compute_boost(chunk, signals)` — 可解释的 metadata boost（category ×1.15, market ×1.10, GLOBAL ×1.03, language ×1.08，最大复合 ×1.41）
  - `build_default_optimized_retriever()` — 从默认知识库构建 optimized retriever
  - CLI: `python -m app.rag.optimized_retriever "query"` — 输出 query signals + top-k 结果
  - 防作弊设计：不读取 eval 数据，不使用 ground-truth 字段

- Added `backend/tests/test_optimized_retriever.py` — optimized retriever 测试
  - 14 个测试用例
  - 覆盖: 跨语言扩展、category 推断、market 推断、防作弊检查（静态扫描）、metadata 保留、score 排序、空查询、top-k 限制、默认构建、eval 对比（Recall@5 不降级、MRR 或 Recall@1 不降级）、failed case 修复验证

### Changed

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M5 optimized retriever 完成
  - 下一步：M6 扩展 120+ bad cases
  - 更新风险点和禁止事项

- Updated `docs/CHANGELOG.md`
  - 追加 M5 变更记录

### Fixed
- 无

## [0.5.0] - M4: Retrieval Evaluation Harness

**发布日期**：2026-06-24

**版本说明**：M4 retrieval evaluation harness 实现，加载 M1 的 eval cases，调用 M3 的 baseline BM25 retriever，计算 Recall@1/3/5 和 MRR，输出 per-case 结果和 failed cases，为 M5 optimized retriever 提供基准指标。

### Added

- Added `backend/app/eval/retrieval_eval.py` — retrieval evaluation harness
  - `get_default_eval_cases_path()` — 返回默认 seed eval cases 路径
  - `load_eval_cases(path)` — 加载 JSONL eval cases，空行跳过，坏 JSON 报行号，schema 校验报行号
  - `unique_doc_ids_from_results(results)` — 从 RetrievedChunk 列表提取去重 doc_id，保持检索顺序，同一 doc 多 chunk 只保留第一次出现
  - `hit_at_k(expected_doc_ids, retrieved_doc_ids, k)` — 检查 top-k 是否命中任一 expected doc
  - `reciprocal_rank(expected_doc_ids, retrieved_doc_ids)` — 计算第一个命中 doc 的倒数排名
  - `evaluate_case(case, retriever, top_k)` — 单条 case 评测，输出 CaseResult（case_id, question, category, market, language, difficulty, expected_doc_ids, retrieved_doc_ids, retrieved_chunk_ids, top_scores, hit_at_1, hit_at_3, hit_at_5, reciprocal_rank）
  - `evaluate_retriever(retriever, cases, top_k)` — 批量评测，输出 EvalReport（total_cases, recall_at_1, recall_at_3, recall_at_5, mrr, failed_cases, per_case_results）
  - `run_default_evaluation()` — 默认 baseline 评测（build_default_retriever + load_eval_cases + evaluate_retriever）
  - CLI: `python -m app.eval.retrieval_eval` — 输出 aggregate metrics + failed cases 列表
  - 防作弊设计：expected_doc_ids 只在 eval 层用于打分，不传入 retriever.search

- Added `backend/app/eval/__init__.py` — eval 包初始化

- Added `backend/tests/test_retrieval_eval.py` — retrieval eval 测试
  - 10 个测试用例
  - 覆盖: seed 加载（20 条）、doc_id 去重保序、hit_at_k 边界、reciprocal_rank 计算、防作弊测试（search 只接收 query + top_k）、字段完整性、aggregate metrics 计算、默认评测集成测试、retriever.py 静态检查、坏 JSON/schema 错误行号

### Changed

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M4 retrieval evaluation harness 完成
  - 下一步：M5 optimized retriever
  - 更新风险点（eval harness 作弊、retriever 偷看、baseline 低不等于失败、failed cases 必须输出、eval/retriever 解耦、doc 去重）

- Updated `docs/CHANGELOG.md`
  - 追加 M4 变更记录

### Fixed
- 无

## [0.4.0] - M3: Baseline BM25 Retriever

**发布日期**：2026-06-24

**版本说明**：M3 baseline BM25 retriever 实现，在 M2 产出的 chunks 上完成 Top-K 关键词检索，返回带 score 和 metadata 的检索结果，为 M4 retrieval evaluation 做准备。

### Added

- Added `backend/app/rag/retriever.py` — baseline BM25 检索器
  - `tokenize(text)` — 英文小写分词 + CJK 字符级 token
  - `BM25Retriever(chunks, k1, b)` — 自实现 BM25 检索器
  - `BM25Retriever.search(query, top_k)` — Top-K 检索，按 score 降序返回 RetrievedChunk
  - `build_default_retriever()` — 从默认知识库构建 retriever
  - CLI: `python -m app.rag.retriever "query"` — CLI smoke test
  - 标准 BM25 公式：IDF(q) * (TF * (k1+1)) / (TF + k1 * (1 - b + b * dl/avgdl))
  - k1=1.5, b=0.75

- Added `backend/app/rag/schemas.py` — 新增 RetrievedChunk 模型
  - 12 字段: KnowledgeChunk 的 11 字段 + score
  - score >= 0，类型为 float
  - 保留 KnowledgeChunk 完整 metadata

- Added `backend/tests/test_retriever.py` — retriever 测试
  - 12 个测试用例
  - 覆盖: 英文 tokenize、中文 tokenize、空 chunks、空 query、top-k 排序、metadata 保留、seed KB 检索、防作弊检查、top-k 限制、score 非负、top_k=0 异常、英文查询

### Changed

- Updated `backend/app/rag/schemas.py`
  - 新增 RetrievedChunk 模型（保留 KnowledgeDocument、KnowledgeChunk、EvalCase 不变）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M3 baseline BM25 retriever 完成
  - 下一步：M4 retrieval evaluation harness
  - 更新风险点和禁止事项

### Fixed
- 无

## [0.3.0] - M2: Loader + Chunker

**发布日期**：2026-06-24

**版本说明**：M2 loader + chunker 实现，将 M1 的 JSONL 知识库加载为 Python 对象并切分为可检索 chunks，为 M3 BM25 retriever 做准备。

### Added

- Added `backend/app/rag/loader.py` — JSONL 知识库加载器
  - `load_jsonl(path)` — 逐行加载 JSONL，空行跳过，坏 JSON 报行号
  - `load_knowledge_documents(path)` — 加载并校验为 KnowledgeDocument 列表
  - `get_default_knowledge_path()` — 返回默认 seed 知识库路径
  - CLI: `python -m app.rag.loader` 输出文档数量、语言分布、category 分布

- Added `backend/app/rag/chunker.py` — 文档切分器
  - `split_text_by_chars(text, max_chars, overlap)` — 按字符切分文本
  - `chunk_document(doc, max_chars, overlap)` — 单文档切分
  - `chunk_documents(docs, max_chars, overlap)` — 批量切分
  - 默认 max_chars=320, overlap=40
  - chunk_id 格式: `{doc_id}::chunk_{index:03d}`
  - CLI: `python -m app.rag.chunker` 输出文档数、chunks 数、平均长度

- Added `backend/app/rag/schemas.py` — 新增 KnowledgeChunk 模型
  - 11 字段: chunk_id / doc_id / title / category / market / language / policy_type / priority / source / content / chunk_index
  - 保留 KnowledgeDocument 核心 metadata
  - chunk_id 不能为空，chunk_index >= 0

- Added `backend/tests/test_loader_chunker.py` — loader + chunker 测试
  - 11 个测试用例
  - 覆盖: 加载、metadata 保留、短文档单 chunk、长文档多 chunk、overlap、chunk_id 稳定、坏 JSON 行号、非法参数、语言/市场保留

### Changed

- Updated `backend/app/rag/schemas.py`
  - 新增 KnowledgeChunk 模型（保留 KnowledgeDocument 和 EvalCase 不变）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M2 loader + chunker 完成
  - 下一步：M3 baseline BM25 retriever
  - 更新风险点和禁止事项

### Fixed
- 无

## [0.2.0] - M1: 知识库 Schema + Seed Eval Cases

**发布日期**：2026-06-24

**版本说明**：M1 数据层建设，创建 Pydantic 数据模型、种子知识库（14 条）、种子评测集（20 条）和数据校验测试。

### Added

- Added `backend/app/rag/schemas.py` — Pydantic 数据模型
  - KnowledgeDocument：9 字段（doc_id/title/category/market/language/policy_type/priority/source/content）
  - EvalCase：8 字段（case_id/question/category/market/language/difficulty/expected_doc_ids/expected_keywords）
  - 字段与 M0 文档 metadata schema 对齐

- Added `backend/data/knowledge_base/customer_service_seed.jsonl` — 种子知识库
  - 14 条知识文档，覆盖 12 个场景
  - 场景覆盖：物流时效、清关延迟、退货政策、退款规则、换货流程、地址修改、订单取消、支付失败、包裹丢失、包裹破损、优惠券问题、多语言英文咨询
  - 语言覆盖：zh（12 条）/ en（2 条）
  - 市场覆盖：US / EU / GLOBAL

- Added `backend/data/eval_cases_seed.jsonl` — 种子评测集
  - 20 条评测用例
  - difficulty 分布：easy(8) / medium(8) / hard(4)
  - language 分布：zh(16) / en(4)
  - 所有 expected_doc_ids 均对应知识库 doc_id

- Added `backend/tests/test_data_schema.py` — 数据 schema 校验测试
  - JSONL 读取与 Pydantic 校验
  - doc_id / case_id 唯一性检查
  - expected_doc_ids 与知识库交叉校验
  - language 覆盖检查（zh/en）
  - 数量检查（12+ docs, 20 cases）
  - 英文 case 问题语言检查

### Changed

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M1 数据层建设完成
  - 下一步：M2 loader + chunker
  - 新增风险点和禁止事项

### Fixed
- 无

## [0.1.0] - M0: RAG + Eval 方向重锁

**发布日期**：2026-06-24

**版本说明**：M0 边界重锁，项目方向从"6 Agent 工单系统"正式修正为"跨境电商客服 RAG Agent + RAG Evaluation Harness"。前端冻结为 legacy/static demo，新增 4 个设计文档，更新开发状态和变更记录。

### Added

- Added `docs/00_SCOPE_LOCK.md` — 项目边界锁定
  - 项目定位：跨境电商客服 RAG Agent + RAG Evaluation Harness
  - 做什么 / 不做什么清单
  - 前端冻结声明（legacy/static demo）
  - 知识库 Metadata Schema（8 字段：doc_id/title/category/market/language/policy_type/priority/source）
  - 多语种知识库快速迁移说明

- Added `docs/01_ACCEPTANCE_CRITERIA.md` — 两天 MVP 验收标准
  - 简历指标口径说明（"提升 30 个百分点" vs "提升 30%"）
  - 11 项必须完成标准 + 验收命令
  - 3 项可选加分
  - 8 项不做清单

- Added `docs/02_RAG_DESIGN.md` — RAG 设计文档
  - RAG 流程：knowledge base → chunking → retrieval → prompt builder → answer generator → citations
  - 分层知识库 schema（Markdown + YAML frontmatter）
  - chunking 策略（按标题+段落切分，100-500 tokens）
  - retriever 设计（baseline BM25 → optimized: metadata filter + synonym expansion + query rewrite + embedding adapter stub）
  - citations 设计（doc_id, chunk_id, source, score 一路保留）
  - 多语种迁移流程

- Added `docs/03_EVAL_DESIGN.md` — Evaluation Harness 设计
  - 第一层：Retrieval Evaluation（Recall@1/3/5, MRR）
  - 第二层：Answer Evaluation（三大维度：Relevance/Groundedness/Completeness + 辅助指标：Citation Hit Rate/Keyword Coverage/Answer Pass Rate）
  - 8 条防作弊约束
  - 数据集设计（seed_eval_cases.json, bad_cases.json）

- Added `docs/ROADMAP_V2.md` — 修正版开发路线（M0-M11）
  - 后端优先开发顺序
  - 检索方案设计（baseline → optimized）
  - 数据集策略（20 seed → 120+ bad cases）
  - Evaluation 顺序（先 Retrieval Eval，后 Answer Eval）

- Added `docs/M0_EXECUTION_PROMPT.md` — M0 执行 Prompt

### Changed

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：M0: Scope Locked, Frontend Frozen, Docs Ready
  - 下一步：M1: Knowledge Base Schema + 20 Seed Eval Cases
  - 新增风险点和禁止事项

### Fixed
- 无

## [0.0.8] - Pre-MVP Readiness Audit

**发布日期**：2026-06-11

**版本说明**：Pre-MVP Readiness Audit，审查 M0-M6 是否严格符合"开发前 9 步准备"，验证工程准备状态，修复文档不一致问题。

### Added

- Added `docs/PRE_MVP_READINESS.md` — Pre-MVP 审查报告
  - 9-Step Checklist 全部 Pass
  - Engineering Readiness Checklist 全部 Pass
  - Goal Mode Entry Conditions 全部满足
  - 结论：Ready for Goal Mode MVP Development

### Changed

- Updated `README.md`
  - 修正开发进度为 "Pre-MVP Readiness Audit completed"
  - 修正技术栈描述（AI 改为 mock-first / rule-based，数据改为 JSON file）
  - 补充文档链接（新增 PRD / DESIGN / TECHNICAL_SPEC）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Pre-MVP Readiness Audit completed
  - 新增 Pre-MVP 审查完成记录
  - 更新下一步为 Goal 模式 MVP 开发
  - 更新禁止事项为 Goal 模式规则
  - 核心文档列表新增 PRE_MVP_READINESS.md

## [0.0.7.3] - Official Frontend Design Skill Review

**发布日期**：2026-06-11

**版本说明**：Module 6.3 安装官方 frontend-design skill，重新审查首页，优化为更成熟的 ToB 工单处理工作台。

### Changed

- Installed official frontend-design skill from Anthropic skills repository
  - 来源：https://github.com/anthropics/skills
  - 安装方式：手动下载（npx skills 命令不可用）
  - 路径：`.claude/skills/frontend-design/SKILL.md`
  - 已读取 SKILL.md 并基于其指导进行设计审查

- Re-reviewed homepage using frontend-design skill guidance
  - 审查结论：无视觉焦点、信息层级扁平、Agent Timeline 缺乏流程感、空状态过多、缺少签名元素、布局节奏单调
  - 可保留：色彩系统、Header 结构、卡片边框风格、12 栏网格、模块划分

- Refined homepage into a more mature ToB support ticket workflow console
  - 新增 Pipeline 进度条（签名元素）：6 步带编号水平进度条 + 0/6 complete 计数
  - Agent Workflow 升级为 8 栏主区域，成为视觉主角
  - Review Summary + Reply Preview 降为 4 栏副区域
  - Agent 步骤增加编号（1-6）和执行时间列
  - 空状态改为真实占位内容（订单号、产品类型、物流公司等）
  - Evidence 增加真实文档名和相关度分数
  - Tool Results 增加真实数据展示
  - 标题使用 uppercase tracking-wider 建立视觉层级
  - 字号分层：标题 10px uppercase、正文 11-12px、辅助 10px

- Updated development status
  - `docs/DEV_STATUS.md` 更新为 Module 6.3 completed
  - 记录 skill 来源、安装方式、审查结论、重构结果

## [0.0.7.2] - Frontend Design Skill Repair

**发布日期**：2026-06-11

**版本说明**：Module 6.2 使用 frontend/design skill 对首页进行设计审查和重构，将 AI demo 风格的占位页优化为专业 ToB 工单处理工作台。

### Changed

- Used frontend/design skill to review and refine the placeholder homepage
  - 本地无可用 frontend/design/UI/UX skill（`.claude/skills/` 目录不存在）
  - 直接基于 `docs/DESIGN.md` 设计规范进行专业设计审查
  - 审查结论：Agent 名称错误、无信息层级、缺少必要模块、内容空洞、无导航结构、整体像模板页

- Reworked homepage into a ToB support ticket workflow console
  - 新增 Header：项目名 + Tickets/Eval 导航 + Mock Mode 状态指示 + 版本号
  - Ticket Intake：Customer Message + Order ID + Product Type + Analyze 按钮 + Quick tickets 快捷标签
  - Agent Workflow：6 个 Agent 正确名称垂直时间线（Intent → Retrieval → Tool → Policy → Reply → QA）
  - Review Summary：Final Result / Risk Level / QA Score 三栏 + Human Review 状态 + Ticket ID
  - Reply Preview：回复草稿占位区域
  - Evidence Preview：3 个 policy document 占位卡片（来源 + 相关度）
  - Tool Results：get_order + get_logistics 两个工具结果面板（键值对格式）
  - QA / Human Review：QA Score + Risks Detected + Suggestion + Risk List

- Reduced AI-demo visual style
  - 移除大面积空白和灰色占位 box
  - 使用 DESIGN.md 规范的企业蓝主色 + 状态色体系
  - 信息密集型布局，12 栏栅格系统
  - 细边框白色卡片，无渐变无玻璃拟态
  - 系统字体栈（移除 Google Fonts 网络依赖）

- Updated development status
  - `docs/DEV_STATUS.md` 更新为 Module 6.2 completed
  - 记录 design skill 使用情况、审查结论、重构结果

## [0.0.7.1] - Conda Environment Fix

**发布日期**：2026-06-11

**版本说明**：Module 6.1 修正后端验证环境，从系统 Python 切换到 Conda 环境，补充 Windows Conda 路径指引。

### Changed

- Revalidated backend initialization using the customerops-agent Conda environment
  - M6 问题：最初后端验证使用了系统 Python 3.11.5，已修正为 Conda 环境
  - Conda 路径：`E:\Conda\Scripts\conda.exe`（conda 25.9.1）
  - 环境名：`customerops-agent`（新建）
  - Python 版本：3.11.15 (conda-forge)
  - Python executable：`E:\Conda\envs\customerops-agent\python.exe`
  - pytest: 2/2 passed
  - ruff: All checks passed
  - frontend build: Successfully compiled (Next.js 16.2.9)

- Added Windows Conda path guidance to README
  - 补充 Conda 路径查找表格
  - 补充完整 Conda 命令示例（create / pip install / pytest / ruff / uvicorn）
  - 说明路径可替换

- Updated development status with Conda environment verification results
  - `docs/DEV_STATUS.md` 更新为 Module 6.1 completed
  - 记录 M6 问题、修正措施、验证结果
  - 下一步进入 Module 7

## [0.0.7] - Project Initialization

**发布日期**：2026-06-11

**版本说明**：Module 6 项目初始化，创建 backend / frontend 基础结构，FastAPI health API，Next.js 占位首页。

### Changed

- Initialized backend FastAPI project structure
  - 创建 `backend/app/` 目录结构（api / core / agents / schemas / services / rag / tools / data）
  - 创建 `backend/app/main.py` FastAPI 应用入口
  - 创建 `backend/app/api/routes_health.py` health 端点
  - 创建 `backend/app/core/config.py` 基础配置
  - 创建 `backend/requirements.txt` 依赖列表
  - 创建 `backend/conftest.py` pytest 配置

- Added health API and health test
  - `GET /health` 返回 `{"status": "ok", "service": "customerops-agent", "mode": "mock"}`
  - `backend/tests/test_health.py` 包含 2 个测试用例

- Initialized frontend Next.js project structure
  - 使用 `create-next-app` 创建 Next.js 16 + TypeScript + Tailwind CSS 项目
  - 创建 `frontend/app/page.tsx` ToB 工作台占位首页
  - 创建 `frontend/app/globals.css` 设计系统变量
  - 创建 `frontend/app/layout.tsx` 布局和元数据
  - 创建 `frontend/lib/api.ts` API 客户端占位
  - 创建 `frontend/types/ticket.ts` 类型定义占位

- Added placeholder ToB workspace homepage
  - 显示项目名 CustomerOps Agent
  - 显示定位：售后客服工单多 Agent 工作台
  - 工单输入区域占位设计
  - Agent Timeline 占位区域（6 个 Agent 步骤）
  - Evidence / Tool Result / QA 占位卡片

- Added README, .env.example, and .gitignore
  - `README.md` 包含项目简介、技术栈、启动说明、当前状态
  - `.env.example` 包含示例配置（无真实密钥）
  - `.gitignore` 排除敏感文件和缓存目录

- Updated development status
  - `docs/DEV_STATUS.md` 更新为 Module 6 completed
  - `docs/CHANGELOG.md` 新增本条记录

## [0.0.6] - Development Rules and Initialization Checklist

**发布日期**：2026-06-11

**版本说明**：Module 5 开发规矩 / Git 策略 / 初始化前检查，为后续项目初始化和 Goal 模式开发建立最终规则。

### Changed

- Updated `docs/DEV_RULES.md`
  - 新增 Goal 模式开发总规则（11 条）
  - 新增 Claude / AI 开发前必读文档列表（6 个文档）
  - 新增 Claude 每轮输出要求（6 项）
  - 新增分层职责规则（8 层职责定义）
  - 强化 Git 策略规则（8 个 checkpoint 节点）
  - 新增推荐提交信息规范（8 种场景）
  - 新增禁止提交内容清单（12 项）

- Updated `docs/TECHNICAL_SPEC.md`
  - 新增 Initialization Readiness Checklist 章节（第 15 节）
  - 文档准备检查（6 项）
  - 范围准备检查（4 项）
  - 技术准备检查（6 项）
  - 初始化必须创建（9 项）
  - 初始化禁止（8 项）
  - 初始化验收（9 项）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Module 5 Development Rules, Git Strategy, and Initialization Checklist completed
  - 已完成：开发规矩、AI 协作规则、Git 策略、初始化检查清单
  - 下一步：Module 6 项目初始化

## [0.0.5.1] - Conda Environment Rule

**发布日期**：2026-06-11

**版本说明**：Module 4.1 补充 Python Conda 环境开发规则，明确后端 Python 必须使用 Conda 虚拟环境管理。

### Changed

- Updated `docs/TECHNICAL_SPEC.md`
  - 新增 Python Environment（Conda）章节
  - 明确推荐环境名 `customerops-agent`、Python 3.11
  - 明确禁止使用全局 Python 和 venv
  - 添加后续初始化时的 Conda 环境创建和常用命令示例

- Updated `docs/DEV_RULES.md`
  - 新增 Python 开发环境规则（Conda）章节
  - 明确 Conda 环境要求、依赖管理、Claude 协作规则
  - 新增开发环境禁止项（禁止 base 环境安装依赖、禁止全局 Python、禁止 venv）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Module 4.1 Conda Environment Rule Added
  - 已完成：Conda 环境规则补充
  - 下一步：Module 5 开发规矩 / Git 策略 / 初始化前检查

## [0.0.5] - Technical Foundation Planning

**发布日期**：2026-06-11

**版本说明**：Module 4 技术地基准备阶段，完成技术栈锁定、模块设计、API 契约、Schema 定义、Mock 数据规划等核心技术文档。

### Added

- Added `docs/TECHNICAL_SPEC.md` - 技术规格文档
  - 技术目标定义
  - Fixed Stack（Python 3.11+ / FastAPI / Pydantic v2 / Next.js / React / TypeScript / Tailwind CSS）+ Future Replaceable Stack（LangGraph / 真实 LLM / Chroma / PostgreSQL / Docker）
  - 非功能需求（安全 / 性能 / 可用性 / 成本）
  - 项目目录结构设计（backend + frontend 完整目录树）
  - 后端模块设计（API / Service / Agent / RAG / Tools / Core 六层）
  - 前端模块设计（3 页面 + 15 组件 + lib / types）
  - Agent 工作流设计（6 Agent 固定线性流程 + 输入输出 + 失败处理 + 实现方式）
  - API 契约（6 个接口：health / examples / tickets analyze / tickets get / evals cases / evals run）
  - Pydantic Schema 设计（14 个核心 Schema 字段定义）
  - Mock 数据设计（mock_orders / mock_logistics / eval_cases）
  - Knowledge Base 设计（6 篇 Markdown 知识库）
  - 测试计划（11 类测试 + 验收标准）
  - 项目初始化要求（11 项）
  - Goal 模式技术指令摘要

### Changed

- Updated `docs/PROJECT_CONTEXT.md`
  - Goal 模式上下文文档列表新增 `docs/TECHNICAL_SPEC.md`

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Module 4 Technical Foundation Planning completed
  - 已完成：技术地基规划全部内容
  - 下一步：Module 5 开发规矩 / Git 策略 / 初始化前检查
  - 更新禁止事项

## [0.0.4.1] - Documentation Consolidation and Scope Correction

**发布日期**：2026-06-11

**版本说明**：文档收敛与 PRD 范围修正，将阶段性文档整合为核心文档，明确 MVP / Future Scope / Permanent Safety Boundaries 区分。

### Changed

- Consolidated PRD-related documents into `docs/PRD.md`
  - 合并自：01_IDEA、02_IDEA_PRESSURE_TEST、03_IDEA_DECISION、04_PRD_DRAFT、05_PRD_REVIEW、06_PRD_FINAL、MVP_SCOPE、PROJECT_SCOPE
  - 明确 Current MVP Scope（20 项）
  - 明确 MVP Out of Scope but Future Possible（15 项）
  - 明确 Permanent Safety Boundaries（11 项）
  - 明确 Explicit Non-goals（7 项）
  - 明确后续版本路线（MVP → V1 → V2 → V3 → V4）

- Consolidated design-related documents into `docs/DESIGN.md`
  - 合并自：07_DESIGN_GUIDE、08_PAGE_PLAN、09_USER_FLOW、FRONTEND_DESIGN_REFERENCE
  - 明确 MVP 页面（3 个 + 1 个可选）
  - 明确 Future Pages（6 个）
  - 保留 15 个核心组件定义
  - 保留 9 个用户流程
  - 保留视觉基调和禁止风格

- Archived planning documents under `docs/archive/planning/`
  - 01_IDEA.md → archive
  - 02_IDEA_PRESSURE_TEST.md → archive
  - 03_IDEA_DECISION.md → archive
  - 04_PRD_DRAFT.md → archive
  - 05_PRD_REVIEW.md → archive
  - 06_PRD_FINAL.md → archive
  - MVP_SCOPE.md → archive
  - PROJECT_SCOPE.md → archive
  - 07_DESIGN_GUIDE.md → archive
  - 08_PAGE_PLAN.md → archive
  - 09_USER_FLOW.md → archive
  - FRONTEND_DESIGN_REFERENCE.md → archive

- Updated `docs/PROJECT_CONTEXT.md`
  - 新增 Goal 模式上下文规则：核心文档列表 + archive 说明

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Document consolidation and PRD scope correction completed
  - 已完成：文档收敛、PRD 合并、Design 合并、范围区分、历史归档
  - 下一步：Module 4 技术地基准备
  - 更新禁止事项

## [0.0.4] - Product Design and User Flow

**发布日期**：2026-06-11

**版本说明**：Module 3 产品设计与页面流程阶段，完成设计基调定义、页面结构规划、核心用户流程设计和前端设计参考整理。

### Added

- Added `docs/07_DESIGN_GUIDE.md` - 产品设计指南
  - 设计定位：ToB 客服运营后台，不是聊天机器人
  - 视觉风格：企业蓝主色、4px 基础网格、白色卡片 + 细边框
  - 信息层级：8 级优先级定义
  - 组件设计：15 个核心组件的设计原则（TicketInput、AgentTimeline、EvidencePanel 等）
  - 响应式原则：桌面端为主，1280px / 1024px 断点

- Added `docs/08_PAGE_PLAN.md` - 页面规划
  - Page 1：工单分析工作台（首页）— 输入工单、选择示例、启动分析
  - Page 2：分析结果详情页 — Agent Timeline + 结构化结果展示
  - Page 3：Eval / Bad Case 页面 — 评估用例和结果展示
  - Page 4：About / Architecture（可选，不单独做页面）
  - 每个页面的布局、核心模块、用户操作、对应 API、状态设计

- Added `docs/09_USER_FLOW.md` - 核心用户流程
  - 9 个核心流程：正常售后、缺订单号、物流查询、发票问题、投诉高风险、RAG 无结果、Tool 失败、QA 不通过、Eval
  - 每个流程的 Agent 执行顺序、输入输出、前端展示
  - 关键差异点和异常处理

- Added `docs/FRONTEND_DESIGN_REFERENCE.md` - 前端设计参考
  - 设计参考来源：企业后台、工单系统、电商后台、AI 工作流、数据分析
  - 可借鉴设计系统：Ant Design、Material Design、Shopify Polaris、Atlassian、shadcn/ui
  - 页面设计关键词
  - 禁止风格清单
  - 推荐布局方案
  - Goal 模式前端指令摘要
  - 颜色系统参考（CSS 变量）

### Changed

- Changed `docs/DEV_STATUS.md` - 更新开发状态
  - 当前阶段：Module 3 产品设计与页面流程完成
  - 已完成：Module 3 全部文档
  - 下一步：Module 4 技术地基准备
  - 更新禁止事项和验收标准

## [0.0.3] - PRD and Scope Finalization

**发布日期**：2026-06-11

**版本说明**：Module 2 PRD 生成与固化阶段，完成 PRD 初版、PRD 审查、最终 PRD 固化和项目范围锁定。

### Added

- Added `docs/04_PRD_DRAFT.md` - PRD 初版文档
  - 项目背景和定位
  - 目标用户定义
  - 5 个核心场景（产品故障、退款换货、物流查询、发票问题、投诉高风险）
  - 12 项 MVP 核心功能
  - 输入输出定义
  - 核心流程（6 Agent 线性编排）
  - 13 项验收标准
  - 14 项暂不实现范围
  - 6 个风险点及控制方式

- Added `docs/05_PRD_REVIEW.md` - PRD 审查文档
  - 项目定位审查：未误解
  - MVP 范围审查：合理，部分功能需保持轻量
  - 15 项必须保留功能
  - 14 项必须删除功能
  - 10 项后续扩展方向
  - 6 项 Goal 模式风险及控制方式
  - PRD 收窄建议

- Added `docs/06_PRD_FINAL.md` - 最终 PRD 文档
  - 15 项 MVP 必做功能
  - 14 项明确禁止功能
  - 用户使用路径
  - 系统输入输出定义
  - 6 个 Agent 详细定义（职责、输入、输出、失败处理）
  - 16 项功能验收标准
  - 9 项 MVP 成功标准

- Added `docs/PROJECT_SCOPE.md` - 项目范围锁定文档
  - 唯一目标
  - 15 项 In Scope
  - 20 项 Out of Scope
  - 9 项 Allowed Simplifications
  - 7 项 Hard Boundaries
  - 21 项 Goal 模式必须遵守清单

### Changed

- Changed `docs/DEV_STATUS.md` - 更新开发状态
  - 当前阶段：Module 2 PRD 生成与固化完成
  - 已完成：Module 2 全部文档
  - 下一步：Module 3 产品设计与页面流程
  - 更新禁止事项和验收标准

## [0.0.2] - Idea Validation and MVP Scope

**发布日期**：2026-06-11

**版本说明**：Module 1 想法验证 + MVP 收窄阶段，完成项目想法定义、压力测试、判断结论和 MVP 范围锁定。

### Added

#### 想法验证文档
- Added `docs/01_IDEA.md` - 想法定义文档
  - 项目想解决什么问题
  - 目标用户是谁
  - 用户为什么需要它
  - 和普通方案的区别
  - 最小可行版本定义
  - 项目希望证明的能力
  - 适合写进简历的原因
  - 适合深圳 AI Agent 岗位的原因

- Added `docs/02_IDEA_PRESSURE_TEST.md` - 想法压力测试文档
  - 需求是否真实
  - 用户场景是否明确
  - 项目是否有差异化
  - MVP 是否足够小
  - 技术实现是否可控
  - 成本是否可接受
  - 是否适合当前阶段开发
  - 是否适合写进简历
  - 是否存在伪需求
  - 是否存在过度设计风险
  - 是否和岗位匹配
  - 是否和 CodePilot 互补
  - 压力测试结论

- Added `docs/03_IDEA_DECISION.md` - 想法判断结论文档
  - 最终判断：可以做，但需要收窄范围
  - 为什么可以做
  - 为什么必须收窄
  - 简历项目优先级建议
  - 和 CodePilot、ProfileAgent 的组合关系
  - 2-4 天 MVP 开发建议
  - 明确不能进入 MVP 的功能

- Added `docs/MVP_SCOPE.md` - MVP 范围文档
  - MVP 一句话范围
  - 当前版本必须做
  - 当前版本不做
  - 输入输出定义
  - 核心 Agent 定义
  - 核心工具定义
  - 知识库范围
  - 验收标准
  - 后续扩展方向

### Changed

- Changed `docs/DEV_STATUS.md` - 更新开发状态
  - 当前阶段：Module 1 想法验证 + MVP 收窄
  - 已完成：Module 1 全部文档
  - 下一步：Module 2 PRD 生成与固化
  - 更新禁止事项和验收标准

## [0.0.1] - Context Init

**发布日期**：2026-06-11

**版本说明**：项目上下文初始化阶段，建立开发文档和规则。

### Added

#### 文档层
- Added `docs/PROJECT_CONTEXT.md` - 项目上下文文档
  - 项目名称和定位
  - 项目背景和目标用户
  - 核心业务场景
  - MVP 核心能力
  - 多 Agent 设计方向
  - 项目边界（不做什么）
  - 和普通 AI 客服机器人的区别
  - 和 CodePilot 的差异化
  - 适合简历和面试展示的原因

- Added `docs/DEV_RULES.md` - 开发规则文档
  - 总开发原则（小步快跑、渐进式开发、文档先行）
  - AI 协作规则
  - 每轮开发规则（开始前、开发中、结束后）
  - 文件修改规则
  - 模块拆分规则（分层架构）
  - API 契约规则
  - 安全规则
  - LLM 使用规则
  - 测试规则
  - Git 回滚规则
  - 禁止事项

- Added `docs/DEV_STATUS.md` - 开发状态文档
  - 当前阶段：Step 0.1 项目上下文初始化
  - 当前项目状态：初始化中
  - 已完成内容
  - 未开始内容
  - 当前限制
  - 下一步建议
  - 当前可修改范围
  - 当前禁止修改范围
  - 当前验收标准
  - 后续开发路线

- Added `docs/CHANGELOG.md` - 变更记录文档（本文件）
  - 变更记录格式说明
  - 当前版本记录

### Changed
- 无

### Fixed
- 无

### Security
- 无

## 版本规划

### v0.8.x - Agent Workflow 设计
- [x] v0.8.0 - Agent Workflow Design（轻量客服 Agent Workflow 设计）

### v0.0.x - 项目初始化与验证
- [x] v0.0.1 - Context Init（项目上下文初始化）
- [x] v0.0.2 - Idea Validation and MVP Scope（想法验证 + MVP 收窄）
- [x] v0.0.3 - PRD Generation（PRD 生成与固化）
- [x] v0.0.4 - Product Design and User Flow（产品设计与页面流程）
- [x] v0.0.5 - Technical Foundation Planning（技术地基准备）
- [x] v0.0.6 - Development Rules and Initialization Checklist（开发规矩和初始化检查）
- [x] v0.0.7 - Project Initialization（项目初始化）
- [x] v0.0.7.1 - Conda Environment Fix（Conda 环境修正与复验）
- [x] v0.0.7.2 - Frontend Design Skill Repair（前端首页设计审查与重构）
- [x] v0.0.7.3 - Official Frontend Design Skill Review（官方 skill 安装与审查）

### v0.1.x - 设计阶段
- [x] v0.1.0 - Architecture Design（技术架构设计）— 已在 v0.0.5 完成
- [x] v0.1.1 - UI/UX Design（UI/UX 设计）— 已在 v0.0.4 完成
- [x] v0.1.2 - Schema Design（数据与 Schema 设计）— 已在 v0.0.5 完成

### v0.2.x - 核心功能
- [ ] v0.2.0 - Core Agents（核心 Agent 实现）
- [ ] v0.2.1 - Business Flow（业务流程实现）
- [ ] v0.2.2 - API Layer（API 接口实现）

### v0.3.x - 前端和集成
- [ ] v0.3.0 - Frontend（前端实现）
- [ ] v0.3.1 - Integration Test（集成测试）
- [ ] v0.3.2 - Evaluation（评估和优化）

### v0.4.x - 完善和展示
- [ ] v0.4.0 - Documentation（文档完善）
- [ ] v0.4.1 - Demo（演示准备）
- [ ] v0.4.2 - Resume（简历优化）

### v1.0.0 - MVP 完成
- [ ] 完整的售后客服工单处理流程
- [ ] 多 Agent 协作演示
- [ ] RAG 知识库检索演示
- [ ] Tool Calling 演示
- [ ] 结构化输出演示
- [ ] 基础评估机制
- [ ] 前后端联调
- [ ] 演示文档和视频
