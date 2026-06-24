# CustomerOps Agent｜开发状态

## 1. 当前阶段

**M2: Loader + Chunker**

## 2. 当前项目状态

**状态：M2 loader + chunker 完成**

- ✅ 项目方向重锁为 RAG + Eval（M0）
- ✅ 前端冻结为 legacy/static demo（M0）
- ✅ 边界锁定文档（00_SCOPE_LOCK.md）
- ✅ 验收标准文档（01_ACCEPTANCE_CRITERIA.md）
- ✅ RAG 设计文档（02_RAG_DESIGN.md）
- ✅ Eval 设计文档（03_EVAL_DESIGN.md）
- ✅ ROADMAP_V2 后端优先开发路线（M0-M11）
- ✅ Pydantic schema 定义（schemas.py: KnowledgeDocument + EvalCase + KnowledgeChunk）
- ✅ Seed knowledge base（14 条知识文档）
- ✅ Seed eval cases（20 条评测用例）
- ✅ 数据 schema 测试（test_data_schema.py）
- ✅ JSONL loader（loader.py）
- ✅ KnowledgeChunk chunker（chunker.py）
- ✅ loader + chunker 测试（test_loader_chunker.py）
- ❌ 尚未实现 retriever
- ❌ 尚未实现 evaluation harness
- ❌ 尚未实现 answer generator
- ❌ 尚未实现 RAG API

## 3. 已完成内容

### M2：Loader + Chunker（本轮）

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
| `backend/app/rag/schemas.py` | 数据模型 | ✅ M1 新增, M2 扩展 |
| `backend/app/rag/loader.py` | JSONL 加载器 | ✅ M2 新增 |
| `backend/app/rag/chunker.py` | 文档切分器 | ✅ M2 新增 |
| `backend/data/knowledge_base/customer_service_seed.jsonl` | 种子知识库 | ✅ M1 新增 |
| `backend/data/eval_cases_seed.jsonl` | 种子评测集 | ✅ M1 新增 |
| `backend/tests/test_data_schema.py` | 数据校验测试 | ✅ M1 新增 |
| `backend/tests/test_loader_chunker.py` | loader/chunker 测试 | ✅ M2 新增 |

## 5. 下一步

**进入 M3：baseline BM25 retriever**

M3 目标：
- 在 chunks 上实现 BM25 关键词检索
- 支持 Top-K 返回
- 为 M4 prompt builder 提供检索结果

## 6. 风险点

| 风险 | 说明 | 控制方式 |
|------|------|---------|
| chunking 丢 metadata | chunk 切分后 metadata 丢失 | 测试已覆盖 metadata 保留 |
| chunk_id 不稳定 | chunk_id 在不同运行间变化 | chunk_id 格式固定为 {doc_id}::chunk_{index:03d} |
| chunk 太大或太小 | max_chars 设置不当 | 默认 320 字符，overlap 40，可调参数 |
| loader 吞异常 | 数据问题难排查 | loader 逐行报行号，不吞异常 |
| 提前把 retriever 写进 M2 | 边界失控 | M2 严格只做 loader + chunker |

## 7. 当前禁止事项

- ❌ 不继续扩写大文档
- ❌ 不碰前端
- ❌ 不写 retriever
- ❌ 不写 evaluation harness
- ❌ 不写 answer generator
- ❌ 不接 LLM API
- ❌ 不实现 6 Agent 工单编排
- ❌ 不实现登录/权限/多租户
