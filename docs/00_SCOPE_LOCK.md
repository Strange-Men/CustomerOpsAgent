# CustomerOps Agent｜项目边界锁定

**日期**：2026-06-24
**状态**：LOCKED — M0 后不再修改本文档

---

## 一、项目定位

**跨境电商轻量客服 RAG Agent + RAG Evaluation Harness**

本项目是一个面向跨境电商客服场景的轻量客服 RAG Agent 系统，核心能力是：

1. 分层知识库检索（BM25 baseline → 优化策略）
2. 轻量 Agent Workflow（Intent Recognition → Evidence Check → Answer Generation → Citation Check → Fallback）
3. 回答生成（mock-first，带 citations）
4. 双层 Evaluation Harness（Retrieval Eval + Answer Eval）
5. 120+ Bad Case 分析与迭代优化

**Agent 层说明**：Agent 层由 intent recognition、evidence check、answer generation、citation check、fallback rules 组成，是围绕 RAG 的轻量工作流。明确不做复杂 6 Agent 工单系统、不做 LangGraph 多 Agent 编排、不做多租户 SaaS。

**简历对应能力**：
- "构建 RAG 知识库，按 category/market/language/policy_type 做分层，通过 metadata filter 提升召回准确率"
- "建立 Evaluation Harness，从三个维度自动批量化评估回答质量"
- "top-5 知识召回准确率从 baseline 提升至 85%"
- "高频咨询场景回答合格率从 55% 提升到 85%，提升 30 个百分点"
- "积累 120+ bad cases，形成分类优化日志"
- "支持多语种知识库快速迁移"

---

## 二、两天 MVP 目标

**Day 1：检索闭环 + Retrieval Eval（M0-M4）**
- M0：边界重锁 + 冻结前端 + 文档补档
- M1：知识库 schema + 20 条 seed eval cases
- M2：loader + chunker
- M3：baseline BM25 retriever
- M4：retrieval evaluation harness

**Day 2：优化 + Answer Eval + API（M5-M10）**
- M5：optimized retriever（Recall@5 ≥ 85%）
- M6：扩展 120+ bad cases + optimization log
- M7：prompt builder + mock answer generator + citations
- M8：answer evaluation harness
- M9：FastAPI API 集成
- M10：README / ARCHITECTURE / EVAL_REPORT

---

## 三、做什么（MVP 范围）

| # | 能力 | 说明 |
|---|------|------|
| 1 | 分层知识库 | Markdown + YAML frontmatter，按 category/market/language/policy_type 分层 |
| 2 | 多语种迁移支持 | 数据结构 + 检索接口支持多语种，不需要翻译服务 |
| 3 | BM25 baseline retriever | 纯关键词匹配，可解释基线 |
| 4 | Optimized retriever | BM25 + metadata filter + synonym expansion + query rewrite + embedding adapter stub |
| 5 | Retrieval Evaluation | Recall@1/3/5, MRR |
| 6 | Answer Evaluation | 三大维度：Relevance, Groundedness, Completeness + 辅助指标 |
| 7 | Bad Case 优化 | 120+ cases + optimization log |
| 8 | FastAPI API | /api/retrieve, /api/answer, /api/eval |
| 9 | 20 seed eval cases → 120+ bad cases | 覆盖物流/清关/退货/退款/换货/支付/地址修改/取消订单/多语言 |

---

## 四、不做什么

| # | 禁止项 | 原因 |
|---|--------|------|
| 1 | 登录/注册 | MVP 不需要用户系统 |
| 2 | 权限系统 | 单用户 demo |
| 3 | 真实订单系统 | mock data 足够 |
| 4 | 真实物流 API | mock data 足够 |
| 5 | 客服坐席后台 | 不是工单系统 |
| 6 | 工单流转 | 不是工单系统 |
| 7 | 复杂多租户 | 单用户 demo |
| 8 | 复杂 Dashboard | 极简前端即可 |
| 9 | LangGraph 多 Agent 编排 | 单 Agent RAG 足够 |
| 10 | 生产级数据库 | JSON file 足够 |
| 11 | 过度 UI 动效 | 后端优先，前端极简 |
| 12 | 6 Agent 工单编排 | 方向已修正 |
| 13 | 真实 LLM 调用 | mock-first |
| 14 | 向量数据库 | BM25 足够 |
| 15 | Docker 部署 | 本地 demo |
| 16 | 复杂翻译服务 | 只做数据结构支持 |

---

## 五、前端策略

### 冻结声明

`frontend/app/page.tsx` 及其依赖文件**冻结为 legacy/static demo**。

- 不删除
- 不修改
- 不扩展
- 不修 bug
- 保留可 build 状态

### 后端优先

M0-M10 全部聚焦后端 RAG + Eval 核心闭环。

### 可选极简前端（M11，仅后端闭环后）

| 页面 | 内容 | 禁止内容 |
|------|------|---------|
| Chat Demo | 输入问题 → answer + citations + retrieved chunks | 无登录、无权限 |
| Eval Report | Recall@5 / Answer Pass Rate / Groundedness | 无复杂 Dashboard |
| Bad Case Compare | baseline vs optimized 差异对比 | 无工单后台 |

### 前端工作流要求

后续如做前端，必须严格走"前端工作流"（参考 `D:\Claude_skill\MySkill\前端工作流.md`）：
1. 先写前端设计文档（1 页）
2. 审查通过后才写代码
3. 使用 `.claude/skills/frontend-design/SKILL.md`
4. 单页面不超过 300 行
5. 只用 Tailwind + 系统字体
6. 不引入新 UI 库

---

## 六、知识库 Metadata Schema

知识库文档使用 Markdown + YAML frontmatter 格式：

```yaml
---
doc_id: "POL-LOGISTICS-001"        # 唯一标识
title: "跨境物流配送政策"            # 文档标题
category: "logistics"               # 分类：logistics/customs/return/refund/exchange/payment
market: "US"                        # 目标市场：US/EU/SEA
language: "zh"                      # 语言代码：zh/en
policy_type: "shipping"             # 政策类型：shipping/return/customs/payment
priority: 1                         # 优先级：1=高, 2=中, 3=低
source: "official_2026Q1"           # 来源
---

（Markdown 正文内容）
```

---

## 七、多语种知识库快速迁移

**落地要求**：
1. knowledge_base 文档必须包含 language 字段
2. eval_cases 必须包含 language 字段
3. 至少包含 zh / en 两种语言样例
4. retriever 支持 language filter（metadata filter 的一部分）
5. README 需要说明如何迁移到新的语种知识库
6. 不需要做复杂翻译服务，只需数据结构和检索接口支持多语种迁移

**迁移流程**：
1. 在 `backend/data/knowledge_base/{language}/` 下新增对应语种 .md 文件
2. frontmatter 中设置 language 字段
3. 新增对应的 eval cases（含 language 字段）
4. retriever 的 metadata filter 自动支持新语种，无需改代码

---

## 八、M0 后文档限制

M0 结束后：
- 立刻进入 M1 数据层和代码实现
- 不继续扩写大量规划文档
- M10 统一更新 README / ARCHITECTURE / EVAL_REPORT / INTERVIEW_QA
- 中间阶段只写代码 + 测试，不写额外设计文档

---

## 九、版本记录

- **v1.0**（2026-06-24）：M0 边界重锁，从"6 Agent 工单系统"修正为"RAG + Eval"方向
