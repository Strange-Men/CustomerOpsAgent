# CustomerOps Agent｜初版 PRD

**版本**：Draft v1.0
**日期**：2026-06-11
**状态**：初版，待审查

---

## 1. 项目背景

跨境电商和 3C 产品售后客服每天面对大量重复性工单：物流延迟、退款申请、换货请求、发票问题、产品故障。客服人员需要在多个系统之间反复切换——查订单、查物流、翻政策文档、判断处理条件、写回复话术。一条工单平均耗时 5-15 分钟，高峰期积压严重。

传统解决方案有两种，但都有明显缺陷：

**纯人工处理**：效率低、新人误判率高、处理标准不统一、无法规模化。

**普通 AI 客服机器人**：只能做关键词匹配 + 模板回复，无法理解业务流程，不能调用订单/物流工具，没有政策判断逻辑，没有质检环节。

**核心问题**：售后工单处理是一个结构化的业务流程——识别意图、检索政策、查询数据、判断条件、生成回复、质量检查。这个流程不是自由对话，不能用普通聊天机器人解决。

CustomerOps Agent 的解决方案是：用多 Agent 协作的方式，让每个 Agent 负责流程中的一个环节，通过 Orchestrator 编排执行顺序，最终输出带 evidence 的结构化处理建议。

**本项目不是要替代真实客服系统**，而是验证"多 Agent 业务流程能否有效处理售后工单"这一技术假设。

---

## 2. 项目定位

### 2.1 CustomerOps Agent 是什么

CustomerOps Agent 是一个面向跨境电商 / 3C 售后客服工单的**业务流程型多 Agent 系统**。用户输入一条售后工单后，系统通过 6 个 Agent 的协作流程，完成意图识别、知识库检索、工具调用、政策判断、回复生成和 QA 质检，最终输出结构化的处理建议。

### 2.2 CustomerOps Agent 不是什么

| 它不是 | 为什么不是 |
|--------|-----------|
| 普通聊天机器人 | 不是"用户问什么 AI 回什么"的问答模式，而是固定的业务流程编排 |
| 简单 FAQ 系统 | 不是关键词匹配 + 模板回复，而是语义理解 + 业务逻辑判断 |
| 纯 RAG 文档问答 | 不只是检索文档回答问题，还需要调用工具、判断政策、生成回复、质检 |
| 完整客服 SaaS | 不做用户系统、权限管理、多租户、真实业务系统接入 |
| 通用 AI 助手 | 专注售后工单一垂直场景，不做其他业务 |

### 2.3 MVP 验证目标

MVP 只验证一件事：**一条售后工单能否通过多 Agent 流程完成结构化处理，输出带 evidence 的处理建议。**

---

## 3. 目标用户

| 用户角色 | 使用场景 | 核心需求 |
|---------|---------|---------|
| 跨境电商客服团队 | 日常处理售后工单 | 提高处理效率，减少重复劳动，标准化回复质量 |
| 3C 产品售后团队 | 处理电子产品退换货 | 准确判断退款/换货条件，减少误判，附带政策依据 |
| 中小电商运营人员 | 兼职客服处理售后 | 降低学习成本，系统自动提示处理建议 |
| 客服主管 | 监控客服质量 | 可追溯、可审核的处理记录，风险工单自动标记 |
| 技术评估者 | 评估系统能力 | 展示多 Agent 编排、RAG、Tool Calling、结构化输出等工程能力 |

**MVP 阶段重点**：AI Agent 应用开发场景。系统的核心价值是展示技术能力，而非替代真实客服系统。

---

## 4. 核心场景

### 场景 1：产品故障售后

**用户输入**：
```
"我买的蓝牙耳机左耳没声音了，订单号 ORD-2024-003，买了一个月"
```

**系统处理流程**：
1. Intent Agent：识别为"产品故障 + 维修/换货申请"
2. Retrieval Agent：检索 earbuds_faq.md（故障排查）、replacement_policy.md（换货政策）、after_sales_policy.md（保修政策）
3. Tool Agent：调用 get_order 查询订单状态和购买时间，调用 check_refund_window 检查售后窗口
4. Policy Agent：判断是否在保修期内、是否符合换货条件
5. Reply Agent：生成回复（含故障排查步骤 + 处理方案）
6. QA Agent：检查回复是否包含必要信息、是否承诺了不应承诺的内容

