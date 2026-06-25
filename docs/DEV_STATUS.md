# CustomerOps Agent｜开发状态

## 1. 当前阶段

**M11: Optional Real LLM Adapter**

Added optional real LLM adapter for answer generation. Default remains mock. No API key = no real LLM calls.

Previous release: M10.5.1 (v1.0.1-demo) — preserved, not overwritten.

## 2. 当前项目状态

**状态：Optional Real LLM Adapter Added / Default Mock Remains**

- ✅ 项目方向重锁为 RAG + Eval（M0）
- ✅ 前端冻结为 legacy/static demo（M0）
- ✅ 边界锁定文档（00_SCOPE_LOCK.md）
- ✅ 验收标准文档（01_ACCEPTANCE_CRITERIA.md）
- ✅ RAG 设计文档（02_RAG_DESIGN.md）
- ✅ Eval 设计文档（03_EVAL_DESIGN.md）
- ✅ ROADMAP_V2 后端优先开发路线（M0-M11）
- ✅ Pydantic schema 定义（schemas.py: KnowledgeDocument + EvalCase + KnowledgeChunk + RetrievedChunk）
- ✅ Seed knowledge base（14 条知识文档）
- ✅ Seed eval cases（20 条评测用例）
- ✅ 数据 schema 测试（test_data_schema.py）
- ✅ JSONL loader（loader.py）
- ✅ KnowledgeChunk chunker（chunker.py）
- ✅ loader + chunker 测试（test_loader_chunker.py）
- ✅ Baseline BM25 retriever（retriever.py）
- ✅ RetrievedChunk schema（schemas.py）
- ✅ retriever 测试（test_retriever.py, 10 个测试用例）
- ✅ Retrieval evaluation harness（retrieval_eval.py）
- ✅ eval cases loader（load_eval_cases）
- ✅ Recall@1 / Recall@3 / Recall@5 / MRR 计算
- ✅ failed cases 输出
- ✅ retrieval eval 测试（test_retrieval_eval.py）
- ✅ Optimized retriever（optimized_retriever.py）
- ✅ query expansion（跨语言同义词扩展）
- ✅ query signal inference（category / market / language 推断）
- ✅ metadata-aware score adjustment（category / market / language boost）
- ✅ doc-level diversity（重复 doc 去重）
- ✅ baseline vs optimized seed 对比（Recall@5: 90%→100%, MRR: 0.785→0.917）
- ✅ optimized retriever 测试（test_optimized_retriever.py, 14 个测试用例）
- ✅ Full eval set（122 条 bad cases，覆盖 10 category / 3 market / 2 language / 3 difficulty）
- ✅ Full eval dataset quality tests（test_full_eval_dataset.py, 12 个测试用例）
- ✅ BAD_CASE_OPTIMIZATION_LOG.md
- ✅ EVAL_REPORT_M6.md
- ✅ baseline vs optimized full 对比（Recall@5: 75.4%→98.4%, MRR: 0.696→0.911）
- ✅ CLI smoke test
- ✅ Entity Extractor - 变量提取节点（M7）
- ✅ Intent Recognizer - 意图识别节点（M7）
- ✅ Mock Logistics Tool - 模拟物流插件（M7）
- ✅ Fallback Rules - 兜底规则引擎（M7）
- ✅ Prompt Builder - 提示构建器（M7）
- ✅ Mock Answer Generator - 模拟回答生成器（M7）
- ✅ Workflow Orchestrator - 工作流编排器（M7）
- ✅ Agent Workflow Tests - 24 个测试用例（M7）
- ✅ Answer Quality Evaluation（M8）
  - ✅ answer_eval.py — 6 个评估指标（relevance / groundedness / completeness / citation hit / keyword coverage / answer pass rate）
  - ✅ 38 个 answer eval 测试用例（test_answer_eval.py）
  - ✅ EVAL_REPORT_M8.md — 公开技术报告
  - ✅ CLI smoke test: `python -m backend.app.eval.answer_eval`
  - ✅ Answer Pass Rate: 31.97%（baseline，暴露 routing / completeness 问题）
