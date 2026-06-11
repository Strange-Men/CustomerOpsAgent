# CustomerOps Agent｜PRD

**版本**：v2.0
**日期**：2026-06-11
**状态**：Consolidated — 合并自 IDEA、MVP_SCOPE、PRD_DRAFT、PRD_REVIEW、PRD_FINAL、PROJECT_SCOPE

---

## 1. 项目定位

CustomerOps Agent 是面向跨境电商 / 3C 售后客服工单的**业务流程型多 Agent 系统**。

- **不是**普通聊天机器人（不是"用户问什么 AI 回什么"的问答模式）
- **不是** FAQ 系统（不是关键词匹配 + 模板回复）
- **不是**完整客服 SaaS（不做用户系统、权限管理、多租户、真实业务系统接入）

核心价值：用多 Agent 协作的方式，让每个 Agent 负责售后工单处理流程中的一个环节，通过 Orchestrator 编排执行顺序，最终输出带 evidence 的结构化处理建议。

---

## 2. 当前 MVP 目标

验证售后工单能否通过多 Agent 流程完成结构化处理：

```
工单输入
  → Intent Agent（意图识别）
  → Retrieval Agent（知识库检索）
  → Tool Agent（工具调用）
  → Policy Agent（政策判断）
  → Reply Agent（回复生成）
  → QA Agent（质检）
  → Final Result
```

---

## 3. Current MVP Scope

当前 Goal 模式**只实现**以下内容：

| # | 模块 | 说明 |
|---|------|------|
| 1 | 工单输入 | 前端页面输入 message（必填）、order_id（可选）、product_type（可选） |
| 2 | Intent Agent | 意图识别 + 实体提取 + 置信度输出 |
| 3 | Retrieval Agent | 本地 Markdown 知识库检索，输出 evidence |
| 4 | Tool Agent | 4 个 mock 工具：get_order、get_logistics、check_refund_window、create_ticket |
| 5 | Policy Agent | 简单条件判断（时间窗口 + 状态匹配），输出 eligible + suggestion + reason |
| 6 | Reply Agent | 基于上下文生成客服回复，回复需包含政策引用 |
| 7 | QA Agent | 规则检查（必要字段、超长、禁用词），输出 score + risks + need_human_review |
| 8 | Orchestrator | 固定线性流程编排 6 个 Agent |
| 9 | Analyze API | POST /api/analyze，返回完整分析结果 |
| 10 | Eval API | POST /api/eval，执行 10 条测试用例 |
| 11 | Health API | GET /api/health，健康检查 |
| 12 | 示例工单 | 10 条覆盖常见售后场景的示例 |
| 13 | 知识库 | 6 篇 Markdown 政策文档 |
| 14 | Agent Timeline | 前端展示 6 个 Agent 的执行状态 |
| 15 | Evidence 展示 | 前端展示检索到的政策文档片段 |
| 16 | Tool Result 展示 | 前端展示工具调用结果 |
| 17 | Reply 展示 | 前端展示客服回复建议 |
| 18 | QA 展示 | 前端展示质检结果 |
| 19 | Eval / Bad Case 页面 | 前端展示评估用例和结果 |
| 20 | 基础测试 | 核心 Agent 和 API 的单元测试 |

**实现约束**：

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

---

## 4. MVP Out of Scope but Future Possible

当前 MVP **不做**，但后续版本**可以做**。这些**不是永久禁止**，只是当前 MVP 不做：

| # | 功能 | 说明 |
|---|------|------|
| 1 | 真实 LLM | 替换 mock 响应为 OpenAI / Claude API 调用 |
| 2 | LangGraph 条件路由 | 根据工单类型动态选择 Agent 组合 |
| 3 | 动态 Agent 编排 | 不固定线性流程，按需编排 |
| 4 | Chroma / FAISS | 使用向量数据库进行语义检索 |
| 5 | 真实电商平台 API | 对接 Shopify / Amazon 等平台的订单和物流接口 |
| 6 | 真实物流 API | 对接真实物流服务商 |
| 7 | 历史工单 | 工单持久化存储和历史查询 |
| 8 | 人工审核工作台 | 客服主管审核 AI 建议的专用页面 |
| 9 | 知识库管理后台 | 可视化管理知识库文档 |
| 10 | 多轮客服会话 | 支持多轮对话，处理复杂工单 |
| 11 | Eval Dashboard | 更丰富的评估维度、指标和可视化 |
| 12 | Docker / 云部署 | 容器化部署，支持一键启动 |
| 13 | 用户登录 | 用户认证和登录系统 |
| 14 | 权限系统 | 角色权限控制 |
| 15 | 多租户 | 多团队 / 多组织支持 |

---

## 5. Permanent Safety Boundaries

以下安全边界**任何版本都不能突破**：

