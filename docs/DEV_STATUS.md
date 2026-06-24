# CustomerOps Agent｜开发状态

## 1. 当前阶段

**M1: 知识库 Schema + Seed Eval Cases**

## 2. 当前项目状态

**状态：M1 数据层建设完成**

- ✅ 项目方向重锁为 RAG + Eval（M0）
- ✅ 前端冻结为 legacy/static demo（M0）
- ✅ 边界锁定文档（00_SCOPE_LOCK.md）
- ✅ 验收标准文档（01_ACCEPTANCE_CRITERIA.md）
- ✅ RAG 设计文档（02_RAG_DESIGN.md）
- ✅ Eval 设计文档（03_EVAL_DESIGN.md）
- ✅ ROADMAP_V2 后端优先开发路线（M0-M11）
- ✅ Pydantic schema 定义（schemas.py）
- ✅ Seed knowledge base（14 条知识文档）
- ✅ Seed eval cases（20 条评测用例）
- ✅ 数据 schema 测试（test_data_schema.py）
- ❌ 尚未实现 loader / chunker
- ❌ 尚未实现 retriever
- ❌ 尚未实现 evaluation harness
- ❌ 尚未实现 answer generator
- ❌ 尚未实现 RAG API

## 3. 已完成内容

### M1：知识库 Schema + Seed Eval Cases（本轮）

- ✅ 创建 `backend/app/rag/schemas.py`
  - KnowledgeDocument 模型（9 字段：doc_id/title/category/market/language/policy_type/priority/source/content）
  - EvalCase 模型（8 字段：case_id/question/category/market/language/difficulty/expected_doc_ids/expected_keywords）
  - 字段与 M0 文档 metadata schema 对齐

- ✅ 创建 `backend/data/knowledge_base/customer_service_seed.jsonl`
  - 14 条知识文档
  - 覆盖场景：物流时效、清关延迟、退货政策、退款规则、换货流程、地址修改、订单取消、支付失败、包裹丢失、包裹破损、优惠券问题、多语言英文咨询
  - 语言覆盖：zh（12 条）/ en（2 条）
  - 市场覆盖：US / EU / GLOBAL

- ✅ 创建 `backend/data/eval_cases_seed.jsonl`
  - 20 条评测用例
  - difficulty 分布：easy(8) / medium(8) / hard(4)
  - language 分布：zh(16) / en(4)
  - 所有 expected_doc_ids 均对应知识库 doc_id

- ✅ 创建 `backend/tests/test_data_schema.py`
  - JSONL 读取与 Pydantic 校验
  - doc_id / case_id 唯一性检查
  - expected_doc_ids 与知识库交叉校验
  - language 覆盖检查（zh/en）
  - 数量检查（12+ docs, 20 cases）
  - 英文 case 问题语言检查

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
| `backend/app/rag/schemas.py` | 数据模型 | ✅ M1 新增 |
| `backend/data/knowledge_base/customer_service_seed.jsonl` | 种子知识库 | ✅ M1 新增 |
| `backend/data/eval_cases_seed.jsonl` | 种子评测集 | ✅ M1 新增 |
| `backend/tests/test_data_schema.py` | 数据校验测试 | ✅ M1 新增 |

## 5. 下一步

**进入 M2：loader + chunker**

M2 目标：
- 实现 JSONL loader，读取知识库文件
- 实现 chunker，将文档按段落切分为 chunks
- 每个 chunk 继承文档级 metadata
- 单元测试覆盖

## 6. 风险点

| 风险 | 说明 | 控制方式 |
|------|------|---------|
| 数据质量不够 | 14 条 seed 知识库可能不够覆盖 | M6 扩展到 120+ |
| expected_doc_ids 不匹配 | eval case 引用的 doc_id 可能不存在 | 测试已覆盖交叉校验 |
| 字段设计后续不够用 | schema 字段可能需要扩展 | M2 chunking 时验证 |
| 英文 case 只是伪英文 | 英文问题质量可能不高 | 测试已检查非中文 |
| 测试只测文件存在 | 测试已真正校验 JSONL 内容和 schema | ✅ 已解决 |

## 7. 当前禁止事项

- ❌ 不继续扩写大文档
- ❌ 不碰前端
- ❌ 不写 retriever
- ❌ 不写 evaluation harness
- ❌ 不写 answer generator
- ❌ 不接 LLM API
- ❌ 不实现 6 Agent 工单编排
- ❌ 不实现登录/权限/多租户
