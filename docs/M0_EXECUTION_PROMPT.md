# M0 执行 Prompt

**阶段**：M0 — 边界重锁 + 冻结前端 + 最小文档补档
**预计耗时**：~2 小时
**核心原则**：不写业务代码，只写文档

---

## Prompt（直接复制使用）

```
你现在进入 M0 阶段：边界重锁 + 冻结前端 + 最小文档补档。

## 背景
CustomerOps Agent 项目方向从"6 Agent 工单系统"修正为"RAG 知识库 + Retrieval 优化 + Evaluation Harness"。
现有 frontend/app/page.tsx 是 674 行静态工单工作台，与新方向不匹配，需要冻结。

## 你的任务

### 任务 1：创建 docs/00_SCOPE_LOCK.md

内容要求：
1. 项目定位：跨境电商客服 RAG Agent 系统
2. 做什么（MVP 范围）：
   - 分层知识库（Markdown + metadata，按 category/market/language/policy_type 分层）
   - 多语种知识库快速迁移支持（数据结构 + 检索接口，不需要翻译服务）
   - BM25 baseline retriever
   - Optimized retriever（metadata filter + synonym expansion + query rewrite + embedding adapter stub）
   - Retrieval Evaluation（Recall@1/3/5, MRR）
   - Answer Evaluation（三大维度：Relevance, Groundedness, Completeness + 辅助指标：Citation Hit Rate, Keyword Coverage, Answer Pass Rate）
   - Bad Case 优化（120+ cases + optimization log）
   - FastAPI API（/api/retrieve, /api/answer, /api/eval）
   - 20 条 seed eval cases → 120+ bad cases
3. 不做什么：
   - 不做 6 Agent 工单编排
   - 不做登录/权限/多租户
   - 不做真实 LLM 调用（mock-first）
   - 不做向量数据库
   - 不做 Docker 部署
   - 不做前端工单系统
   - 不做订单/物流真实 API
   - 不做复杂前端 Dashboard
   - 不做复杂翻译服务（只做数据结构支持）
4. 前端策略：
   - frontend/app/page.tsx 冻结为 legacy/static demo
   - 不删除、不修改、不扩展
   - 可选极简前端（M11）只做 Chat Demo + Eval Report + Bad Case Compare
5. 检索方案：
   - Baseline：BM25 / 关键词检索（可解释基线）
   - Optimized：BM25 + metadata filter（含 language filter）+ synonym expansion + query rewrite + optional embedding adapter
   - embedding adapter 先用 stub，保留可替换接口
6. 知识库 Metadata Schema（分层知识库定义）：
   - doc_id: 唯一标识
   - title: 文档标题
   - category: 分类（logistics/customs/return/refund/exchange/payment）
   - market: 目标市场（US/EU/SEA）
   - language: 语言代码（zh/en）
   - policy_type: 政策类型（shipping/return/customs/payment）
   - priority: 优先级（1=高, 2=中, 3=低）
   - source: 来源（official_2026Q1）
   - content: Markdown 正文（不在 frontmatter 中）
7. 数据集策略：
   - M1：20 条 seed eval cases（覆盖物流/清关/退货/退款/换货/支付/地址修改/取消订单/多语言，至少包含 zh/en 两种语言）
   - M6：扩展到 120+ bad cases + bad case optimization log
8. Evaluation 顺序：
   - 先 Retrieval Eval（M4）：Recall@1/3/5, MRR
   - 后 Answer Eval（M8）：三大维度（Relevance, Groundedness, Completeness）+ 辅助指标
   - 对应简历核心指标："top-5 知识召回准确率提升至 85%"
9. 简历指标口径：
   - 简历简写："高频咨询场景回答合格率提升 30%"
   - 严谨表述："高频咨询场景回答合格率从 55% 提升到 85%，提升 30 个百分点"
   - 项目报告统一使用"30 个百分点"
10. 防作弊约束：
    - retriever 不能读取 expected_doc_ids
    - answer_generator 不能读取 expected_keywords
    - optimized retriever 不能为 eval cases 写死规则
    - baseline 和 optimized 必须跑同一份 eval set
    - eval report 必须输出失败 case
    - eval set 固定版本，不可随意修改
    - 所有指标必须可复现

### 任务 2：创建 docs/01_ACCEPTANCE_CRITERIA.md

内容要求：
1. 简历指标口径说明：
   - 简历简写："高频咨询场景回答合格率提升 30%"
   - 严谨表述："高频咨询场景回答合格率从 55% 提升到 85%，提升 30 个百分点"
   - "提升 30%" 是相对提升（55% × 1.3 = 71.5%），口径不同
   - "提升 30 个百分点" 是绝对提升（55% + 30pp = 85%）
   - 项目报告、EVAL_REPORT、面试口述统一使用"30 个百分点"
   - README 可保留"提升 30%"作为简历简写，但需注明口径
2. 两天 MVP 结束标准（11 项必须完成）
3. 可选完成标准（3 项加分）
4. 不做清单（8 项）
5. 每项标准的验收命令

### 任务 3：创建 docs/02_RAG_DESIGN.md

内容要求：
1. 知识库设计：
   - Markdown + YAML frontmatter
   - 完整 metadata schema（分层知识库）：
     * doc_id: 唯一标识（string）
     * title: 文档标题（string）
     * category: 分类（string，如 logistics/customs/return/refund/exchange/payment）
     * market: 目标市场（string，如 US/EU/SEA）
     * language: 语言代码（string，如 zh/en）
     * policy_type: 政策类型（string，如 shipping/return/customs/payment）
     * priority: 优先级（int，1=高/2=中/3=低）
     * source: 来源（string，如 official_2026Q1）
   - 6 篇知识库文档覆盖：物流政策、清关指南、退货政策、退款流程、换货政策、支付问题
   - 至少包含 zh / en 两种语言样例
   - 多语种迁移说明：新增语种只需在 backend/data/knowledge_base/{language}/ 下新增 .md 文件，retriever 的 metadata filter 自动支持
2. Chunking 策略：
   - 按标题 + 段落切分
   - 每个 chunk 携带完整 metadata（doc_id, category, market, language, policy_type 等全部继承）
   - chunk 大小范围：100-500 tokens
3. Retriever 设计：
   - Baseline：BM25（纯关键词匹配）
   - Optimized：BM25 + metadata filter（含 language filter）+ synonym expansion + query rewrite
   - Embedding adapter：接口预留，MVP 用 stub
   - metadata filter 在检索前应用，减少候选集
4. Prompt Builder 设计：
   - 组装 retrieved chunks + query → prompt
   - 包含 citation 指令
5. Answer Generator 设计：
   - mock-first，rule-based
   - 输出 answer + citations

### 任务 4：创建 docs/03_EVAL_DESIGN.md

内容要求：
1. Retrieval Evaluation（先做）：
   - Recall@1：top-1 是否命中 expected_doc_ids
   - Recall@3：top-3 是否命中 expected_doc_ids
   - Recall@5：top-5 是否命中 expected_doc_ids（核心指标）
   - MRR：第一个命中的排名倒数
   - 每个 case 输出：expected_doc_ids, retrieved_doc_ids, hit, miss
2. Answer Evaluation（后做）—— 三大评估维度 + 辅助指标：
   - 三大评估维度（对应简历"从三个维度自动批量化评估回答质量"）：
     * Relevance：回答是否切题（是否与问题相关）
     * Groundedness：回答是否基于知识库，是否减少幻觉（是否基于 retrieved chunks）
     * Completeness：回答是否覆盖关键处理步骤（是否覆盖 expected_keywords）
   - 辅助指标：
     * Citation Hit Rate：citations 中有多少命中 expected_doc_ids
     * Keyword Coverage：expected_keywords 在回答中的覆盖率
     * Answer Pass Rate：通过的 case 占比（核心汇总指标）
   - 注意：不要把 6 个指标都称为 6 个维度，简历写的是"三个维度"
3. 评测隔离原则（防作弊约束）：
   - retriever 不能读取 expected_doc_ids（调用时只传 query）
   - answer_generator 不能读取 expected_keywords（输入只有 query + retrieved chunks）
   - eval 模块独立于 retrieval/answer 模块
   - optimized retriever 不能为 eval cases 写死规则（优化策略必须是通用的）
   - baseline 和 optimized 必须跑同一份 eval set（版本、条目、顺序一致）
   - eval report 必须输出失败 case（不能只输出数字）
   - eval set 固定版本（一旦生成不可随意修改，修改需记录原因）
   - 所有指标必须可复现（相同 eval set + 相同 config → 相同结果）
4. 数据集设计：
   - seed_eval_cases.json：20 条，字段：query, expected_doc_ids, expected_keywords, category, difficulty, market, language
   - bad_cases.json：120+ 条，额外字段：bad_case_type, optimization_notes
   - bad_case_optimization_log.md：每类问题的优化策略
   - eval set 必须包含 zh / en 两种语言样例

### 任务 5：更新 docs/DEV_STATUS.md

在"当前阶段"部分更新：
- 状态改为 "M0: Scope Locked, Frontend Frozen, Docs Ready"
- 下一步改为 "M1: Knowledge Base Schema + 20 Seed Eval Cases"

### 任务 6：追加 docs/CHANGELOG.md

追加 M0 记录：
- 日期：2026-06-24
- 内容：M0 边界重锁、前端冻结、5 个设计文档创建
- 关联文档：00-03 新文档

## 约束

1. 不写任何业务代码（不创建 .py 文件）
2. 不修改 frontend/ 下任何文件
3. 不修改 backend/app/ 下任何文件
4. 不删除任何文件
5. 不改 git 历史
6. 不伪造 commit
7. 每个文档不超过 200 行
8. 语言：中文为主，技术术语用英文
9. M0 只创建以下 6 个文档，不创建其他文档：
   - docs/00_SCOPE_LOCK.md
   - docs/01_ACCEPTANCE_CRITERIA.md
   - docs/02_RAG_DESIGN.md
   - docs/03_EVAL_DESIGN.md
   - docs/DEV_STATUS.md
   - docs/CHANGELOG.md
10. M0 结束后立刻进入 M1 数据层和代码实现，不继续扩写规划文档

## 完成后

1. 运行 `conda run -n customerops-agent python -m pytest backend` 确认测试仍通过
2. 运行 `cd frontend && npm run build` 确认前端仍可 build
3. 运行 `git status` 确认没有意外修改
4. 提交：`git add docs/ && git commit -m "docs: add scope lock and RAG/eval design docs"`
5. 打 tag：`git tag m0-scope-locked`
```

