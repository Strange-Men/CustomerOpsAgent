# CustomerOps Agent｜修正版开发路线 v2

**日期**：2026-06-24
**依据**：简历定位修正 + 两天 MVP 约束 + 前端工作流

---

## 一、项目现状审计

### 1.1 已有资产

| 资产 | 状态 | 处置 |
|------|------|------|
| `backend/app/main.py` | FastAPI 骨架 + health endpoint | 保留，扩展 |
| `backend/app/api/routes_health.py` | GET /health | 保留 |
| `backend/tests/test_health.py` | 2 个测试通过 | 保留 |
| `backend/requirements.txt` | 8 个基础依赖 | 扩展 |
| `frontend/app/page.tsx` | 674 行静态工单工作台 | **冻结，标记 legacy** |
| `frontend/` 整体 | Next.js 16 + Tailwind | **冻结** |
| `docs/` 7 个核心文档 | 方向偏"6 Agent 工单系统" | **不删除，归档为 v1 参考** |
| `docs/archive/planning/` | 13 个规划文档 | 保留不动 |
| `.claude/skills/frontend-design/` | 官方设计 skill | 保留，M11 可选前端时使用 |

### 1.2 核心偏差

| 维度 | 当前方向 | 简历需要的方向 |
|------|---------|---------------|
| 核心能力 | 6 Agent 工单编排 | RAG 知识库 + Retrieval 优化 + Eval Harness |
| 前端重点 | 工单分析工作台 | Chat Demo + Eval Report + Bad Case Compare |
| 检索描述 | "关键词匹配" | BM25 baseline → 优化策略 → Recall@5 提升 |
| 评估方式 | 固定用例执行 | Retrieval Eval + Answer Eval 双层评测框架 |
| 数据规模 | 10 条示例工单 | 20 seed → 120+ bad cases，带分类/难度/优化日志 |

### 1.3 不删除任何文件

所有现有文件保留。新文档在 `docs/` 下新增，不覆盖旧文档。

---

## 二、前端最终策略

### 2.1 冻结声明

`frontend/app/page.tsx` 及其依赖文件（layout.tsx, globals.css, lib/api.ts）**冻结为 legacy/static demo**。

- 不删除
- 不修改
- 不扩展
- 不修 bug（如果有）
- 保留可 build 状态

### 2.2 可选极简前端（M11，仅后端闭环后）

如果后端 RAG + Eval 核心闭环完成，按前端工作流做极简演示页：

| 页面 | 内容 | 禁止内容 |
|------|------|---------|
| Chat Demo | 输入问题 → answer + citations + retrieved chunks | 无登录、无权限、无订单系统 |
| Eval Report | Recall@5 / Answer Pass Rate / Groundedness / Bad Case 数 | 无复杂 Dashboard、无动画 |
| Bad Case Compare | baseline vs optimized 差异对比 | 无工单后台、无多租户 |

### 2.3 前端工作流要求（M11 如触发）

1. 先写前端设计文档（1 页）
2. 审查通过后才写代码
3. 使用 `.claude/skills/frontend-design/SKILL.md`
4. 单页面不超过 300 行
5. 只用 Tailwind + 系统字体
6. 不引入新 UI 库

---

## 三、后端优先开发顺序（M0-M11）

### 阶段总览

```
M0  边界重锁 + 冻结前端 + 最小文档补档          [~2h]
M1  知识库 schema + 20 条 seed eval cases        [~2h]
M2  loader + chunker                             [~2h]
M3  baseline BM25 retriever                      [~2h]
M4  retrieval evaluation harness                 [~2h]
M5  optimized retriever                          [~3h]
M6  扩展 120+ bad cases + optimization log       [~2h]
M7  prompt builder + mock answer generator       [~2h]
M8  answer evaluation harness                    [~2h]
M9  FastAPI API 集成                             [~2h]
M10 README / ARCHITECTURE / EVAL_REPORT          [~2h]
M11 可选极简前端（仅后端闭环后）                   [~3h]
```

**两天时间分配**：
- Day 1：M0-M4（检索闭环 + Retrieval Eval）
- Day 2：M5-M9（优化 + Answer Eval + API）+ M10 文档

### 检索方案设计

```
Baseline（M3）：
  └─ BM25 / 关键词检索
  └─ 可解释、可调试
  └─ 作为 Recall@5 的基线数值

Optimized（M5）：
  ├─ BM25（保留）
  ├─ + metadata filter（category, market, language）
  ├─ + synonym expansion（同义词映射表）
  ├─ + query rewrite（规则化 query 改写）
  └─ + optional embedding adapter（mock/stub，保留接口）

检索方案设计原则：先建立可解释 baseline，再通过可控优化策略提升 Top-5 Recall，而不是一开始堆复杂框架。embedding adapter 作为可选增强，接口已预留但 MVP 用 stub 实现。
```

### 知识库 Metadata Schema（分层知识库定义）

