# CustomerOps Agent｜最终 PRD

**版本**：Final v1.0
**日期**：2026-06-11
**状态**：已固化
**依据**：初版 PRD (04_PRD_DRAFT.md) + PRD 审查报告 (05_PRD_REVIEW.md)

---

## 1. 当前版本做什么

MVP 必做功能清单（15 项）：

| # | 功能 | 说明 |
|---|------|------|
| 1 | 工单输入 | 前端页面输入 message、order_id、product_type |
| 2 | Intent Agent | 意图识别 + 实体提取 + 置信度输出 |
| 3 | Retrieval Agent | 本地 Markdown 知识库检索，输出 evidence |
| 4 | Tool Agent | 调用 4 个 mock 工具（get_order、get_logistics、check_refund_window、create_ticket） |
| 5 | Policy Agent | 简单条件判断（时间窗口 + 状态匹配），输出 eligible + reason |
| 6 | Reply Agent | 基于上下文生成客服回复，回复需包含政策引用 |
| 7 | QA Agent | 规则检查（必要字段、超长、禁用词），输出 score + risks + need_human_review |
| 8 | Orchestrator | 固定线性流程编排 6 个 Agent |
| 9 | Analyze API | POST /api/analyze，返回完整分析结果 |
| 10 | Eval API | POST /api/eval，执行 10 条测试用例 |
| 11 | Health API | GET /api/health，健康检查 |
| 12 | 前端展示 | 工单输入 + Agent Timeline + 结果展示 + Eval 页面 |
| 13 | 示例工单 | 10 条覆盖常见售后场景的示例 |
| 14 | 知识库 | 6 篇 Markdown 政策文档 |
| 15 | 基础测试 | 核心 Agent 和 API 的单元测试 |

---

## 2. 当前版本不做什么

明确禁止功能清单（14 项）：

| # | 功能 | 禁止原因 |
|---|------|---------|
| 1 | 用户登录 / 注册 | MVP 单用户模式 |
| 2 | 权限系统 | MVP 不需要权限控制 |
| 3 | 多租户 | MVP 只服务一个场景 |
| 4 | 真实支付 | 涉及资金安全 |
| 5 | 真实退款 | 涉及资金安全，只生成建议 |
| 6 | 真实电商平台 API | MVP 不接外部系统 |
| 7 | 真实客服消息发送 | MVP 只生成建议 |
| 8 | 复杂知识库管理后台 | MVP 读本地文件 |
| 9 | 大规模向量数据库 | MVP 用本地检索 |
| 10 | 异步任务队列 | MVP 用同步处理 |
| 11 | 多语言客服 | MVP 只做中文 |
| 12 | 复杂长期记忆 | MVP 不需要跨会话 |
| 13 | 移动端适配 | MVP 只做桌面端 |
| 14 | 生产级部署 | MVP 本地运行 |

---

## 3. 用户如何使用

### 完整使用路径

```
步骤 1：打开前端页面
    ↓
步骤 2：在输入框填写售后问题（必填）
    ↓
步骤 3：可选填写订单号和产品类型
    ↓
步骤 4：点击"提交分析"按钮
    ↓
步骤 5：等待 Agent 流程执行（页面展示 Agent Timeline）
    ↓
步骤 6：查看分析结果
    ├── 意图识别结果
    ├── 检索到的政策证据
    ├── 工具查询结果
    ├── 政策判断结果
    ├── 客服回复建议
    └── QA 质检结果
    ↓
步骤 7：如果 need_human_review = true，标记为需要人工处理
```

---

## 4. 系统输入

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 是 | 用户售后问题文本 |
| order_id | string | 否 | 订单号，如 ORD-2024-001 |
| product_type | string | 否 | 产品类型，如 earbuds、headphones |

**示例**：
```json
{
  "message": "我的订单 ORD-2024-001 已经 10 天没收到货了，要求退款",
  "order_id": "ORD-2024-001",
  "product_type": "earbuds"
}
```

---

## 5. 系统输出