---

## 使用方式

1. 复制上面的 Prompt
2. 在 Claude Code 中粘贴执行
3. 执行完成后 Review 5 个新文档
4. 确认无误后进入 M1

## M0 完成检查清单

- [ ] `docs/00_SCOPE_LOCK.md` 存在且内容完整
  - [ ] 包含知识库 Metadata Schema（8 个字段：doc_id/title/category/market/language/policy_type/priority/source）
  - [ ] 包含多语种知识库快速迁移说明
  - [ ] 包含防作弊约束清单
  - [ ] 包含简历指标口径说明（30 个百分点）
- [ ] `docs/01_ACCEPTANCE_CRITERIA.md` 存在且包含 11 项必须标准
  - [ ] 包含简历指标口径说明
- [ ] `docs/02_RAG_DESIGN.md` 存在且覆盖知识库/chunking/retriever/prompt/answer
  - [ ] 知识库 metadata 包含完整 8 个字段
  - [ ] 包含 language filter 说明
  - [ ] 包含多语种迁移流程
- [ ] `docs/03_EVAL_DESIGN.md` 存在且覆盖 retrieval eval + answer eval + 防作弊约束
  - [ ] Answer Eval 使用"三大维度 + 辅助指标"表述
  - [ ] 包含 8 条防作弊约束
- [ ] `docs/DEV_STATUS.md` 已更新为 M0 状态
- [ ] `docs/CHANGELOG.md` 已追加 M0 记录
- [ ] 只创建了 6 个文档，没有额外扩写
- [ ] backend 测试仍通过
- [ ] frontend 仍可 build
- [ ] git commit 完成
- [ ] git tag `m0-scope-locked` 已创建