```
知识库文档 metadata 必须包含以下字段（YAML frontmatter）：

| 字段         | 类型   | 说明                          | 示例值                  |
|-------------|--------|-----------------------------|------------------------|
| doc_id      | string | 唯一标识                      | "POL-LOGISTICS-001"    |
| title       | string | 文档标题                      | "跨境物流配送政策"        |
| category    | string | 分类                          | "logistics"            |
| market      | string | 目标市场                      | "US" / "EU" / "SEA"    |
| language    | string | 语言代码                      | "zh" / "en"            |
| policy_type | string | 政策类型                      | "shipping" / "return"  |
| priority    | int    | 优先级（1=高, 2=中, 3=低）     | 1                      |
| source      | string | 来源                          | "official_2026Q1"      |

content 为 Markdown 正文，不放在 frontmatter 中。

知识库按 category、market、language、policy_type 做分层，检索时通过 metadata filter 提升召回准确率。
```

### 多语种知识库快速迁移

```
简历表述："支持多语种知识库快速迁移"

落地要求：
  1. knowledge_base 文档必须包含 language 字段
  2. eval_cases 必须包含 language 字段
  3. 至少包含 zh / en 两种语言样例
  4. retriever 支持 language filter（metadata filter 的一部分）
  5. README 需要说明如何迁移到新的语种知识库
  6. 不需要做复杂翻译服务，只需数据结构和检索接口支持多语种迁移

迁移流程（M10 README 中说明）：
  1. 在 backend/data/knowledge_base/{language}/ 下新增对应语种 .md 文件
  2. frontmatter 中设置 language 字段
  3. 新增对应的 eval cases（含 language 字段）
  4. retriever 的 metadata filter 自动支持新语种，无需改代码
```

### 数据集策略

```
M1：20 条 seed eval cases
  ├─ 覆盖：物流、清关、退货、退款、换货、支付、地址修改、取消订单、多语言咨询
  ├─ 字段：query, expected_doc_ids, expected_keywords, category, difficulty, market, language
  ├─ 至少包含 zh / en 两种语言样例
  └─ 目的：跑通 loader → chunker → retriever → retrieval eval 闭环

M6：扩展到 120+ bad cases
  ├─ 在 seed 基础上增加边界 case、难 case、多语言 case
  ├─ 新增字段：bad_case_type, optimization_notes
  └─ 必须保留 bad_case_optimization_log.md
```

### Evaluation 顺序

```
先做 Retrieval Evaluation（M4）：
  ├─ Recall@1
  ├─ Recall@3
  ├─ Recall@5
  ├─ MRR（可选）
  └─ 每个 case 输出 expected_doc_ids vs retrieved_doc_ids 命中情况

再做 Answer Evaluation（M8）：
  ├─ 三大评估维度（对应简历"从三个维度自动批量化评估回答质量"）：
  │   ├─ Relevance：回答是否切题
  │   ├─ Groundedness：回答是否基于知识库，是否减少幻觉
  │   └─ Completeness：回答是否覆盖关键处理步骤
  ├─ 辅助指标：
  │   ├─ Citation Hit Rate：citations 中有多少命中 expected_doc_ids
  │   ├─ Keyword Coverage：expected_keywords 在回答中的覆盖率
  │   └─ Answer Pass Rate：通过的 case 占比（核心汇总指标）
  └─ 注意：不要把 6 个指标都称为 6 个维度，简历写的是"三个维度"

这个顺序对应简历："top-5 知识召回准确率提升至 85%"
```

---

## 四、两天 MVP 结束标准

### 简历指标口径说明

```
简历简写："高频咨询场景回答合格率提升 30%"
严谨表述："高频咨询场景回答合格率从 55% 提升到 85%，提升 30 个百分点"

注意区分：
  - "提升 30%" 是相对提升（55% × 1.3 = 71.5%），口径不同
  - "提升 30 个百分点" 是绝对提升（55% + 30pp = 85%）
  - 项目报告、EVAL_REPORT、面试口述统一使用"30 个百分点"
  - README 可保留"提升 30%"作为简历简写，但需注明口径
```

### 4.1 必须完成（面试可投入）

| # | 标准 | 验收方式 |
|---|------|---------|
| 1 | 20 条 seed eval cases 存在且有分类字段 | `python -m pytest backend/tests/test_eval_cases.py` |
| 2 | loader + chunker 可将 Markdown 知识库切分为 chunks | `python -m pytest backend/tests/test_chunker.py` |
| 3 | baseline BM25 retriever 可检索 | `python -m pytest backend/tests/test_retriever.py` |
| 4 | Retrieval Eval 可计算 Recall@5 | `python -m pytest backend/tests/test_retrieval_eval.py` |
| 5 | optimized retriever Recall@5 ≥ 85% | `python -m pytest backend/tests/test_retrieval_eval.py -k optimized` |
| 6 | 120+ bad cases 存在且有优化日志 | `ls backend/data/eval/bad_cases.json` + `docs/BAD_CASE_LOG.md` |
| 7 | mock answer generator 可生成带 citations 的回答 | `python -m pytest backend/tests/test_answer_gen.py` |
| 8 | Answer Eval 可计算 6 个指标 | `python -m pytest backend/tests/test_answer_eval.py` |
| 9 | FastAPI /api/retrieve + /api/answer + /api/eval 端点可用 | `curl localhost:8000/api/health` |
| 10 | 全部测试通过 | `python -m pytest backend` |
| 11 | ruff check 通过 | `python -m ruff check backend` |