| # | 安全边界 | 说明 |
|---|---------|------|
| 1 | 不在前端暴露 API Key | 前端代码中不得出现任何密钥 |
| 2 | 不提交 .env | .env 文件必须在 .gitignore 中 |
| 3 | 不在日志打印密钥 | 日志中不得输出 API Key、Token 等敏感信息 |
| 4 | 不让 LLM 直接执行真实退款 | 系统只生成退款建议，不执行退款操作 |
| 5 | 不让 LLM 无审核发送真实客服消息 | 系统只生成回复建议，不自动发送 |
| 6 | 不无 evidence 承诺退款、赔偿或换货 | 回复必须有政策依据支撑 |
| 7 | 高风险投诉必须建议人工复核 | need_human_review 必须正确标记 |
| 8 | 真实业务动作必须经过人工确认 | 退款、换货等操作需人工确认后执行 |
| 9 | 用户输入必须校验 | 所有用户输入必须经过验证 |
| 10 | 工具调用必须走白名单 | 不允许任意工具调用 |
| 11 | LLM 输出必须结构化校验 | 使用 Pydantic Schema 约束 LLM 输出 |

---

## 6. Explicit Non-goals

即使后续版本也**不是**本项目重点：

| # | 非目标 | 说明 |
|---|--------|------|
| 1 | 完整客服 SaaS | 本项目是技术 MVP，不是要替代 Zendesk / Freshdesk |
| 2 | 通用聊天机器人平台 | 专注售后工单场景，不做通用对话 |
| 3 | 大而全 CRM | 不做客户关系管理 |
| 4 | 支付系统 | 不涉及任何资金操作 |
| 5 | 真实退款执行系统 | 只生成建议，不执行退款 |
| 6 | 复杂企业权限平台 | 不做 RBAC / ABAC 等复杂权限 |
| 7 | 移动端 App | 只做桌面端 Web |

---

## 7. 输入输出

### 系统输入

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 是 | 用户售后问题文本 |
| order_id | string | 否 | 订单号，如 ORD-2024-001 |
| product_type | string | 否 | 产品类型，如 earbuds、headphones |

### 系统输出

| 字段 | 类型 | 说明 |
|------|------|------|
| ticket_id | string | 工单唯一标识，自动生成 |
| intent_result | object | 意图识别结果（intent, entities, confidence） |
| evidence | array | 检索到的政策文档片段（source, content） |
| tool_results | object | 工具调用结果（order, logistics） |
| policy_result | object | 政策判断结果（eligible, suggestion, reason） |
| reply_result | object | 回复生成结果（reply） |
| qa_result | object | 质检结果（score, risks, suggestion） |
| need_human_review | boolean | 是否需要人工审核 |
| final_result | string | 最终处理建议（auto_reply / need_human_review） |

---

## 8. 核心场景

| # | 场景 | 关键点 |
|---|------|--------|
| 1 | 产品故障售后 | 完整流程，Agent 全部成功 |
| 2 | 退款 / 换货咨询 | 退款窗口判断 + 政策依据 |
| 3 | 物流查询 | Tool Agent 返回物流状态 |
| 4 | 发票问题 | Intent = invoice_request |
| 5 | 投诉 / 高风险工单 | need_human_review = true |
| 6 | 缺少订单号 | Tool Agent 返回 need_more_info |
| 7 | RAG 无结果 | Evidence 为空，建议转人工 |
| 8 | Tool 调用失败 | 工具异常处理，页面不崩溃 |
| 9 | QA 不通过 | 展示 issues 和建议，标记不建议发送 |

---

## 9. 后续版本路线

| 版本 | 重点 | 说明 |
|------|------|------|
| **MVP** | mock-first 可演示闭环 | 6 Agent + mock tools + 前端展示 + 基础 Eval |
| **V1** | 真实 LLM + structured output + LangGraph 条件路由 | 替换 mock 为真实 LLM，引入条件分支 |
| **V2** | 向量库 + RAG rerank + Eval Dashboard + 历史记录 | 语义检索增强，评估体系完善 |
| **V3** | 真实订单 / 物流 API + 人工审核工作台 | 对接真实业务系统 |
| **V4** | 用户系统、多租户、部署、监控、成本统计 | 产品化 |

---

## 10. Goal 模式开发规则

1. **Goal 模式只实现 Current MVP Scope**（第 3 节）
2. **不实现 Future Scope**（第 4 节）—— 这些是后续版本的事
3. **不突破 Permanent Safety Boundaries**（第 5 节）—— 任何版本都不能突破
4. **不实现 Non-goals**（第 6 节）—— 即使后续也不是重点
5. **如需扩展，必须先更新 PRD.md** —— 不得自行扩大范围
6. **不把后续版本功能提前塞进 MVP** —— 保持 MVP 轻量可控

---

## 附录：输入输出示例

### 示例输入

```json
{
  "message": "我的订单 ORD-2024-001 已经 10 天没收到货了，要求退款",
  "order_id": "ORD-2024-001",
  "product_type": "earbuds"
}
```

### 示例输出

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