- ✅ Answer Workflow Optimization（M9）
  - ✅ 意图识别优化：logistics 拆分为 logistics_status / logistics_policy
  - ✅ 路由决策优化：政策查询走 RAG，不要求 order_id
  - ✅ 兜底规则优化：missing_order_id 只适用于真实物流状态查询
  - ✅ Mock 回答优化：使用多个 retrieved chunks 的 evidence
  - ✅ 消歧规则：包裹/政策关键词优先于物流状态
  - ✅ M9 answer quality 测试（test_answer_workflow_optimization.py, 19 个测试用例）
  - ✅ EVAL_REPORT_M9.md — M9 评测报告
  - ✅ ANSWER_WORKFLOW_OPTIMIZATION_LOG.md — 优化日志
  - ✅ Answer Pass Rate: 44.26%（+12.29% vs M8）
  - ✅ Fallback Rate: 15.57%（-24.59% vs M8）
- ✅ Answer Quality Polish（M9.5）
  - ✅ 物流延迟 vs 包裹丢失拆分：延迟表达走 logistics_policy，损坏/丢失走 package
  - ✅ 英文物流延迟识别：新增 hasn't arrived / taking too long / shipping delay 等
  - ✅ 退款 vs 物流消歧：退款关键词优先于物流子串匹配
  - ✅ 多意图回答优化：订单取消 + 退款查询覆盖两个方面
  - ✅ 引用多样性：citation 优先来自不同 doc_id
  - ✅ 口语化包裹关键词：新增 "丢了"、"包裹丢了" 等
  - ✅ M9.5 answer quality 测试（test_answer_workflow_optimization.py, 33 个测试用例）
  - ✅ EVAL_REPORT_M9_5.md — M9.5 评测报告
  - ✅ Answer Pass Rate: 46.72%（+2.46% vs M9）
  - ✅ Fallback Rate: 13.11%（-2.46% vs M9）
- ✅ Agent API Smoke Demo（M10）
  - ✅ FastAPI endpoint: POST /api/agent/chat
  - ✅ AgentChatRequest / AgentChatResponse Pydantic schemas
  - ✅ API router 只包装 workflow，不复制逻辑
  - ✅ API 测试（test_agent_api.py, 9 个测试用例）
  - ✅ docs/API_SMOKE_DEMO.md — API smoke demo 文档
  - ✅ README 更新（Features / API Smoke Demo / Evaluation / Limitations）
- ✅ Final Release Checklist（M10.5）
  - ✅ docs/FINAL_RELEASE_CHECKLIST.md — 最终发布检查清单
  - ✅ docs/FINAL_ACCEPTANCE_REPORT.md — 最终验收报告
  - ✅ README 更新（Documentation 链接、Development Status）
  - ✅ DEV_STATUS 更新（当前阶段、下一步、已完成）
  - ✅ CHANGELOG 追加 M10.5 记录
  - ✅ PROJECT_CONTEXT 更新（current release status、final capability snapshot、limitations、next optional work）
  - ✅ Release tag: v1.0.0-demo
- ✅ 轻量客服 Agent Workflow 设计文档（M6.5）

## 3. 已完成内容

### M11：Optional Real LLM Adapter（本轮）

- ✅ 创建 `backend/app/llm/` 包
  - `__init__.py` — 包初始化，导出核心类型
  - `schemas.py` — LLMMessage / LLMGenerationRequest / LLMGenerationResult
  - `config.py` — 从环境变量读取 LLM 配置，不打印 API key
  - `base.py` — BaseLLMAdapter 抽象基类
  - `mock_adapter.py` — MockLLMAdapter，默认适配器
  - `openai_compatible_adapter.py` — OpenAICompatibleAdapter，调用 /chat/completions
  - `factory.py` — create_llm_adapter 工厂，默认返回 mock

