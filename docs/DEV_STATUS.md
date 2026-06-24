# CustomerOps Agent｜开发状态

## 1. 当前阶段

**M3: Baseline BM25 Retriever**

## 2. 当前项目状态

**状态：M3 baseline BM25 retriever 完成**

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
- ❌ 尚未实现 retrieval evaluation harness
- ❌ 尚未实现 answer generator
- ❌ 尚未实现 RAG API

## 3. 已完成内容

### M3：Baseline BM25 Retriever（本轮）

- ✅ 修改 `backend/app/rag/schemas.py`
  - 新增 RetrievedChunk 模型（12 字段）
  - 保留 KnowledgeChunk 完整 metadata + score 字段
  - score >= 0，类型为 float

- ✅ 创建 `backend/app/rag/retriever.py`
  - `tokenize(text)` — 英文小写分词 + CJK 字符级 bigram
  - `BM25Retriever(chunks)` — 自实现 BM25 检索器
  - `BM25Retriever.search(query, top_k)` — Top-K 检索，按 score 降序
  - `build_default_retriever()` — 从默认知识库构建 retriever
  - CLI: `python -m app.rag.retriever "query"` — CLI smoke test
  - 标准 BM25 公式：TF * IDF / (TF + k1 * (1 - b + b * dl/avgdl))
  - k1=1.5, b=0.75

- ✅ 创建 `backend/tests/test_retriever.py`
  - 12 个测试用例，覆盖：英文 tokenize、中文 tokenize、空 chunks、空 query、top-k 排序、metadata 保留、seed KB 检索、防作弊检查、top-k 限制、score 非负、top_k=0 抛异常、英文查询

### M2：Loader + Chunker

- ✅ 修改 `backend/app/rag/schemas.py`
  - 新增 KnowledgeChunk 模型（11 字段）
  - chunk_id / doc_id / title / category / market / language / policy_type / priority / source / content / chunk_index
  - chunk_id 不能为空，chunk_index >= 0，content 不能为空

- ✅ 创建 `backend/app/rag/loader.py`
  - `load_jsonl(path)` — 逐行加载 JSONL，空行跳过，坏 JSON 报行号
  - `load_knowledge_documents(path)` — 加载并校验为 KnowledgeDocument 列表
  - `get_default_knowledge_path()` — 返回默认 seed 知识库路径
  - CLI: `python -m app.rag.loader` — 输出文档数量、语言分布、category 分布

- ✅ 创建 `backend/app/rag/chunker.py`
  - `split_text_by_chars(text, max_chars, overlap)` — 按字符切分文本
  - `chunk_document(doc, max_chars, overlap)` — 单文档切分
  - `chunk_documents(docs, max_chars, overlap)` — 批量切分
  - 默认 max_chars=320, overlap=40
  - chunk_id 格式: `{doc_id}::chunk_{index:03d}`
  - CLI: `python -m app.rag.chunker` — 输出文档数、chunks 数、平均长度

- ✅ 创建 `backend/tests/test_loader_chunker.py`
  - 11 个测试用例，覆盖：加载、metadata 保留、短文档单 chunk、长文档多 chunk、overlap、chunk_id 稳定、坏 JSON 行号、非法参数、语言/市场保留

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
| `backend/data/knowledge_base/customer_service_seed.jsonl` | 种子知识库 | ✅ M1 新增 |
| `backend/data/eval_cases_seed.jsonl` | 种子评测集 | ✅ M1 新增 |
| `backend/tests/test_data_schema.py` | 数据校验测试 | ✅ M1 新增 |
| `backend/tests/test_loader_chunker.py` | loader/chunker 测试 | ✅ M2 新增 |
| `backend/tests/test_retriever.py` | retriever 测试 | ✅ M3 新增 |

## 5. 下一步

**进入 M4：retrieval evaluation harness**

M4 目标：
- 实现 retrieval evaluation harness
- 计算 baseline Recall@1/3/5 与 MRR
- 为 M5 optimized retriever 提供基准指标

## 6. 风险点

| 风险 | 说明 | 控制方式 |
|------|------|---------|
| baseline retriever 偷看 eval cases | 检索结果被 expected_doc_ids 污染 | 测试检查 retriever.py 不包含 eval_cases / expected_doc_ids |
| 过早加入 optimized 策略 | 边界失控，M3 只做 baseline BM25 | 代码审查不包含 synonym/query rewrite/embedding |
| 中文 tokenizer 过度复杂 | 引入 jieba 等外部依赖 | 测试覆盖简单 CJK 字符级 token |
| BM25 score 排序错误 | 检索结果顺序不对 | 测试检查 score 降序 |
| 检索结果丢 metadata | RetrievedChunk 缺字段 | 测试覆盖所有 metadata 字段 |
| top_k 边界处理不清晰 | top_k=0 或负数行为不确定 | top_k<=0 抛 ValueError，测试覆盖 |

## 7. 当前禁止事项

- ❌ 不继续扩写大文档
- ❌ 不碰前端
- ❌ 不写 optimized retriever
- ❌ 不写 answer generator
- ❌ 不接 LLM API
- ❌ 不实现 6 Agent 工单编排
- ❌ 不实现登录/权限/多租户