**系统输出**：
- 意图：product_fault + replacement_request
- 政策判断：在保修期内，符合换货条件
- 回复：包含故障排查步骤 + 换货流程说明
- QA：通过，无风险

### 场景 2：退款 / 换货咨询

**用户输入**：
```
"我要退款，收到的耳机和页面描述不一样，没有降噪功能"
```

**系统处理流程**：
1. Intent Agent：识别为"产品与描述不符 + 退款申请"
2. Retrieval Agent：检索 refund_policy.md、after_sales_policy.md
3. Tool Agent：调用 get_order 查询订单信息，调用 check_refund_window 检查退款窗口
4. Policy Agent：判断是否在退款窗口内、产品与描述不符是否属于无条件退款情形
5. Reply Agent：生成回复（含退款流程说明）
6. QA Agent：检查回复是否正确引用政策

**系统输出**：
- 意图：product_mismatch + refund_request
- 政策判断：产品与描述不符，支持无条件退款
- 回复：退款流程说明 + 预计到账时间
- QA：通过

### 场景 3：物流查询

**用户输入**：
```
"我的订单 ORD-2024-002 物流一直没更新，已经 8 天了"
```

**系统处理流程**：
1. Intent Agent：识别为"物流延迟查询"
2. Retrieval Agent：检索 logistics_policy.md
3. Tool Agent：调用 get_order 获取物流单号，调用 get_logistics 查询物流状态
4. Policy Agent：判断是否超过物流时效、是否符合退款/补偿条件
5. Reply Agent：生成回复（含物流状态 + 处理方案）
6. QA Agent：检查回复是否准确反映物流状态

**系统输出**：
- 意图：logistics_delay
- 政策判断：超过 7 天未更新，可申请退款或等待
- 回复：物流当前状态 + 两个选项（继续等待 / 申请退款）
- QA：通过

### 场景 4：发票问题

**用户输入**：
```
"我上个月买的耳机还没有收到发票，能帮我开一下吗"
```

**系统处理流程**：
1. Intent Agent：识别为"发票申请"
2. Retrieval Agent：检索 invoice_policy.md
3. Tool Agent：调用 get_order 查询订单信息和发票状态
4. Policy Agent：判断是否在开票时效内、开票类型
5. Reply Agent：生成回复（含开票流程说明）
6. QA Agent：检查回复是否准确

**系统输出**：
- 意图：invoice_request
- 政策判断：在开票时效内，可以补开
- 回复：开票流程说明 + 预计时间
- QA：通过

### 场景 5：投诉 / 高风险工单

**用户输入**：
```
"你们客服上次说 3 天处理，到现在都没人管！我要投诉到 12315！"
```

**系统处理流程**：
1. Intent Agent：识别为"投诉 + 高风险"
2. Retrieval Agent：检索 after_sales_policy.md（投诉处理流程）
3. Tool Agent：调用 get_order 查询历史工单
4. Policy Agent：判断为高风险工单，建议升级处理
5. Reply Agent：生成安抚性回复
6. QA Agent：标记为高风险，建议转人工

**系统输出**：
- 意图：complaint + high_risk
- 政策判断：高风险工单，需人工介入
- 回复：安抚性话术 + 承诺专人跟进
- QA：标记 need_human_review = true
- final_result：need_human_review

---

## 5. MVP 核心功能

### 5.1 工单输入

- 用户通过前端页面输入售后问题文本
- 可选填订单号（order_id）和产品类型（product_type）
- 提交后系统自动触发 Agent 流程

### 5.2 Intent Agent（意图识别）

- 接收用户原始文本
- 输出意图分类（退款 / 换货 / 物流 / 发票 / 投诉等）
- 提取关键实体（订单号、产品名、时间等）
- 输出置信度分数

### 5.3 Retrieval Agent（知识库检索）

- 接收意图和关键词
- 从本地 Markdown 知识库检索相关文档片段
- 输出检索到的 evidence 列表（含来源和内容）