### 4.2 可选完成（加分项）

| # | 标准 | 条件 |
|---|------|------|
| 12 | 极简 Chat Demo 前端 | M11，仅 M1-M10 全部完成后 |
| 13 | Eval Report 页面 | M11，同上 |
| 14 | embedding adapter stub | M5，接口保留即可 |

### 4.3 不做清单

- ❌ 不做 6 Agent 工单编排
- ❌ 不做登录/权限/多租户
- ❌ 不做真实 LLM 调用
- ❌ 不做向量数据库
- ❌ 不做 Docker 部署
- ❌ 不做复杂前端 Dashboard
- ❌ 不做订单/物流真实 API
- ❌ 不做前端工单系统

---

## 五、阶段详情

### M0：边界重锁 + 冻结前端 + 最小文档补档

**本轮目标**：
1. 锁定项目边界为 RAG + Eval，冻结前端
2. 补 5 个最小必要文档
3. 不写业务代码

**修改文件**：
- `docs/00_SCOPE_LOCK.md`（新增）
- `docs/01_ACCEPTANCE_CRITERIA.md`（新增）
- `docs/02_RAG_DESIGN.md`（新增）
- `docs/03_EVAL_DESIGN.md`（新增）
- `docs/DEV_STATUS.md`（更新当前状态）
- `docs/CHANGELOG.md`（追加 M0 记录）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/` 全部不动（M0 不写代码）
- `README.md` 暂不更新（M10 统一更新）
- `docs/archive/` 不动

**验收命令**：
```bash
# 确认新文档存在
ls docs/00_SCOPE_LOCK.md docs/01_ACCEPTANCE_CRITERIA.md docs/02_RAG_DESIGN.md docs/03_EVAL_DESIGN.md

# 确认 backend 测试仍通过
conda run -n customerops-agent python -m pytest backend

# 确认 frontend 仍可 build
cd frontend && npm run build

# 确认 git 状态
git status
```

**我应该 Review 哪些代码**：
- 本轮无代码，Review 5 个新文档的内容
- 重点看 00_SCOPE_LOCK.md 的边界定义是否清晰
- 重点看 03_EVAL_DESIGN.md 的指标是否覆盖简历要求

**对应 RAG 基础知识点**：
- 项目边界定义（Scope Management）
- RAG 系统架构设计（Retrieval → Generation → Evaluation 三层）
- Evaluation 指标设计（Recall@K, Groundedness, Relevance）

**如果写错，面试时会被怎么追问**：
- "你的 Recall@5 具体是怎么计算的？expected_doc_ids 从哪来？"
- "你为什么先做 Answer Eval 再做 Retrieval Eval？这不是反了吗？"
- "你的 embedding adapter 接口设计是什么？为什么不用向量检索？"

**是否需要 git commit / tag**：
- ✅ commit: `docs: add scope lock and RAG/eval design docs`
- ✅ tag: `m0-scope-locked`

---

### M1：知识库 schema + 20 条 seed eval cases

**本轮目标**：
1. 设计知识库文档 schema（Markdown + metadata frontmatter）
2. 创建 20 条高质量 seed eval cases
3. 覆盖 10 个核心场景

**修改文件**：
- `backend/data/knowledge_base/`（新增目录 + 6 个 .md 知识库文件）
- `backend/data/eval/seed_eval_cases.json`（新增）
- `backend/app/schemas/knowledge.py`（新增 Pydantic schema）
- `backend/app/schemas/eval_case.py`（新增 Pydantic schema）
- `backend/tests/test_eval_cases.py`（新增）
- `backend/tests/test_knowledge_schema.py`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/main.py`（M1 不改 API）
- `docs/00_SCOPE_LOCK.md`（已锁定）

**验收命令**：
```bash
# 知识库文件存在
ls backend/data/knowledge_base/*.md

# eval cases 文件存在且可解析
python -c "import json; cases=json.load(open('backend/data/eval/seed_eval_cases.json')); print(f'{len(cases)} cases loaded')"

# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_eval_cases.py backend/tests/test_knowledge_schema.py

# ruff 通过
conda run -n customerops-agent python -m ruff check backend
```

**我应该 Review 哪些代码**：
1. `knowledge.py` 的 schema：metadata 字段是否包含 doc_id, title, category, market, language, policy_type, priority, source？
2. `eval_case.py` 的 schema：是否包含 expected_doc_ids, expected_keywords, category, difficulty, language？
3. `seed_eval_cases.json`：20 条是否覆盖物流/清关/退货/退款/换货/支付/地址修改/取消订单/多语言？是否包含 zh/en 两种语言？
4. 知识库 .md 文件：frontmatter 格式是否一致？language 字段是否存在？