| 字段 | 类型 | 说明 |
|------|------|------|
| ticket_id | string | 工单唯一标识，自动生成 |
| intent_result | object | 意图识别结果 |
| intent_result.intent | string | 意图分类 |
| intent_result.entities | object | 提取的实体 |
| intent_result.confidence | float | 置信度（0-1） |
| evidence | array | 检索到的政策文档片段 |
| evidence[].source | string | 文档来源 |
| evidence[].content | string | 文档内容片段 |
| tool_results | object | 工具调用结果 |
| tool_results.order | object | 订单信息 |
| tool_results.logistics | object | 物流信息 |
| policy_result | object | 政策判断结果 |
| policy_result.eligible | boolean | 是否符合条件 |
| policy_result.suggestion | string | 处理建议 |
| policy_result.reason | string | 判断依据 |
| reply_result | object | 回复生成结果 |
| reply_result.reply | string | 客服回复文本 |
| qa_result | object | 质检结果 |
| qa_result.score | float | 质量评分（0-1） |
| qa_result.risks | array | 风险列表 |
| qa_result.suggestion | string | 改进建议 |
| need_human_review | boolean | 是否需要人工审核 |
| final_result | string | 最终处理建议（auto_reply / need_human_review） |

**示例**：
```json
{
  "ticket_id": "TK-20240611-001",
  "intent_result": {
    "intent": "logistics_delay + refund_request",
    "entities": {"order_id": "ORD-2024-001"},
    "confidence": 0.92
  },
  "evidence": [
    {"source": "logistics_policy.md", "content": "物流超过7天未更新可申请退款..."},
    {"source": "refund_policy.md", "content": "购买后30天内可申请退款..."}
  ],
  "tool_results": {
    "order": {"status": "shipped", "shipped_at": "2024-06-01", "amount": 299.00},
    "logistics": {"status": "in_transit", "last_update": "2024-06-03"}
  },
  "policy_result": {
    "eligible": true,
    "suggestion": "建议同意退款",
    "reason": "物流超过7天未更新，符合退款条件"
  },
  "reply_result": {
    "reply": "尊敬的客户，非常抱歉给您带来不便。经查询您的订单..."
  },
  "qa_result": {
    "score": 0.95,
    "risks": [],
    "suggestion": "回复符合规范"
  },
  "need_human_review": false,
  "final_result": "auto_reply"
}
```

---

## 6. Agent 工作流

### 6.1 固定流程

```
Intent Agent → Retrieval Agent → Tool Agent → Policy Agent → Reply Agent → QA Agent → Final Result
```

流程为固定线性顺序，不做条件分支和动态路由。

### 6.2 Intent Agent

**职责**：识别工单意图，提取关键实体，输出置信度。

**输入**：
- message (string)：用户原始文本

**输出**：
- intent (string)：意图分类（refund / replacement / logistics / invoice / complaint）
- entities (object)：提取的实体（order_id、product_name、time 等）
- confidence (float)：置信度 0-1

**失败处理**：如果置信度 < 0.5，标记为低置信度，最终 need_human_review = true。

### 6.3 Retrieval Agent

**职责**：从本地 Markdown 知识库检索相关政策文档。

**输入**：
- intent (string)：意图分类
- keywords (array)：关键词列表

**输出**：
- evidence (array)：检索到的文档片段列表
  - source (string)：文档文件名
  - content (string)：文档内容片段

**失败处理**：如果未检索到任何文档，返回空数组，Policy Agent 使用默认规则判断。

### 6.4 Tool Agent

**职责**：调用 mock 工具获取订单和物流数据。

**输入**：
- order_id (string)：订单号
- entities (object)：其他实体信息

**输出**：
- tool_results (object)：
  - order (object)：订单信息（status、shipped_at、amount 等）
  - logistics (object)：物流信息（status、last_update 等）

**失败处理**：如果工具调用失败（如订单号不存在），返回错误信息，Policy Agent 标记数据不完整。

### 6.5 Policy Agent

**职责**：根据政策和数据判断是否符合条件。

**输入**：
- intent (string)：意图分类
- evidence (array)：政策文档片段
- tool_results (object)：工具调用结果

**输出**：
- eligible (boolean)：是否符合条件
- suggestion (string)：处理建议
- reason (string)：判断依据

**失败处理**：如果数据不完整无法判断，eligible = null，标记 need_human_review = true。

### 6.6 Reply Agent

**职责**：生成专业客服回复。

**输入**：
- 全部上下文（intent、evidence、tool_results、policy_result）

**输出**：
- reply (string)：客服回复文本

**失败处理**：如果无法生成回复，返回默认模板回复，标记 need_human_review = true。

### 6.7 QA Agent

**职责**：检查回复质量和风险。

**输入**：
- reply (string)：回复文本
- policy_result (object)：政策判断结果