### 5.4 Tool Agent（工具调用）

- 接收订单号等参数
- 调用 mock 工具获取订单/物流数据
- 4 个 mock 工具：get_order、get_logistics、check_refund_window、create_ticket
- 输出工具调用结果

### 5.5 Policy Agent（政策判断）

- 接收意图、工具结果、政策文档
- 根据业务规则判断是否符合条件
- 输出处理建议和政策依据

### 5.6 Reply Agent（客服回复生成）

- 接收所有上下文信息
- 生成专业客服回复文本
- 回复需包含政策依据

### 5.7 QA Agent（回复质检）

- 接收回复内容和业务规则
- 检查回复质量、风险和规范性
- 输出质量评分、风险提示、改进建议
- 高风险工单标记 need_human_review

### 5.8 Orchestrator（流程编排）

- 编排 6 个 Agent 的执行顺序
- 管理 Agent 之间的数据传递
- 处理异常和降级逻辑
- 生成 agent_trace 记录执行过程

### 5.9 Analyze API（工单分析接口）

- POST /api/analyze
- 接收工单输入，返回完整分析结果
- 统一响应格式：{code, message, data}

### 5.10 Example Cases（示例工单）

- 10 条覆盖常见售后场景的示例工单
- 包含预期输出，用于验证和演示

### 5.11 Eval / Bad Case（基础评估）

- 10 条测试用例
- 基础评估指标：意图准确率、政策判断准确率、回复质量
- POST /api/eval 执行评估

### 5.12 Frontend Display（前端展示）

- 工单输入页面
- Agent Timeline 组件：展示 6 个 Agent 的执行过程和状态
- 结果展示页面：展示意图、证据、工具结果、政策判断、回复、质检
- Eval 页面：展示测试用例和评估结果

---

## 6. 输入输出

### 6.1 系统输入

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 是 | 用户售后问题文本 |
| order_id | string | 否 | 订单号，如 ORD-2024-001 |
| product_type | string | 否 | 产品类型，如 earbuds、headphones |

**示例输入**：
```json
{
  "message": "我的订单 ORD-2024-001 已经 10 天没收到货了，要求退款",
  "order_id": "ORD-2024-001",
  "product_type": "earbuds"
}
```

### 6.2 系统输出

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
  "need_human_review": false,
  "final_result": "auto_reply"
}
```

---

## 7. 核心流程

### 7.1 固定流程

```
用户输入工单
    ↓
Intent Agent（意图识别）
    ↓
Retrieval Agent（知识库检索）
    ↓
Tool Agent（工具调用）
    ↓
Policy Agent（政策判断）
    ↓
Reply Agent（回复生成）
    ↓
QA Agent（质检）
    ↓