**对应 RAG 基础知识点**：
- Knowledge Base 设计（文档结构、metadata 索引）
- Chunking 策略前置（文档粒度设计影响 chunk 质量）
- Evaluation Dataset 设计（seed cases 的覆盖度和质量 > 数量）

**如果写错，面试时会被怎么追问**：
- "你的 knowledge base 为什么选 Markdown 而不是数据库？"
- "expected_doc_ids 是怎么确定的？谁标注的？"
- "20 条 seed cases 够不够？怎么保证覆盖度？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add knowledge base schema and 20 seed eval cases`
- ✅ tag: `m1-kb-and-seed-cases`

---

### M2：loader + chunker

**本轮目标**：
1. 实现 Markdown loader（读取 .md + frontmatter metadata）
2. 实现 chunker（按段落/标题切分，保留 metadata）
3. 每个 chunk 必须携带 doc_id, category, market, language, chunk_index

**修改文件**：
- `backend/app/rag/loader.py`（新增）
- `backend/app/rag/chunker.py`（新增）
- `backend/tests/test_loader.py`（新增）
- `backend/tests/test_chunker.py`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/main.py`（M2 不改 API）
- `backend/data/`（数据文件不动）

**验收命令**：
```bash
# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_loader.py backend/tests/test_chunker.py

# 手动验证 chunk 输出
python -c "
from app.rag.loader import load_knowledge_base
from app.rag.chunker import chunk_documents
docs = load_knowledge_base('backend/data/knowledge_base')
chunks = chunk_documents(docs)
print(f'{len(docs)} docs → {len(chunks)} chunks')
print(chunks[0].metadata)
"
```

**我应该 Review 哪些代码**：
1. `loader.py`：是否正确解析 YAML frontmatter？metadata 有没有丢失？
2. `chunker.py`：chunk 边界在哪？是否按标题切分？chunk 大小范围？
3. metadata 传递：doc_id / category / market / language 是否从 doc → chunk 一路传下去？
4. 边界 case：空文档、无 frontmatter 文档、超长段落怎么处理？

**对应 RAG 基础知识点**：
- Document Loading（Markdown 解析、metadata 提取）
- Text Splitting（chunking 策略：按段落 vs 按 token vs 按语义）
- Metadata Propagation（metadata 必须从文档级传递到 chunk 级）

**如果写错，面试时会被怎么追问**：
- "你的 chunking 策略是什么？为什么选这个粒度？"
- "chunk 之间有没有重叠？为什么有/没有？"
- "metadata 是怎么从文档传到 chunk 的？如果丢了怎么办？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add markdown loader and chunker with metadata propagation`
- ✅ tag: `m2-loader-chunker`

---

### M3：baseline BM25 retriever

**本轮目标**：
1. 实现 BM25 baseline retriever
2. 输入：query string → 输出：top-k chunks with scores
3. 不做任何优化，纯 BM25 作为可解释基线

**修改文件**：
- `backend/app/rag/retriever.py`（新增）
- `backend/app/rag/bm25_index.py`（新增）
- `backend/tests/test_retriever.py`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/main.py`（M3 不改 API）
- `backend/app/rag/loader.py`（M2 已完成，不动）
- `backend/app/rag/chunker.py`（M2 已完成，不动）

**验收命令**：
```bash
# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_retriever.py

# 手动验证检索
python -c "
from app.rag.loader import load_knowledge_base
from app.rag.chunker import chunk_documents
from app.rag.retriever import BM25Retriever
docs = load_knowledge_base('backend/data/knowledge_base')
chunks = chunk_documents(docs)
retriever = BM25Retriever(chunks)
results = retriever.retrieve('包裹还没到怎么办', top_k=5)
for r in results:
    print(f'score={r.score:.3f} doc_id={r.metadata[\"doc_id\"]} chunk={r.chunk_index}')
"
```

**我应该 Review 哪些代码**：
1. `bm25_index.py`：BM25 实现是否正确？k1, b 参数？
2. `retriever.py`：返回值是否包含 score, doc_id, chunk_index, metadata？
3. metadata 有没有在检索过程中丢失？
4. 有没有把 expected_doc_ids 泄露给 retriever？（**评测作弊检查**）

**对应 RAG 基础知识点**：
- BM25 算法（TF-IDF 变体，term frequency saturation）
- Retrieval Pipeline（query → index → rank → return）
- Baseline 建立（先有 baseline 才能衡量优化效果）

**如果写错，面试时会被怎么追问**：
- "BM25 的公式是什么？k1 和 b 参数怎么调？"
- "为什么选 BM25 而不是向量检索？"
- "你的 baseline Recall@5 是多少？怎么衡量的？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add baseline BM25 retriever`
- ✅ tag: `m3-baseline-retriever`

---

### M4：retrieval evaluation harness