- ✅ 修改 `backend/app/agent/schemas.py`
  - AgentResponse 新增 answer_source / llm_provider / llm_model 字段

- ✅ 修改 `backend/app/agent/workflow.py`
  - 新增 _try_real_llm_answer 辅助函数
  - 物流路由和 RAG 路由接入 LLM adapter
  - 失败时 fallback 到 mock，标记 answer_source

- ✅ 修改 `backend/app/api/agent.py`
  - AgentChatResponse 新增 answer_source / llm_provider / llm_model

- ✅ 创建 `backend/tests/test_llm_adapter.py`
  - 13 个测试用例
  - 覆盖：默认 mock / 缺配置 fallback / API key 安全 / 确定性 / eval 字段扫描 / answer_source / 失败 fallback / API response

- ✅ 创建 `docs/LLM_ADAPTER.md`
  - Scope / Modes / Environment Variables / Safety / Fallback / Smoke Test / Limitations / Architecture

- ✅ 更新 `README.md` — Features / API response / Limitations / Docs Index
- ✅ 更新 `docs/DEV_STATUS.md` — 当前阶段更新为 M11
- ✅ 更新 `docs/CHANGELOG.md` — 追加 M11 变更记录
- ✅ 更新 `docs/PROJECT_CONTEXT.md` — 补充 LLM adapter 能力

### M10.5：Final Release Checklist（本轮）

- ✅ 创建 `docs/FINAL_RELEASE_CHECKLIST.md`
  - Release Scope 说明（demo release 定位）
  - Completed Milestones 列表（M0-M10.5）
  - Verification Commands（pytest / ruff / retrieval eval / answer eval / API smoke demo）
  - Final Metrics（retrieval / answer / API 指标）
  - Safety Checklist（7 项安全检查）
  - Known Limitations（7 项已知限制）
  - Release Tag（v1.0.0-demo）

- ✅ 创建 `docs/FINAL_ACCEPTANCE_REPORT.md`
  - Acceptance Summary（核心链路说明）
  - Functional Acceptance（13 项功能验收）
  - Evaluation Acceptance（retrieval / answer 评测结果）
  - API Acceptance（7 个已验收场景）
  - Security / Boundary Acceptance（7 项安全检查）
  - Final Status（demo release ready + 可选后续工作）

- ✅ 更新 `README.md`
  - Documentation 链接新增 Final Release Checklist 和 Final Acceptance Report
  - Development Status 更新为 M10.5 demo release ready

- ✅ 更新 `docs/DEV_STATUS.md`
  - 当前阶段更新为 M10.5 Final Release Checklist
  - 当前状态更新为 Demo Release Ready
  - 新增 M10.5 已完成内容
  - 下一步更新为可选后续工作（M11/M12/frontend/deployment）

- ✅ 更新 `docs/CHANGELOG.md`
  - 追加 M10.5 变更记录

- ✅ 更新 `docs/PROJECT_CONTEXT.md`
  - 补充 current release status（v1.0.0-demo）
  - 补充 final capability snapshot
  - 补充 limitations
  - 补充 next optional work

### M10：Agent API Smoke Demo + Final Docs Consolidation（本轮）

- ✅ 创建 `backend/app/api/agent.py`
  - `AgentChatRequest` — request schema（user_query / order_id / conversation_history）
  - `AgentChatResponse` — response schema（answer / route / intent / detail_intent / citations / fallback_triggered / fallback_reason / confidence / retrieved_doc_ids / order_id / tool_used）
  - `POST /api/agent/chat` — 调用 `run_customer_service_agent()`，不复制 workflow 逻辑
  - Error handling: 422 for empty query, 500 for workflow exceptions
  - 不读取 eval_cases / expected_keywords / expected_doc_ids

- ✅ 更新 `backend/app/main.py`
  - 注册 agent router（`app.include_router(agent_router)`）

- ✅ 创建 `backend/tests/test_agent_api.py`
  - 9 个测试用例
  - 覆盖: customs query / refund query / logistics with order_id / logistics without order_id fallback / out-of-scope fallback / empty query rejection / history limiting / eval data static scan / public docs safety