Final Result（最终结果）
```

### 7.2 每步职责和输入输出

| 步骤 | Agent | 职责 | 输入 | 输出 |
|------|-------|------|------|------|
| 1 | Intent Agent | 识别工单意图和提取实体 | 用户原始文本 (message) | intent (string), entities (object), confidence (float) |
| 2 | Retrieval Agent | 从本地知识库检索相关政策 | intent, keywords | evidence (array of {source, content}) |
| 3 | Tool Agent | 调用 mock 工具获取数据 | order_id, entities | tool_results (object) |
| 4 | Policy Agent | 根据政策和数据判断处理建议 | intent, evidence, tool_results | eligible (bool), suggestion (string), reason (string) |
| 5 | Reply Agent | 生成专业客服回复 | 全部上下文 | reply (string) |
| 6 | QA Agent | 检查回复质量和风险 | reply, policy_result, rules | score (float), risks (array), suggestion (string), need_human_review (bool) |

---

## 8. 验收标准

| # | 功能模块 | 验收标准 | 验证方式 |
|---|---------|---------|---------|
| 1 | 工单输入 | 用户能在前端输入 message、order_id、product_type 并提交 | 前端页面可操作 |
| 2 | Intent Agent | 输入任意售后文本，输出意图分类和置信度，置信度 ≥ 0.7 | 调用 API 返回 intent_result |
| 3 | Retrieval Agent | 输入意图关键词，返回至少 1 条 evidence，包含 source 和 content | 调用 API 返回 evidence 数组 |
| 4 | Tool Agent | 输入订单号，返回订单状态和物流状态（mock 数据） | 调用 API 返回 tool_results |
| 5 | Policy Agent | 输入意图和数据，返回 eligible 和 reason | 调用 API 返回 policy_result |
| 6 | Reply Agent | 输入上下文，返回非空回复文本，回复包含政策引用 | 调用 API 返回 reply_result |
| 7 | QA Agent | 输入回复，返回评分和风险列表，高风险标记 need_human_review | 调用 API 返回 qa_result |
| 8 | Orchestrator | 提交一条工单，6 个 Agent 按序执行，返回完整结果 | 调用 /api/analyze 返回完整 JSON |
| 9 | Analyze API | POST /api/analyze 返回 {code: 200, data: {...}} 格式 | HTTP 请求验证 |
| 10 | Example Cases | 10 条示例工单可正常运行，输出结构正确 | 批量调用验证 |
| 11 | Eval | POST /api/eval 执行 10 条测试用例，返回评估结果 | HTTP 请求验证 |
| 12 | Frontend | Agent Timeline 展示 6 个节点，结果页展示全部字段 | 浏览器访问验证 |
| 13 | 安全 | 代码中无硬编码 API Key，.gitignore 包含 .env | 代码审查 |

---

## 9. 暂不实现范围

以下功能在当前 MVP 版本中**明确不做**：

| 功能 | 不做的原因 |
|------|-----------|
| 用户登录 / 注册 | MVP 不需要用户系统，单用户模式 |
| 权限系统 | MVP 不需要权限控制 |
| 多租户 | MVP 只服务一个业务场景 |
| 真实支付 | MVP 使用 mock 数据，不涉及资金操作 |
| 真实退款 | MVP 只生成退款建议，不执行退款动作 |
| 真实电商平台 API | MVP 不接 Shopify / Amazon / 淘宝等平台 |
| 真实客服消息发送 | MVP 只生成回复建议，不发送到任何渠道 |
| 复杂知识库管理后台 | MVP 直接读取本地 Markdown 文件 |
| 大规模向量数据库 | MVP 使用本地文档检索，不部署 Chroma / FAISS |
| 异步任务队列 | MVP 使用同步处理，不引入 Celery 等 |
| 多语言客服 | MVP 只处理中文工单 |
| 复杂长期记忆 | MVP 不需要跨会话记忆 |
| 移动端适配 | MVP 只做桌面端展示 |
| 生产级部署 | MVP 本地运行即可 |

---

## 10. 风险点

| # | 风险 | 影响 | 控制方式 |
|---|------|------|---------|
| 1 | **多 Agent 过度设计风险** | Agent 职责划分过细，编排逻辑过于复杂，开发周期失控 | 固定 6 个 Agent 线性流程，不做条件分支和动态路由；Orchestrator 保持简单 |
| 2 | **RAG 检索不准** | 本地 Markdown 检索效果差，evidence 质量低 | MVP 使用关键词匹配 + 简单相似度，不做复杂向量检索；知识库文档内容精简且结构化 |
| 3 | **LLM 幻觉** | Agent 输出不准确或编造信息 | MVP 默认 mock-first，使用规则逻辑兜底；后续接真实 LLM 时加 Pydantic Schema 约束输出 |
| 4 | **mock 数据过假** | mock 工具返回的数据太简单，无法体现 Tool Calling 价值 | mock 数据需要有足够细节和变化，覆盖多种场景 |
| 5 | **前端做成普通聊天框** | 前端只展示对话，无法体现 Agent 流程和结构化结果 | 必须有 Agent Timeline 组件和结构化结果展示页面 |
| 6 | **Goal 模式开发时范围膨胀** | Claude 在 Goal 模式下可能自动添加登录、权限、数据库等功能 | PROJECT_SCOPE.md 明确边界，Goal 模式启动时必须读取并遵守 |

---

## 附录：文档版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| Draft v1.0 | 2026-06-11 | 初版 PRD，待审查 |