**输出**：
- score (float)：质量评分 0-1
- risks (array)：风险列表
- suggestion (string)：改进建议
- need_human_review (boolean)：是否需要人工审核

**失败处理**：如果检查出高风险（如承诺了不应承诺的内容），强制 need_human_review = true。

### 6.8 决定 need_human_review 的条件

以下任一条件满足，need_human_review = true：
- Intent Agent 置信度 < 0.5
- Policy Agent 判断数据不完整
- QA Agent 检测到高风险
- 工单包含投诉关键词

---

## 7. 功能验收标准

| # | 功能模块 | 验收标准 | 验证方式 |
|---|---------|---------|---------|
| 1 | 工单输入 | 前端页面可输入 message（必填）、order_id（可选）、product_type（可选）并提交 | 浏览器操作 |
| 2 | Intent Agent | 输入售后文本 → 输出 intent + entities + confidence，confidence ≥ 0.7 | 单元测试 + API 调用 |
| 3 | Retrieval Agent | 输入关键词 → 返回 ≥ 1 条 evidence，每条含 source 和 content | 单元测试 + API 调用 |
| 4 | Tool Agent | 输入订单号 → 返回 order + logistics 数据 | 单元测试 + API 调用 |
| 5 | Policy Agent | 输入意图+数据 → 返回 eligible + reason | 单元测试 + API 调用 |
| 6 | Reply Agent | 输入上下文 → 返回非空 reply，reply 包含政策引用 | 单元测试 + API 调用 |
| 7 | QA Agent | 输入回复 → 返回 score + risks + suggestion + need_human_review | 单元测试 + API 调用 |
| 8 | Orchestrator | 提交工单 → 6 个 Agent 按序执行 → 返回完整结果 | 集成测试 |
| 9 | Analyze API | POST /api/analyze → 返回 {code: 200, data: {...}} | HTTP 测试 |
| 10 | Eval API | POST /api/eval → 执行 10 条用例 → 返回评估结果 | HTTP 测试 |
| 11 | Health API | GET /api/health → 返回 {status: "ok"} | HTTP 测试 |
| 12 | 前端展示 | Agent Timeline 展示 6 个节点 + 状态；结果页展示全部字段 | 浏览器操作 |
| 13 | 示例工单 | 10 条示例可正常运行，输出结构正确 | 批量调用 |
| 14 | Eval | 10 条测试用例可执行，返回评估结果 | API 调用 |
| 15 | 安全 | 无硬编码 API Key；.gitignore 包含 .env | 代码审查 |
| 16 | 测试 | 核心模块测试覆盖率 > 60% | 测试运行 |

---

## 8. 最终 MVP 成功标准

MVP 完成后必须满足以下**所有**条件：

| # | 成功标准 | 说明 |
|---|---------|------|
| 1 | 用户能提交售后工单 | 前端输入页面可用，提交后触发 Agent 流程 |
| 2 | 系统能跑完整 Agent 流程 | 6 个 Agent 按序执行，Orchestrator 编排成功 |
| 3 | 前端能展示流程和结果 | Agent Timeline 展示 6 个节点，结果页展示全部字段 |
| 4 | 回复包含 evidence | Reply Agent 生成的回复引用了 Retrieval Agent 检索的政策 |
| 5 | 高风险/低置信度能转人工 | need_human_review 字段正确标记 |
| 6 | Eval 至少有固定样例 | 10 条测试用例可执行并返回结果 |
| 7 | 后端有基础测试 | 核心 Agent 和 API 有单元测试，覆盖率 > 60% |
| 8 | 不暴露密钥 | 代码中无硬编码 API Key |
| 9 | 不接真实业务系统 | 所有工具为 mock 实现 |

---

## 附录：实现约束

| 维度 | 约束 |
|------|------|
| Agent | 每个 Agent 单一职责，内部逻辑不超过 100 行 |
| Orchestrator | 固定线性流程，不做条件分支和动态路由 |
| RAG | 关键词匹配 + 本地文件读取，不做向量检索 |
| Tool | mock 实现，返回预设数据，不执行真实操作 |
| Policy | 简单条件判断（时间窗口 + 状态匹配），不做规则引擎 |
| QA | 规则检查（必要字段、超长、禁用词），不做 NLP 质检 |
| 前端 | 最简单组件实现，不做复杂交互 |
| 测试 | 核心模块单元测试，不做复杂集成测试 |
| Eval | 固定用例执行 + 简单对比，不做自动评估框架 |