- ✅ 创建 `docs/API_SMOKE_DEMO.md`
  - Endpoint 说明、Request/Response body、curl 示例、Limitations

- ✅ 更新 `README.md` — Features / API Smoke Demo / Evaluation / Limitations / Quick Start
- ✅ 更新 `docs/AGENT_WORKFLOW.md` — 新增 API entrypoint 章节
- ✅ 更新 `docs/DEV_STATUS.md` — 当前阶段更新为 M10
- ✅ 更新 `docs/CHANGELOG.md` — 追加 M10 变更记录
- ✅ 更新 `docs/PROJECT_CONTEXT.md` — 补充当前交付状态

### M8：Answer Quality Evaluation

- ✅ 创建 `backend/app/eval/answer_eval.py`
  - `normalize_text(text)` — 大小写、空白归一化
  - `keyword_coverage(answer, expected_keywords)` — 关键词覆盖率（支持中英文）
  - `citation_hit_rate(citation_doc_ids, expected_doc_ids)` — 引用命中率
  - `evaluate_relevance(case, response)` — 相关性评估（category match / route / fallback）
  - `evaluate_groundedness(case, response)` — 有据性评估（RAG citation / tool_used / fabrication check）
  - `evaluate_completeness(case, response)` — 完整性评估（keyword coverage + fallback penalty）
  - `evaluate_citation(case, response)` — 引用质量评估
  - `evaluate_answer_case(case, response)` — 单条 case 完整评估
  - `evaluate_agent_answers(cases)` — 批量评估 + 汇总指标
  - `run_default_answer_evaluation()` — 默认全量评估
  - CLI: `python -m backend.app.eval.answer_eval`

- ✅ 创建 `backend/tests/test_answer_eval.py`
  - 38 个测试用例
  - 覆盖: normalize_text / keyword_coverage / citation_hit_rate / relevance / groundedness / completeness / citation / per-case result / aggregate metrics / full dataset / anti-cheating / public docs safety

- ✅ 创建 `docs/EVAL_REPORT_M8.md`
  - 评测范围、指标说明、数据集、结果、失败分析、解读

- ✅ Answer quality baseline 结果
  - Total cases: 122
  - Avg Relevance: 0.5967
  - Avg Groundedness: 0.6959
  - Avg Completeness: 0.3396
  - Citation Hit Rate: 56.56%
  - Answer Pass Rate: 31.97%
  - Fallback Rate: 40.16%
  - Failed cases: 83

### M6.5：Agent Workflow 设计补档（本轮）

- ✅ 创建 `docs/AGENT_WORKFLOW.md`
  - Agent Workflow 总览（Intent Recognition → Query Signals → RAG Retrieval → Evidence Check → Prompt Builder → Answer Generator → Citation Check → Fallback）
  - Intent Recognition 设计（11 个 intent：logistics/customs/return/refund/exchange/address/order/payment/package/coupon/unknown）
  - Evidence Check 设计（6 项检查：chunks 非空 / top score / category 匹配 / citation 可用 / intent 覆盖 / 多意图冲突）
  - Citation Check 设计（4 条规则：必须带引用 / 不能引用不存在的 doc_id / 无引用不输出正式答复 / 引用必须来自 retrieved chunks）
  - Fallback / Escalation 规则（10 条：检索无结果 / score 太低 / citation 缺失 / 订单状态 / 知识库外 / 多意图 / 政策风险 / 情绪激烈 / 隐私敏感 / 低置信度）
  - M7 开发范围（7 个模块 + 不做清单）
  - 设计原则总结（Rule-first / Fail-safe / Citation-required / Single-pipeline / Intent-aware）

- ✅ 修改 `docs/00_SCOPE_LOCK.md`
  - 项目定位从"RAG Agent"补充为"轻量客服 RAG Agent"
  - 新增 Agent 层说明（intent recognition / evidence check / answer generation / citation check / fallback rules）
  - 明确不做复杂 6 Agent 工单系统、不做 LangGraph、不做多租户 SaaS

