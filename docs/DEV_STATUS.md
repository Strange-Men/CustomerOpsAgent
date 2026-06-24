# CustomerOps Agent｜开发状态

## 1. 当前阶段

**M4: Retrieval Evaluation Harness**

## 2. 当前项目状态

**状态：M4 retrieval evaluation harness 完成**

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
- ❌ 尚未实现 optimized retriever
- ❌ 尚未实现 answer generator
- ❌ 尚未实现 RAG API

## 3. 已完成内容

### M4：Retrieval Evaluation Harness（本轮）

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
| `backend/data/knowledge_base/customer_service_seed.jsonl` | 种子知识库 | ✅ M1 新增 |
| `backend/data/eval_cases_seed.jsonl` | 种子评测集 | ✅ M1 新增 |
| `backend/tests/test_data_schema.py` | 数据校验测试 | ✅ M1 新增 |
| `backend/tests/test_loader_chunker.py` | loader/chunker 测试 | ✅ M2 新增 |
| `backend/tests/test_retriever.py` | retriever 测试 | ✅ M3 新增 |
| `backend/tests/test_retrieval_eval.py` | retrieval eval 测试 | ✅ M4 新增 |

## 5. 下一步

**进入 M5：optimized retriever**

M5 目标：
- 通过 metadata filter / query rewrite / synonym expansion 提升 Recall@5
- 目标 Recall@5 ≥ 85%

## 6. 风险点

| 风险 | 说明 | 控制方式 |
|------|------|---------|
| eval harness 把 expected_doc_ids 传给 retriever | 检索器作弊，指标虚高 | 防作弊测试检查 search 只接收 query + top_k |
| retriever 偷看 eval cases | retriever.py 被注入 eval 信息 | 静态检查 retriever.py 不包含 eval_cases / expected_doc_ids |
| baseline Recall@5 低但误以为项目失败 | baseline 是基准不是目标 | 明确 M4 只记录 baseline，M5 才优化 |
| 不输出 failed cases | M5 没有优化方向 | evaluate_retriever 必须输出 failed_cases |
| evaluation 和 retriever 耦合太深 | 修改 retriever 影响 eval | eval 层只调用 search，不修改 retriever 内部 |
| 同一 doc 多个 chunk 重复影响评估 | hit 虚高 | unique_doc_ids_from_results 去重 |

## 7. 当前禁止事项

- ❌ 不继续扩写大文档
- ❌ 不碰前端
- ❌ 不写 optimized retriever（M5 才做）
- ❌ 不写 answer generator
- ❌ 不接 LLM API
- ❌ 不实现 6 Agent 工单编排
- ❌ 不实现登录/权限/多租户