**本轮目标**：
1. 实现 Retrieval Eval 框架
2. 计算 Recall@1, Recall@3, Recall@5, MRR
3. 每个 case 输出 expected_doc_ids vs retrieved_doc_ids 命中详情
4. 输出总体 Recall@5 作为核心指标

**修改文件**：
- `backend/app/eval/retrieval_eval.py`（新增）
- `backend/app/eval/metrics.py`（新增）
- `backend/tests/test_retrieval_eval.py`（新增）
- `backend/data/eval/eval_results_baseline.json`（新增，baseline 结果）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/main.py`（M4 不改 API）
- `backend/app/rag/retriever.py`（M3 已完成，不动）
- `backend/data/eval/seed_eval_cases.json`（M1 已完成，不动）

**验收命令**：
```bash
# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_retrieval_eval.py

# 运行 baseline eval
python -c "
from app.eval.retrieval_eval import run_retrieval_eval
results = run_retrieval_eval()
print(f'Recall@1: {results.recall_at_1:.2%}')
print(f'Recall@3: {results.recall_at_3:.2%}')
print(f'Recall@5: {results.recall_at_5:.2%}')
print(f'MRR: {results.mrr:.2%}')
print(f'Cases: {len(results.details)}')
"

# ruff 通过
conda run -n customerops-agent python -m ruff check backend
```

**我应该 Review 哪些代码**：
1. `metrics.py`：Recall@K 计算逻辑是否正确？expected_doc_ids 和 retrieved_doc_ids 的交集？
2. `retrieval_eval.py`：有没有让 retriever 看到 expected_doc_ids？（**评测作弊检查**）
3. 每个 case 的 detail 输出是否包含 expected, retrieved, hit, miss？
4. baseline 结果是否被保存，用于后续 optimized 对比？

**对应 RAG 基础知识点**：
- Retrieval Metrics（Recall@K, MRR 的定义和计算）
- Evaluation Harness 设计（自动化批量评估、结果持久化）
- 评测隔离（retriever 不能看到 expected 答案）

**如果写错，面试时会被怎么追问**：
- "Recall@5 具体怎么算？如果一个 case 有 3 个 expected doc，retriever 返回 5 个，其中 2 个命中，Recall@5 是多少？"
- "你怎么保证评测的公平性？retriever 有没有作弊的可能？"
- "MRR 和 Recall@K 有什么区别？什么时候用哪个？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add retrieval evaluation harness with Recall@K metrics`
- ✅ tag: `m4-retrieval-eval`

---

### M5：optimized retriever

**本轮目标**：
1. 在 BM25 基础上实现优化策略
2. metadata filter + synonym expansion + query rewrite
3. embedding adapter 接口预留（mock/stub）
4. Recall@5 目标 ≥ 85%

**修改文件**：
- `backend/app/rag/optimized_retriever.py`（新增）
- `backend/app/rag/synonym_expander.py`（新增）
- `backend/app/rag/query_rewriter.py`（新增）
- `backend/app/rag/metadata_filter.py`（新增）
- `backend/app/rag/embedding_adapter.py`（新增，stub）
- `backend/tests/test_optimized_retriever.py`（新增）
- `backend/data/eval/eval_results_optimized.json`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/main.py`（M5 不改 API）
- `backend/app/rag/retriever.py`（baseline 不动）
- `backend/data/eval/seed_eval_cases.json`（不动）

**验收命令**：
```bash
# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_optimized_retriever.py

# 运行 optimized eval，对比 baseline
python -c "
from app.eval.retrieval_eval import run_retrieval_eval, compare_results
baseline = run_retrieval_eval('baseline')
optimized = run_retrieval_eval('optimized')
compare_results(baseline, optimized)
"

# ruff 通过
conda run -n customerops-agent python -m ruff check backend
```

**我应该 Review 哪些代码**：
1. `optimized_retriever.py`：优化策略的组合方式？score 如何融合？
2. `synonym_expander.py`：同义词表从哪来？扩展逻辑？
3. `query_rewriter.py`：改写规则是什么？会不会改错？
4. `metadata_filter.py`：filter 是在检索前还是检索后？
5. `embedding_adapter.py`：接口是否清晰？stub 是否返回空结果而不是报错？
6. **有没有把优化策略硬编码到 eval cases 里？**（作弊检查）

**对应 RAG 基础知识点**：
- Query Expansion（同义词扩展提升召回）
- Query Rewriting（规则化改写提升匹配）
- Metadata Filtering（结构化过滤提升精准度）
- Embedding Adapter Pattern（可替换接口设计）
- Score Fusion（多信号融合排序）

**如果写错，面试时会被怎么追问**：
- "你的 synonym expansion 是怎么做的？同义词表从哪来？"
- "query rewrite 会不会引入噪声？怎么衡量？"
- "embedding adapter 为什么用 stub？接口设计是什么样的？"
- "你的 Recall@5 从 baseline 的 X% 提升到 85%，具体是哪些优化策略贡献的？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add optimized retriever with metadata/synonym/query-rewrite`
- ✅ tag: `m5-optimized-retriever`

---