- ✅ 修改 `docs/02_RAG_DESIGN.md`
  - 新增第七节"RAG 与 Agent Workflow 的关系"
  - 说明 RAG 负责找证据、Agent 负责判断和决策
  - 说明没有证据时不能强答

- ✅ 修改 `docs/DEV_STATUS.md`
  - 当前阶段更新为 M6.5
  - 新增 M6.5 已完成内容

- ✅ 修改 `docs/CHANGELOG.md`
  - 追加 M6.5 变更记录

## 3.1 已完成内容

### M6：Full Bad Case Eval Set + Optimization Log（本轮）

- ✅ 创建 `backend/data/eval_cases_full.jsonl`
  - 122 条 eval cases（20 seed + 102 新增）
  - category 覆盖：logistics(18), customs(16), package(18), return(10), refund(10), exchange(10), address(10), order(10), payment(10), coupon(10)
  - market 覆盖：US(37), EU(16), GLOBAL(69)
  - language 覆盖：zh(82), en(40)
  - difficulty 覆盖：easy(16), medium(75), hard(31)
  - 问题类型：直问型、口语型、模糊型、复合型、跨语言型、市场限定型、边界型、多意图型、拼写变化型、高频客服型

- ✅ 创建 `backend/tests/test_full_eval_dataset.py`
  - 12 个测试用例
  - 覆盖：加载校验、case_id 唯一性、expected_doc_ids 存在性、language 分布、difficulty 分布、category 覆盖、market 覆盖、keywords 质量、英文问题语言检查、seed 包含检查、baseline+optimized 集成测试、seed 文件未修改

- ✅ 创建 `docs/BAD_CASE_OPTIMIZATION_LOG.md`
  - 数据集说明（seed 20 条 + full 122 条）
  - 优化策略摘要（query expansion / signal inference / metadata boost / doc diversity）
  - 6 类 baseline 典型失败类型分析
  - seed failed cases 回顾
  - full eval baseline vs optimized 对比
  - 仍失败 cases 摘要（2 条）
  - 简历指标口径提醒

- ✅ 创建 `docs/EVAL_REPORT_M6.md`
  - 数据集说明和分布
  - baseline vs optimized 指标表
  - 结论和简历表述建议
  - 注意事项

- ✅ Full eval baseline vs optimized 结果
  - Baseline: Recall@1=64.75%, Recall@3=74.59%, Recall@5=75.41%, MRR=0.6956, failed=30
  - Optimized: Recall@1=85.25%, Recall@3=96.72%, Recall@5=98.36%, MRR=0.9108, failed=2
  - 提升: Recall@5 +22.95pp, MRR +0.2152, failed -28

### M5：Optimized Retriever

- ✅ 创建 `backend/app/rag/optimized_retriever.py`
  - `normalize_query(query)` — 小写化、去多余空白
  - `expand_query(query)` — 跨语言同义词扩展（shipping→物流、customs→清关 等 12 组）
  - `infer_query_signals(query)` — 推断 category / market / language
  - `OptimizedRetriever(chunks)` — 基于 BM25Retriever 的优化检索器
  - `OptimizedRetriever.search(query, top_k)` — 查询扩展 + metadata boost + doc diversity
  - `_compute_boost(chunk, signals)` — 可解释的 metadata boost（category ×1.15, market ×1.10, language ×1.08, GLOBAL ×1.03）
  - `build_default_optimized_retriever()` — 从默认知识库构建
  - CLI: `python -m app.rag.optimized_retriever "query"` — 输出 query signals + top-k 结果

- ✅ 创建 `backend/tests/test_optimized_retriever.py`
  - 14 个测试用例
  - 覆盖: 跨语言扩展、category 推断、market 推断、防作弊检查、metadata 保留、score 排序、空查询、top-k 限制、默认构建、eval 对比、failed case 修复验证

