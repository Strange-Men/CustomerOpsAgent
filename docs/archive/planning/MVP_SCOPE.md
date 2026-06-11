# CustomerOps Agent｜MVP 范围定义

## 1. MVP 一句话范围

当前 MVP 只验证"售后客服工单能否通过多 Agent 流程完成分类、检索、工具查询、政策判断、回复生成和质检"，不做真实业务系统接入。

## 2. 当前版本必须做

### 核心 Agent（6 个）

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| Intent Agent | 工单意图识别 | 用户原始输入 | 意图分类、关键实体、置信度 |
| Retrieval Agent | 知识库检索 | 意图、关键词 | 相关政策文档片段、来源 |
| Tool Agent | 工具调用 | 订单号、物流号 | 订单状态、物流状态 |
| Policy Agent | 售后政策判断 | 意图、订单信息、政策 | 是否符合条件、处理建议、依据 |
| Reply Agent | 客服回复生成 | 所有上下文 | 专业客服回复文本 |
| QA Agent | 质量检查 | 回复内容、业务规则 | 质量评分、风险提示、改进建议 |

### Orchestrator

- 编排 6 个 Agent 的执行顺序
- 管理 Agent 之间的数据传递
- 处理异常和降级逻辑

### API 层

| API | 方法 | 路径 | 功能 |
|-----|------|------|------|
| Analyze API | POST | /api/analyze | 提交工单，返回完整分析结果 |
| Eval API | POST | /api/eval | 执行评估，返回评估结果 |
| Health API | GET | /api/health | 健康检查 |

### Mock Tools（4 个）

| Tool | 功能 | 输入 | 输出 |
|------|------|------|------|
| get_order | 查询订单信息 | 订单号 | 订单状态、发货时间、金额 |
| get_logistics | 查询物流状态 | 物流单号 | 当前状态、位置、预计到达时间 |
| check_refund_window | 检查退款窗口 | 订单号、购买时间 | 是否在退款窗口内 |
| create_ticket | 创建工单 | 工单信息 | 工单号、创建时间 |

**注意**：所有 tools 都是 mock 实现，不执行真实业务动作。

### 知识库（6 篇 Markdown 文档）

| 文档 | 内容 |
|------|------|
| after_sales_policy.md | 售后总政策 |
| refund_policy.md | 退款政策 |
| replacement_policy.md | 换货政策 |
| logistics_policy.md | 物流政策 |
| invoice_policy.md | 发票政策 |
| earbuds_faq.md | 耳机产品 FAQ |

### 前端页面

| 页面/组件 | 功能 |
|----------|------|
| 工单输入 | 输入售后问题文本、可选订单号、产品类型 |
| Agent Timeline | 展示 6 个 Agent 的执行过程和状态 |
| 结果展示 | 展示意图、证据、工具结果、政策判断、回复、质检 |
| Eval 页面 | 展示测试用例和评估结果 |

### 示例工单（10 条）

覆盖常见售后场景：
- 物流延迟 + 退款申请
- 产品故障 + 换货申请
- 发票问题
- 退款窗口过期
- 物流丢件
- 产品与描述不符
- 配件缺失
- 安装问题
- 保修期内维修
- 投诉处理

### Eval / Bad Case

- 10 条测试用例
- 基础评估指标（意图准确率、政策判断准确率、回复质量）
- Bad Case 收集和展示

### 文档

- README.md：项目说明、启动方式、架构图
- docs/：完整项目文档

## 3. 当前版本不做

| 功能 | 原因 |
|------|------|
| 用户登录 | MVP 不需要用户系统 |
| 权限系统 | MVP 不需要权限控制 |
| 多租户 | MVP 只服务一个场景 |
| 真实电商平台接入 | MVP 不接真实业务系统 |
| 真实支付 | MVP 使用 mock 数据 |
| 真实退款 | MVP 使用 mock 数据 |
| 真实客服消息发送 | MVP 只生成建议，不发送 |
| 复杂知识库管理后台 | MVP 直接读取本地文件 |
| 在线向量数据库 | MVP 使用本地检索 |
| 异步任务队列 | MVP 使用同步处理 |
| 多语言客服 | MVP 只做中文 |
| 复杂会话记忆 | MVP 不需要多轮记忆 |
| 移动端适配 | MVP 只做桌面端 |

## 4. 当前版本的输入

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 用户售后问题文本 |
| order_id | string | 否 | 订单号，如 ORD-2024-001 |
| product_type | string | 否 | 产品类型，如 earbuds、headphones |
| ticket_id | string | 否 | 工单号，不传则自动生成 |

**示例输入**：
```json
{
  "text": "我的订单 ORD-2024-001 已经 10 天没收到货了，要求退款",
  "order_id": "ORD-2024-001",
  "product_type": "earbuds"
}
```

## 5. 当前版本的输出