### M6：扩展 120+ bad cases + optimization log

**本轮目标**：
1. 将 seed 20 条扩展到 120+ bad cases
2. 增加 bad_case_type, optimization_notes 字段
3. 编写 bad_case_optimization_log.md

**修改文件**：
- `backend/data/eval/bad_cases.json`（新增）
- `backend/data/eval/bad_case_optimization_log.md`（新增）
- `backend/tests/test_bad_cases.py`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/` 业务代码不动
- `backend/data/eval/seed_eval_cases.json`（保留，不合并）

**验收命令**：
```bash
# bad cases 数量
python -c "import json; cases=json.load(open('backend/data/eval/bad_cases.json')); print(f'{len(cases)} bad cases')"

# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_bad_cases.py

# 优化日志存在
ls backend/data/eval/bad_case_optimization_log.md
```

**我应该 Review 哪些代码**：
1. bad_cases.json：是否有 category, difficulty, bad_case_type, optimization_notes 字段？
2. 覆盖度：物流/清关/退货/退款/换货/支付/地址修改/取消订单/多语言是否都有？
3. 优化日志：每类问题的优化策略是否清晰？
4. **有没有把 bad case 的 expected 答案泄露给 retriever/answer generator？**

**对应 RAG 基础知识点**：
- Bad Case Analysis（系统化分析检索/生成失败模式）
- Error Taxonomy（分类法：检索失败、生成失败、格式失败）
- Iterative Optimization（基于 bad case 的迭代优化流程）

**如果写错，面试时会被怎么追问**：
- "你的 120+ bad cases 是怎么分类的？"
- "每个 bad case 的优化策略是什么？效果怎么衡量？"
- "bad case 和 seed eval cases 有什么区别？为什么不合并？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add 120+ bad cases with optimization log`
- ✅ tag: `m6-bad-cases`

---

### M7：prompt builder + mock answer generator + citations

**本轮目标**：
1. 实现 prompt builder（组装 retrieved chunks + query → prompt）
2. 实现 mock answer generator（rule-based，不调真实 LLM）
3. 回答必须包含 citations（引用来源 doc_id）

**修改文件**：
- `backend/app/rag/prompt_builder.py`（新增）
- `backend/app/rag/answer_generator.py`（新增）
- `backend/tests/test_prompt_builder.py`（新增）
- `backend/tests/test_answer_generator.py`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/main.py`（M7 不改 API）
- `backend/app/rag/retriever.py`（不动）
- `backend/app/rag/optimized_retriever.py`（不动）

**验收命令**：
```bash
# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_prompt_builder.py backend/tests/test_answer_generator.py

# 手动验证
python -c "
from app.rag.retriever import BM25Retriever
from app.rag.prompt_builder import build_prompt
from app.rag.answer_generator import generate_answer
# ... load chunks, retrieve, build prompt, generate answer
# verify answer contains citations
"

# ruff 通过
conda run -n customerops-agent python -m ruff check backend
```

**我应该 Review 哪些代码**：
1. `prompt_builder.py`：prompt 模板结构？chunks 怎么注入？有没有注入 expected_keywords？（**作弊检查**）
2. `answer_generator.py`：mock 逻辑是什么？有没有看到 eval case 的 expected 答案？（**作弊检查**）
3. citations：是否正确引用 doc_id？格式是否一致？
4. **mock LLM 有没有被喂了 expected_keywords 或 expected_doc_ids？**

**对应 RAG 基础知识点**：
- Prompt Engineering（RAG prompt 模板设计）
- Citation Generation（引用来源追踪）
- Mock-first Development（先 mock 验证流程，再接真实 LLM）

**如果写错，面试时会被怎么追问**：
- "你的 prompt 模板是怎么设计的？chunks 怎么组织？"
- "citations 是怎么生成的？怎么保证引用正确？"
- "mock answer generator 的逻辑是什么？换成真实 LLM 需要改哪些地方？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add prompt builder, mock answer generator with citations`
- ✅ tag: `m7-answer-generation`

---

### M8：answer evaluation harness

**本轮目标**：
1. 实现 Answer Eval 框架
2. 三大评估维度：Relevance, Groundedness, Completeness
3. 辅助指标：Citation Hit Rate, Keyword Coverage, Answer Pass Rate
4. 输出总体 Answer Pass Rate 作为核心汇总指标

**修改文件**：
- `backend/app/eval/answer_eval.py`（新增）
- `backend/tests/test_answer_eval.py`（新增）
- `backend/data/eval/answer_eval_results.json`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/main.py`（M8 不改 API）
- `backend/app/rag/answer_generator.py`（不动）

**验收命令**：
```bash
# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_answer_eval.py

# 运行 answer eval
python -c "
from app.eval.answer_eval import run_answer_eval
results = run_answer_eval()
print(f'Relevance: {results.relevance:.2%}')
print(f'Groundedness: {results.groundedness:.2%}')
print(f'Completeness: {results.completeness:.2%}')
print(f'Citation Hit Rate: {results.citation_hit_rate:.2%}')
print(f'Keyword Coverage: {results.keyword_coverage:.2%}')
print(f'Answer Pass Rate: {results.answer_pass_rate:.2%}')
"