### M4：Retrieval Evaluation Harness

- ✅ 创建 `backend/app/eval/__init__.py`
  - eval 包初始化

- ✅ 创建 `backend/app/eval/retrieval_eval.py`
  - `get_default_eval_cases_path()` — 返回默认 seed eval cases 路径
  - `load_eval_cases(path)` — 加载 JSONL eval cases，空行跳过，坏 JSON 报行号，schema 校验报行号
  - `unique_doc_ids_from_results(results)` — 从 RetrievedChunk 列表提取去重 doc_id，保持顺序
  - `hit_at_k(expected, retrieved, k)` — 检查 top-k 是否命中
  - `reciprocal_rank(expected, retrieved)` — 计算 MRR 的 RR 分量
  - `evaluate_case(case, retriever, top_k)` — 单条 case 评测，输出 CaseResult
  - `evaluate_retriever(retriever, cases, top_k)` — 批量评测，输出 EvalReport
  - `run_default_evaluation()` — 默认 baseline 评测
  - CLI: `python -m app.eval.retrieval_eval` — 输出 aggregate metrics + failed cases

- ✅ 创建 `backend/tests/test_retrieval_eval.py`
  - 10 个测试用例，覆盖：seed 加载、doc_id 去重、hit_at_k、reciprocal_rank、防作弊测试、字段验证、aggregate metrics、默认评测集成测试、retriever 不被修改、坏 JSON 报错

### M3：Baseline BM25 Retriever

- ✅ 修改 `backend/app/rag/schemas.py`
  - 新增 RetrievedChunk 模型（12 字段）

- ✅ 创建 `backend/app/rag/retriever.py`
  - `tokenize(text)` — 英文小写分词 + CJK 字符级 bigram
  - `BM25Retriever(chunks)` — 自实现 BM25 检索器
  - `BM25Retriever.search(query, top_k)` — Top-K 检索
  - `build_default_retriever()` — 从默认知识库构建 retriever
  - CLI: `python -m app.rag.retriever "query"`

- ✅ 创建 `backend/tests/test_retriever.py`
  - 12 个测试用例

### M2：Loader + Chunker

- ✅ 创建 `backend/app/rag/loader.py`
  - `load_jsonl(path)` — 逐行加载 JSONL
  - `load_knowledge_documents(path)` — 加载并校验
  - `get_default_knowledge_path()` — 返回默认路径
  - CLI: `python -m app.rag.loader`

- ✅ 创建 `backend/app/rag/chunker.py`
  - `split_text_by_chars(text, max_chars, overlap)` — 按字符切分
  - `chunk_document(doc)` — 单文档切分
  - `chunk_documents(docs)` — 批量切分
  - CLI: `python -m app.rag.chunker`

- ✅ 创建 `backend/tests/test_loader_chunker.py`
  - 11 个测试用例

### M1：知识库 Schema + Seed Eval Cases

- ✅ 创建 `backend/app/rag/schemas.py` — KnowledgeDocument + EvalCase
- ✅ 创建 `backend/data/knowledge_base/customer_service_seed.jsonl` — 14 条知识文档
- ✅ 创建 `backend/data/eval_cases_seed.jsonl` — 20 条评测用例
- ✅ 创建 `backend/tests/test_data_schema.py` — 数据校验测试

### M0：边界重锁 + 冻结前端 + 最小文档补档

- ✅ 创建 `docs/00_SCOPE_LOCK.md` — 项目边界锁定
- ✅ 创建 `docs/01_ACCEPTANCE_CRITERIA.md` — 验收标准
- ✅ 创建 `docs/02_RAG_DESIGN.md` — RAG 设计文档
- ✅ 创建 `docs/03_EVAL_DESIGN.md` — Eval 设计文档
- ✅ 创建 `docs/ROADMAP_V2.md` — 修正版开发路线
- ✅ 创建 `docs/M0_EXECUTION_PROMPT.md` — M0 执行 Prompt

### 历史完成内容（已归档为 v1 参考）

