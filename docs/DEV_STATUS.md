# CustomerOps Agent｜开发状态

## 1. 当前阶段

**M5: Optimized Retriever**

## 2. 当前项目状态

**状态：M5 optimized retriever 完成**

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
- ✅ baseline vs optimized 对比（Recall@5: 90%→100%, MRR: 0.785→0.917）
- ✅ optimized retriever 测试（test_optimized_retriever.py, 14 个测试用例）
- ✅ CLI smoke test
- ❌ 尚未实现 answer generator
- ❌ 尚未实现 RAG API

## 3. 已完成内容

### M5：Optimized Retriever（本轮）

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
| `docs/00_SCOPE_LOCK.md` | 项目边界锁定 | ✅ M0 新增 |
| `docs/01_ACCEPTANCE_CRITERIA.md` | 验收标准 | ✅ M0 新增 |
| `docs/02_RAG_DESIGN.md` | RAG 设计 | ✅ M0 新增 |
| `docs/03_EVAL_DESIGN.md` | Eval 设计 | ✅ M0 新增 |
| `docs/ROADMAP_V2.md` | 开发路线 | ✅ M0 新增 |
| `backend/app/rag/schemas.py` | 数据模型 | ✅ M1 新增, M2 扩展, M3 扩展 |
| `backend/app/rag/loader.py` | JSONL 加载器 | ✅ M2 新增 |
| `backend/app/rag/chunker.py` | 文档切分器 | ✅ M2 新增 |
| `backend/app/rag/retriever.py` | BM25 检索器 | ✅ M3 新增 |
| `backend/app/eval/retrieval_eval.py` | 检索评测 harness | ✅ M4 新增 |
| `backend/app/rag/optimized_retriever.py` | 优化检索器 | ✅ M5 新增 |
| `backend/data/knowledge_base/customer_service_seed.jsonl` | 种子知识库 | ✅ M1 新增 |
| `backend/data/eval_cases_seed.jsonl` | 种子评测集 | ✅ M1 新增 |
| `backend/tests/test_data_schema.py` | 数据校验测试 | ✅ M1 新增 |
| `backend/tests/test_loader_chunker.py` | loader/chunker 测试 | ✅ M2 新增 |
| `backend/tests/test_retriever.py` | retriever 测试 | ✅ M3 新增 |
| `backend/tests/test_retrieval_eval.py` | retrieval eval 测试 | ✅ M4 新增 |
| `backend/tests/test_optimized_retriever.py` | optimized retriever 测试 | ✅ M5 新增 |

## 5. 下一步

**进入 M6：扩展 120+ bad cases + bad case optimization log**

M6 目标：
- 扩展 120+ bad cases，形成更可信的最终评测集
- 记录 bad case optimization log

## 6. 风险点

| 风险 | 说明 | 控制方式 |
|------|------|---------|
| 为 20 条 seed cases 过拟合 | optimized retriever 可能针对 seed set 写死规则 | 防作弊测试 + 通用词典 + 无 case_id 硬编码 |
| 通过 case_id 或 expected_doc_ids 硬编码 | 作弊提升指标 | 静态检查 optimized_retriever.py 不包含 eval 字段 |
| boost 太大导致 BM25 失真 | metadata boost 覆盖关键词相关性 | boost 保守（max ×1.41），可解释 |
| optimized 覆盖 baseline | 无法对比 | 保留 baseline retriever.py 不变 |
| 只提升 Recall@5，不关注 Recall@1 / MRR | Top-5 命中但 Top-1 未命中 | 同时监控 Recall@1 和 MRR |
| 忘记输出仍失败的 cases | 无法定位下一步优化方向 | eval harness 必须输出 failed_cases |
| 扩展 120+ bad cases 后指标下降 | seed set 过拟合暴露 | M6 以完整 eval set 为准 |

## 7. 当前禁止事项

- ❌ 不继续扩写大文档
- ❌ 不碰前端
- ❌ 不写 answer generator（M7 才做）
- ❌ 不接 LLM API
- ❌ 不实现 6 Agent 工单编排
- ❌ 不实现登录/权限/多租户
- ❌ 不在 optimized retriever 中使用 eval ground-truth 数据