# ruff 通过
conda run -n customerops-agent python -m ruff check backend
```

**我应该 Review 哪些代码**：
1. `answer_eval.py`：三大维度 + 辅助指标的计算逻辑是否正确？
2. Groundedness：怎么判断回答是否基于 retrieved chunks？
3. **有没有让 answer generator 看到 expected_keywords？**（作弊检查）
4. **有没有让 eval 看到 answer generator 的内部状态？**（评测隔离检查）

**对应 RAG 基础知识点**：
- RAG Evaluation Metrics（Relevance, Groundedness, Completeness — 三大维度）
- Citation Quality Metrics（Citation Hit Rate — 辅助指标）
- Answer Quality Assessment（Pass Rate, Keyword Coverage — 辅助指标）

**如果写错，面试时会被怎么追问**：
- "Groundedness 是怎么计算的？和 Relevance 有什么区别？"
- "你的 Answer Pass Rate 是怎么定义的？通过的标准是什么？"
- "三个维度之间有没有相关性？权重怎么分配？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add answer evaluation harness with 6 quality metrics`
- ✅ tag: `m8-answer-eval`

---

### M9：FastAPI API 集成

**本轮目标**：
1. 集成 /api/retrieve 端点
2. 集成 /api/answer 端点
3. 集成 /api/eval 端点
4. 保持 /api/health 不变

**修改文件**：
- `backend/app/api/routes_rag.py`（新增）
- `backend/app/main.py`（追加 router）
- `backend/tests/test_api_rag.py`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/api/routes_health.py`（不动）
- `backend/app/rag/`（不动）
- `backend/app/eval/`（不动）

**验收命令**：
```bash
# 测试通过
conda run -n customerops-agent python -m pytest backend/tests/test_api_rag.py

# 手动测试 API
# 启动服务
conda run -n customerops-agent uvicorn app.main:app --app-dir backend --reload

# 另一个终端
curl http://localhost:8000/api/health
curl -X POST http://localhost:8000/api/retrieve -H "Content-Type: application/json" -d '{"query": "包裹还没到"}'
curl -X POST http://localhost:8000/api/answer -H "Content-Type: application/json" -d '{"query": "包裹还没到"}'
curl -X POST http://localhost:8000/api/eval
```

**我应该 Review 哪些代码**：
1. `routes_rag.py`：request/response schema 是否清晰？
2. `/api/eval`：有没有返回 Recall@5 和 Answer Pass Rate？
3. 错误处理：query 为空、知识库为空、检索失败怎么处理？
4. **API 有没有泄露 eval case 的 expected 答案？**

**对应 RAG 基础知识点**：
- API Design（RESTful RAG API 设计）
- Request/Response Schema（Pydantic 模型约束）
- Integration Testing（端到端 API 测试）

**如果写错，面试时会被怎么追问**：
- "你的 API 设计是什么？为什么分 retrieve 和 answer？"
- "错误处理是怎么做的？如果知识库为空返回什么？"
- "API 的 request/response schema 是怎么定义的？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add RAG API endpoints (retrieve, answer, eval)`
- ✅ tag: `m9-api-integration`

---

### M10：README / ARCHITECTURE / EVAL_REPORT / INTERVIEW_QA

**本轮目标**：
1. 更新 README.md（对齐简历定位）
2. 新增 ARCHITECTURE.md（系统架构图）
3. 新增 EVAL_REPORT.md（评测报告）
4. 新增 INTERVIEW_QA.md（面试问答准备）

**修改文件**：
- `README.md`（重写）
- `docs/ARCHITECTURE.md`（新增）
- `docs/EVAL_REPORT.md`（新增）
- `docs/INTERVIEW_QA.md`（新增）

**不修改文件**：
- `frontend/` 全部不动
- `backend/app/` 全部不动
- `docs/00-03_*.md`（不动）

**验收命令**：
```bash
# 文档存在
ls README.md docs/ARCHITECTURE.md docs/EVAL_REPORT.md docs/INTERVIEW_QA.md

# README 包含简历关键词
grep -q "RAG" README.md && grep -q "Evaluation" README.md && grep -q "Bad Case" README.md

# EVAL_REPORT 包含 Recall@5
grep -q "Recall@5" docs/EVAL_REPORT.md
```

**我应该 Review 哪些代码**：
1. README.md：是否对齐简历四个核心描述？
2. ARCHITECTURE.md：架构图是否清晰？是否说明了 baseline → optimized 的演进？
3. EVAL_REPORT.md：是否有 baseline vs optimized 的 Recall@5 对比？
4. INTERVIEW_QA.md：是否覆盖了常见追问？

**对应 RAG 基础知识点**：
- Technical Documentation（项目文档最佳实践）
- Architecture Diagram（系统架构可视化）
- Evaluation Reporting（评测结果呈现）