- Module 1-6：想法验证、PRD、设计、技术地基、开发规矩、项目初始化
- Pre-MVP Readiness Audit：9 步审查通过
- Frontend Design：674 行静态工单工作台（已冻结为 legacy）
- Backend Init：FastAPI health API + 2 个测试通过

## 4. 核心文档

| 文档 | 说明 | 状态 |
|------|------|------|
| `docs/00_SCOPE_LOCK.md` | 项目边界锁定 | ✅ M0 新增, M6.5 更新 |
| `docs/01_ACCEPTANCE_CRITERIA.md` | 验收标准 | ✅ M0 新增 |
| `docs/02_RAG_DESIGN.md` | RAG 设计 | ✅ M0 新增, M6.5 更新 |
| `docs/03_EVAL_DESIGN.md` | Eval 设计 | ✅ M0 新增 |
| `docs/ROADMAP_V2.md` | 开发路线 | ✅ M0 新增 |
| `docs/AGENT_WORKFLOW.md` | Agent Workflow 设计 | ✅ M6.5 新增 |
| `backend/app/rag/schemas.py` | 数据模型 | ✅ M1 新增, M2 扩展, M3 扩展 |
| `backend/app/rag/loader.py` | JSONL 加载器 | ✅ M2 新增 |
| `backend/app/rag/chunker.py` | 文档切分器 | ✅ M2 新增 |
| `backend/app/rag/retriever.py` | BM25 检索器 | ✅ M3 新增 |
| `backend/app/eval/retrieval_eval.py` | 检索评测 harness | ✅ M4 新增 |
| `backend/app/rag/optimized_retriever.py` | 优化检索器 | ✅ M5 新增 |
| `backend/data/knowledge_base/customer_service_seed.jsonl` | 种子知识库 | ✅ M1 新增 |
| `backend/data/eval_cases_seed.jsonl` | 种子评测集 | ✅ M1 新增 |
| `backend/data/eval_cases_full.jsonl` | 全量评测集 | ✅ M6 新增 |
| `docs/BAD_CASE_OPTIMIZATION_LOG.md` | Bad case 优化日志 | ✅ M6 新增 |
| `docs/EVAL_REPORT_M6.md` | M6 评测报告 | ✅ M6 新增 |
| `docs/EVAL_REPORT_M8.md` | M8 answer quality 评测报告 | ✅ M8 新增 |
| `docs/EVAL_REPORT_M9.md` | M9 answer quality 评测报告 | ✅ M9 新增 |
| `docs/EVAL_REPORT_M9_5.md` | M9.5 answer quality 评测报告 | ✅ M9.5 新增 |
| `docs/ANSWER_WORKFLOW_OPTIMIZATION_LOG.md` | Answer workflow 优化日志 | ✅ M9 新增, M9.5 更新 |
| `backend/tests/test_data_schema.py` | 数据校验测试 | ✅ M1 新增 |
| `backend/tests/test_loader_chunker.py` | loader/chunker 测试 | ✅ M2 新增 |
| `backend/tests/test_retriever.py` | retriever 测试 | ✅ M3 新增 |
| `backend/tests/test_retrieval_eval.py` | retrieval eval 测试 | ✅ M4 新增 |
| `backend/tests/test_optimized_retriever.py` | optimized retriever 测试 | ✅ M5 新增 |
| `backend/tests/test_full_eval_dataset.py` | full eval dataset 测试 | ✅ M6 新增 |
| `backend/app/api/agent.py` | Agent Chat API router | ✅ M10 新增 |
| `backend/tests/test_agent_api.py` | agent API 测试 | ✅ M10 新增 |
| `docs/API_SMOKE_DEMO.md` | API smoke demo 文档 | ✅ M10 新增 |

## 5. 下一步

**可选后续工作：**

