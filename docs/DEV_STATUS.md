# CustomerOps Agent｜开发状态

## 1. 当前阶段

**M0: Scope Locked, Frontend Frozen, Docs Ready**

项目方向已从"6 Agent 工单系统"正式重锁为"跨境电商客服 RAG Agent + RAG Evaluation Harness"。

## 2. 当前项目状态

**状态：M0 边界重锁完成，准备进入 M1 数据层**

- ✅ 项目方向重锁为 RAG + Eval
- ✅ 前端冻结为 legacy/static demo
- ✅ 边界锁定文档（00_SCOPE_LOCK.md）
- ✅ 验收标准文档（01_ACCEPTANCE_CRITERIA.md）
- ✅ RAG 设计文档（02_RAG_DESIGN.md）
- ✅ Eval 设计文档（03_EVAL_DESIGN.md）
- ✅ ROADMAP_V2 后端优先开发路线（M0-M11）
- ✅ M0 执行 Prompt
- ❌ 尚未实现知识库 schema
- ❌ 尚未实现 eval cases
- ❌ 尚未实现 loader / chunker
- ❌ 尚未实现 retriever
- ❌ 尚未实现 evaluation harness
- ❌ 尚未实现 answer generator
- ❌ 尚未实现 RAG API

## 3. 已完成内容

### M0：边界重锁 + 冻结前端 + 最小文档补档（本轮）

- ✅ 创建 `docs/00_SCOPE_LOCK.md` — 项目边界锁定
  - 项目定位：跨境电商客服 RAG Agent + RAG Evaluation Harness
  - 做什么 / 不做什么
  - 前端冻结声明
  - 知识库 Metadata Schema（8 字段）
  - 多语种迁移说明
  - 面试讲法

- ✅ 创建 `docs/01_ACCEPTANCE_CRITERIA.md` — 两天 MVP 验收标准
  - 简历指标口径说明（30 个百分点）
  - 11 项必须完成标准
  - 3 项可选加分
  - 8 项不做清单

- ✅ 创建 `docs/02_RAG_DESIGN.md` — RAG 设计文档
  - RAG 流程：knowledge base → chunking → retrieval → prompt → answer → citations
  - 分层知识库 schema
  - chunking 策略
  - retriever 设计（baseline + optimized）
  - citations 设计
  - 多语种迁移

- ✅ 创建 `docs/03_EVAL_DESIGN.md` — Evaluation Harness 设计
  - 第一层：Retrieval Evaluation（Recall@1/3/5, MRR）
  - 第二层：Answer Evaluation（三大维度 + 辅助指标）
  - 8 条防作弊约束
  - 数据集设计

- ✅ 创建 `docs/ROADMAP_V2.md` — 修正版开发路线
  - M0-M11 后端优先开发顺序
  - 检索方案设计
  - 数据集策略
  - Evaluation 顺序

- ✅ 创建 `docs/M0_EXECUTION_PROMPT.md` — M0 执行 Prompt

- ✅ 更新 `docs/DEV_STATUS.md` — 当前状态
- ✅ 更新 `docs/CHANGELOG.md` — 变更记录

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
| `docs/DEV_STATUS.md` | 开发状态（本文件） | ✅ M0 更新 |
| `docs/CHANGELOG.md` | 变更记录 | ✅ M0 更新 |
| `docs/PROJECT_CONTEXT.md` | 项目背景 | v1 参考 |
| `docs/PRD.md` | 产品需求 | v1 参考 |
| `docs/DESIGN.md` | 设计文档 | v1 参考 |
| `docs/TECHNICAL_SPEC.md` | 技术规格 | v1 参考 |
| `docs/DEV_RULES.md` | 开发规则 | v1 参考 |

## 5. 下一步

**进入 M1：知识库 schema + 20 条 seed eval cases**

M1 目标：
- 设计知识库文档 schema（Markdown + metadata frontmatter）
- 创建 6 篇知识库文档（覆盖物流/清关/退货/退款/换货/支付）
- 创建 20 条 seed eval cases
- 覆盖 zh / en 两种语言
- Pydantic schema 定义

## 6. 风险点

| 风险 | 说明 | 控制方式 |
|------|------|---------|
| 文档过重 | M0 文档较多，需快速进入代码 | M0 后不再扩写文档 |
| 前端偏航 | legacy 前端可能误导方向 | 冻结声明，后端优先 |
| 假指标 | Recall@5 可能被硬编码 | 防作弊约束 |
| eval 数据质量 | 20 条 seed 可能不够 | M6 扩展到 120+ |
| 时间紧 | 两天 MVP 时间有限 | 小步迭代，M0-M4 Day1，M5-M10 Day2 |

## 7. 当前禁止事项

- ❌ 不继续扩写大文档
- ❌ 不碰前端
- ❌ 不写大模块
- ❌ 不修改 frontend/app/page.tsx
- ❌ 不实现 6 Agent 工单编排
- ❌ 不实现登录/权限/多租户
- ❌ 不实现真实 LLM 调用