| 字段 | 类型 | 说明 |
|------|------|------|
| ticket_id | string | 工单唯一标识 |
| intent_result | object | 意图识别结果（意图分类、实体、置信度） |
| evidence | array | 检索到的政策文档片段 |
| tool_results | object | 工具调用结果（订单、物流） |
| policy_result | object | 政策判断结果（是否符合、建议、依据） |
| reply_result | object | 回复生成结果（回复文本） |
| qa_result | object | 质检结果（评分、风险、建议） |
| final_result | string | 最终处理建议（auto_reply / need_human_review） |
| need_human_review | boolean | 是否需要人工审核 |
| agent_trace | array | Agent 执行轨迹（用于 Timeline 展示） |

**示例输出**：
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
  "final_result": "auto_reply",
  "need_human_review": false,
  "agent_trace": [
    {"agent": "IntentAgent", "status": "completed", "duration_ms": 120},
    {"agent": "RetrievalAgent", "status": "completed", "duration_ms": 85},
    {"agent": "ToolAgent", "status": "completed", "duration_ms": 200},
    {"agent": "PolicyAgent", "status": "completed", "duration_ms": 150},
    {"agent": "ReplyAgent", "status": "completed", "duration_ms": 180},
    {"agent": "QAAgent", "status": "completed", "duration_ms": 100}
  ]
}
```

## 6. 当前版本核心 Agent

| Agent | 输入 | 输出 | 核心逻辑 |
|-------|------|------|---------|
| Intent Agent | 用户文本 | 意图分类、实体、置信度 | 基于 prompt 的分类 |
| Retrieval Agent | 意图、关键词 | 政策文档片段 | 本地文档检索 |
| Tool Agent | 订单号、物流号 | 订单、物流数据 | 调用 mock tools |
| Policy Agent | 意图、数据、政策 | 处理建议 | 规则判断 |
| Reply Agent | 所有上下文 | 回复文本 | 基于 prompt 生成 |
| QA Agent | 回复、规则 | 质检结果 | 规则检查 |
| Orchestrator | 用户输入 | 完整结果 | 编排以上 Agent |

## 7. 当前版本核心工具

| Tool | 功能 | Mock 实现 |
|------|------|----------|
| get_order | 查询订单信息 | 返回预设订单数据 |
| get_logistics | 查询物流状态 | 返回预设物流数据 |
| check_refund_window | 检查退款窗口 | 基于时间计算 |
| create_ticket | 创建工单 | 生成工单号 |

**所有工具都是 mock 实现，不执行真实业务动作。**

## 8. 当前版本知识库范围

本地 Markdown 文档：

| 文档 | 内容概要 |
|------|---------|
| after_sales_policy.md | 售后总政策：适用范围、处理流程、时效要求 |
| refund_policy.md | 退款政策：退款条件、退款窗口、退款流程 |
| replacement_policy.md | 换货政策：换货条件、换货流程、运费承担 |
| logistics_policy.md | 物流政策：物流时效、延迟处理、丢件赔偿 |
| invoice_policy.md | 发票政策：开票时间、开票类型、补开发票 |
| earbuds_faq.md | 耳机产品 FAQ：常见问题、故障排查、保修政策 |

**知识库内容需要有实际价值，不能只是占位符。**

## 9. 当前版本验收标准

MVP 完成后必须满足以下所有条件：

| # | 验收项 | 验收方式 |
|---|--------|---------|
| 1 | 用户可以输入一条售后工单 | 前端输入页面可用 |
| 2 | 系统可以输出结构化分析结果 | API 返回完整 JSON |
| 3 | 至少 6 个 Agent 节点可见 | Agent Timeline 展示 6 个节点 |
| 4 | 至少 4 个 mock tools 可用 | Tool Agent 调用 4 个工具 |
| 5 | 至少 5 篇知识库文档可检索 | Retrieval Agent 返回 evidence |
| 6 | 最终回复包含 evidence | 回复附带政策依据 |
| 7 | 高风险或低置信度工单能建议转人工 | need_human_review 字段正确 |
| 8 | 前端能展示 Agent 执行过程 | Timeline 组件正常工作 |
| 9 | Eval 页面能展示至少 10 条 bad case / test case | Eval 页面可用 |
| 10 | 后端核心模块有测试 | 测试覆盖率 > 60% |
| 11 | 项目可本地启动 | README 有启动说明 |
| 12 | 不暴露 API Key | 代码中无硬编码 Key |
| 13 | 不提交 .env | .gitignore 包含 .env |
| 14 | README 能说明项目价值、启动方式和架构 | README 内容完整 |

## 10. 后续扩展方向

以下方向作为未来扩展，不进入 MVP：

| 扩展方向 | 说明 |
|---------|------|
| 接入真实 LLM | 替换 mock 响应为真实 LLM 调用 |
| 接入 Chroma / FAISS | 使用向量数据库进行语义检索 |
| 接入真实电商 API | 对接 Shopify、Amazon 等平台 |
| 接入真实客服系统 | 对接在线客服系统，自动发送回复 |
| Docker 部署 | 容器化部署，支持一键启动 |
| 更完整的 Eval 指标 | 更丰富的评估维度和指标 |
| 多轮客服会话 | 支持多轮对话，处理复杂工单 |
| 知识库管理后台 | 可视化管理知识库文档 |