- **M11.5: Final LLM Adapter Release Checklist** — 验证 mock 默认、optional real LLM、文档与 tag
- **M12: Real Logistics Adapter** — 连接真实物流追踪 API，替换 mock logistics tool
- **Frontend Integration** — 连接 React 前端到 FastAPI 后端，实现聊天 UI
- **Deployment** — 部署到云平台（AWS/GCP/Azure），配置生产环境

**当前已完成：**
- ✅ M11 Optional Real LLM Adapter
- ✅ M10.5 Final Release Checklist
- ✅ Release tag: v1.0.1-demo

## 6. 风险点

| 风险 | 说明 | 控制方式 |
|------|------|---------|
| 为 20 条 seed cases 过拟合 | optimized retriever 可能针对 seed set 写死规则 | 防作弊测试 + 通用词典 + 无 case_id 硬编码 |
| 通过 case_id 或 expected_doc_ids 硬编码 | 作弊提升指标 | 静态检查 optimized_retriever.py 不包含 eval 字段 |
| boost 太大导致 BM25 失真 | metadata boost 覆盖关键词相关性 | boost 保守（max ×1.41），可解释 |
| optimized 覆盖 baseline | 无法对比 | 保留 baseline retriever.py 不变 |
| 只提升 Recall@5，不关注 Recall@1 / MRR | Top-5 命中但 Top-1 未命中 | 同时监控 Recall@1 和 MRR |
| 忘记输出仍失败的 cases | 无法定位下一步优化方向 | eval harness 必须输出 failed_cases |
| full dataset 过于简单 | 122 条可能不够复杂 | 覆盖 hard(31) / medium(75) / 多意图 / 跨语言 |
| expected_doc_ids 标注不准确 | 影响指标可信度 | 数据质量测试 + 人工抽检 |
| optimized 过拟合 seed set | full set 指标可能下降 | 用 full set 结果而非 seed set |
| 只看 Recall@5，不看 Recall@1 / MRR | 排序质量未被评估 | 同时监控三个指标 |
| retrieval 指标 ≠ 回答质量指标 | 高 Recall 不等于好回答 | M8 实现 answer quality evaluation |
| 把 retrieval 指标误当 answer 指标 | 高 Recall@5 不代表好回答 | M8 独立评估 answer 质量 |
| 为分数修改评测规则 | 美化结果 | 评测规则固定，不针对 workflow 调整 |
| mock answer 被误认为真实 LLM | 结果不代表 LLM 质量 | EVAL_REPORT_M8.md 明确标注 mock |
| logistics tool 被误认为真实 API | 结果不代表真实物流 | EVAL_REPORT_M8.md 明确标注 mock |
| expected_keywords 泄露进 agent workflow | 作弊 | 静态检查 agent 模块不包含 eval 字段 |
| public docs 混入非公开内容 | 违反公开文档规范 | 静态测试扫描禁用关键词 |
| 为指标修改 answer_eval | 美化结果 | 评测规则固定，不针对 workflow 调整 |
| 规则过拟合 full eval set | 通用性下降 | 通用规则，不针对 case_id 写死 |
| mock answer 被误认为真实 LLM | 结果不代表 LLM 质量 | EVAL_REPORT 明确标注 mock |
| API 被误认为接了真实 LLM | API 只包装 mock workflow | API_SMOKE_DEMO.md 明确标注 mock |
| mock logistics tool 被误认为真实物流 API | 物流数据是模拟的 | API_SMOKE_DEMO.md 明确标注 mock |
| local-only study notes 被提交 | RAG_HANDS_ON_REVIEW.md 不应进入 Git | .git/info/exclude + 静态检查 |
| public docs 混入非公开内容 | 违反公开文档规范 | 静态测试扫描禁用关键词 |

## 7. 当前禁止事项

- ❌ 不碰前端
- ❌ 不把 optional LLM adapter 包装成生产级上线
- ❌ 不实现 6 Agent 工单编排
- ❌ 不实现 LangGraph 多 Agent
- ❌ 不实现登录/权限/多租户
- ❌ 不在 optimized retriever 中使用 eval ground-truth 数据
- ❌ 不实现真实订单查询 / 物流 API