**如果写错，面试时会被怎么追问**：
- "你的项目架构是什么样的？画一下？"
- "你的评测结果是什么？Recall@5 从多少提升到多少？"
- "你遇到的最大的 bad case 是什么？怎么解决的？"

**是否需要 git commit / tag**：
- ✅ commit: `docs: add README, architecture, eval report, interview QA`
- ✅ tag: `m10-docs`

---

### M11：可选极简前端

**触发条件**：M1-M10 全部完成且有剩余时间

**本轮目标**：
1. 极简 Chat Demo 页面
2. Eval Report 页面
3. Bad Case Compare 页面

**修改文件**：
- `frontend/app/chat/page.tsx`（新增）
- `frontend/app/eval/page.tsx`（新增）
- `frontend/app/bad-cases/page.tsx`（新增）
- `frontend/lib/api.ts`（更新，对接新 API）

**不修改文件**：
- `frontend/app/page.tsx`（legacy，不动）
- `backend/app/`（不动）

**验收命令**：
```bash
cd frontend && npm run build
```

**我应该 Review 哪些代码**：
1. 每个页面是否 < 300 行？
2. 是否只用了 Tailwind + 系统字体？
3. 是否正确调用了 /api/retrieve, /api/answer, /api/eval？
4. **有没有在前端硬编码 eval case 的 expected 答案？**

**对应 RAG 基础知识点**：
- Minimal Viable UI（最小可行演示界面）
- RAG Demo Design（Chat + Citations + Chunks 展示）

**如果写错，面试时会被怎么追问**：
- "你的前端展示了哪些 RAG 信息？"
- "citations 是怎么展示的？"
- "为什么前端这么简单？不担心项目不完整吗？"

**是否需要 git commit / tag**：
- ✅ commit: `feat: add minimal RAG demo frontend (chat, eval, bad cases)`
- ✅ tag: `m11-frontend-demo`

---

## 六、Evaluation Harness 防作弊约束

```
核心原则：评测结果必须可信、可复现、不可伪造。

约束清单：
  1. retriever 不能读取 expected_doc_ids
     - retrieval_eval.py 调用 retriever 时，只传 query，不传 expected
     - retriever 的输入只有 query string + 可选 metadata filter

  2. answer_generator 不能读取 expected_keywords
     - answer_generator 的输入只有 query + retrieved chunks
     - 不能从 eval case 中注入 expected_keywords 到 prompt

  3. optimized retriever 不能为 eval cases 写死规则
     - 优化策略必须是通用的（metadata filter, synonym expansion, query rewrite）
     - 不能针对特定 eval case 做硬编码 if-else
     - 检查方式：random shuffle eval cases 后指标不应剧变

  4. baseline 和 optimized 必须跑同一份 eval set
     - 两者的 eval set 版本、条目、顺序必须一致
     - 不能 optimized 用更简单的 eval set

  5. eval report 必须输出失败 case
     - 不能只输出 Recall@5 = 85% 就完事
     - 必须输出 failed_cases 列表：query + expected + retrieved + miss
     - 这是面试时讲 bad case 分析的基础

  6. eval set 要固定版本
     - seed_eval_cases.json 和 bad_cases.json 一旦生成，不可随意修改
     - 如需修改，必须在 optimization_log 中记录原因和变更内容
     - 版本号体现在文件名或 metadata 中

  7. 所有指标必须可复现
     - 相同 eval set + 相同 retriever config → 相同指标
     - 不依赖随机数（如果用随机，必须 fixed seed）
     - eval 结果保存为 JSON，包含 timestamp + config hash

评测框架有防作弊设计：retriever 看不到 expected 答案，optimized 不为 eval cases 硬编码，所有指标可复现。eval report 不只输出数字，还输出失败 case，方便迭代优化。
```

## 七、M0 后文档限制

```
M0 可以创建以下文档（仅限这 6 个）：
  - docs/00_SCOPE_LOCK.md
  - docs/01_ACCEPTANCE_CRITERIA.md
  - docs/02_RAG_DESIGN.md
  - docs/03_EVAL_DESIGN.md
  - docs/DEV_STATUS.md
  - docs/CHANGELOG.md

M0 结束后：
  - 立刻进入 M1 数据层和代码实现
  - 不继续扩写大量规划文档
  - M10 统一更新 README / ARCHITECTURE / EVAL_REPORT / INTERVIEW_QA
  - 中间阶段只写代码 + 测试，不写额外设计文档
```

## 八、Code Review 教学清单

每轮结束后，我会告诉你：

1. **这个函数的输入是什么？** — 参数类型、来源
2. **输出是什么？** — 返回类型、包含哪些字段
3. **metadata 有没有丢？** — doc_id / category / market / language / score / citation 是否一路传下去
4. **有没有评测作弊？** — expected_doc_ids / expected_keywords 有没有泄露给 retriever / answer_generator
5. **失败情况怎么处理？** — 空输入、空知识库、检索失败、生成失败
6. **手动测试 case** — 每轮 2-3 个你可以手动跑的测试命令
