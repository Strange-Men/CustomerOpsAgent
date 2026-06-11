# CustomerOps Agent｜核心用户流程

**版本**：v1.0
**日期**：2026-06-11
**阶段**：Module 3 产品设计与页面流程

---

## 流程总览

| # | 流程 | 场景 | 关键点 |
|---|------|------|--------|
| 1 | 正常产品故障售后 | 耳机故障 + 退款 | 完整流程，Agent 全部成功 |
| 2 | 缺少订单号 | 用户没给订单号 | Tool Agent 返回 need_more_info |
| 3 | 物流查询 | 查询物流状态 | Intent = logistics |
| 4 | 发票问题 | 开票 / 补票 | Intent = invoice |
| 5 | 投诉 / 高风险 | 投诉 + 高风险 | need_human_review = true |
| 6 | RAG 无结果 | 知识库未命中 | Evidence 为空 |
| 7 | Tool 调用失败 | 订单查询失败 | 工具异常处理 |
| 8 | QA 不通过 | 回复质量不达标 | 展示 issues 和建议 |
| 9 | Eval / Bad Case | 评估用例运行 | Expected vs Actual |

---

## Flow 1：正常产品故障售后流程

### 用户输入

```
"我的耳机刚买三天，左耳没声音，订单号 ORD-2024-001，可以退款吗？"
```

### Agent 执行顺序

```
Intent Agent → Retrieval Agent → Tool Agent → Policy Agent → Reply Agent → QA Agent
```

### 详细流程

#### Step 1：Intent Agent

| 项目 | 内容 |
|------|------|
| 输入 | "我的耳机刚买三天，左耳没声音，订单号 ORD-2024-001，可以退款吗？" |
| 输出 | intent: "product_defect + refund_request" |
| | entities: { order_id: "ORD-2024-001", product: "earbuds", issue: "左耳没声音" } |
| | confidence: 0.95 |
| 前端展示 | Timeline 节点 1 变绿，IntentResultCard 显示意图和置信度 |

#### Step 2：Retrieval Agent

| 项目 | 内容 |
|------|------|
| 输入 | intent: "product_defect", keywords: ["耳机", "故障", "退款", "左耳没声音"] |
| 输出 | evidence: [ |
| |   { source: "earbuds_faq.md", content: "耳机单侧无声问题排查..." }, |
| |   { source: "refund_policy.md", content: "购买后30天内可申请退款..." }, |
| |   { source: "after_sales_policy.md", content: "产品故障售后处理流程..." } |
| | ] |
| 前端展示 | Timeline 节点 2 变绿，EvidencePanel 显示 3 条政策引用 |

#### Step 3：Tool Agent

| 项目 | 内容 |
|------|------|
| 输入 | order_id: "ORD-2024-001" |
| 调用 | get_order("ORD-2024-001") |
| 输出 | order: { status: "delivered", amount: 299.00, purchased_at: "2026-06-08" } |
| 调用 | check_refund_window("ORD-2024-001") |
| 输出 | refund_window: { eligible: true, days_remaining: 27 } |
| 前端展示 | Timeline 节点 3 变绿，ToolResultPanel 显示订单和退款窗口信息 |

#### Step 4：Policy Agent

| 项目 | 内容 |
|------|------|
| 输入 | intent + evidence + tool_results |
| 判断 | 产品故障 + 30天内 + 退款窗口有效 |
| 输出 | eligible: true |
| | suggestion: "建议同意退款" |
| | reason: "产品故障在30天退款窗口内，符合退款条件" |
| 前端展示 | Timeline 节点 4 变绿，PolicyResultCard 显示 "符合退款条件"（绿色） |

#### Step 5：Reply Agent

| 项目 | 内容 |
|------|------|
| 输入 | 全部上下文 |
| 输出 | reply: "尊敬的客户，非常抱歉给您带来不便。经查询，您的订单 ORD-2024-001 购买的耳机仍在30天退款窗口内。根据我们的售后政策，产品故障可申请退款处理。请您保留好商品及包装，我们将在3个工作日内为您处理退款。如有其他问题，请随时联系我们。" |
| 前端展示 | Timeline 节点 5 变绿，ReplyCard 显示回复文本 + 复制按钮 |

#### Step 6：QA Agent

| 项目 | 内容 |
|------|------|
| 输入 | reply + policy_result |
| 检查 | 包含订单号 ✓、包含政策依据 ✓、无禁用词 ✓、长度适中 ✓ |
| 输出 | score: 0.95 |
| | risks: [] |
| | suggestion: "回复符合规范" |
| | need_human_review: false |
| 前端展示 | Timeline 节点 6 变绿，QAResultCard 显示评分 0.95 |

### 前端最终展示

1. Timeline 全绿（6/6 完成）
2. FinalResultSummary：auto_reply，风险低
3. ReplyCard：绿色色条，回复文本，复制按钮
4. EvidencePanel：3 条政策引用
5. ToolResultPanel：订单信息 + 退款窗口
6. PolicyResultCard：符合退款条件
7. QAResultCard：评分 0.95，无风险

---

## Flow 2：缺少订单号流程

### 用户输入

```
"我的耳机左耳没声音，可以退款吗？"
```

（没有提供订单号）

### Agent 执行顺序

```
Intent Agent → Retrieval Agent → Tool Agent (need_more_info) → Policy Agent → Reply Agent → QA Agent
```

### 关键差异

#### Step 1：Intent Agent

| 项目 | 内容 |
|------|------|
| 输出 | intent: "product_defect + refund_request" |
| | entities: { order_id: null, product: "earbuds" } |
| | confidence: 0.85 |

#### Step 3：Tool Agent（关键差异）

| 项目 | 内容 |
|------|------|
| 输入 | order_id: null |
| 判断 | 无订单号，无法查询订单 |
| 输出 | status: "need_more_info" |
| | message: "缺少订单号，无法查询订单信息" |
| | tool_results: { order: null, logistics: null } |
| 前端展示 | Timeline 节点 3 变黄（warning），显示 "需要更多信息" |

#### Step 4：Policy Agent

| 项目 | 内容 |
|------|------|
| 输入 | intent + evidence + tool_results（数据不完整） |
| 判断 | 无订单数据，无法确认退款条件 |
| 输出 | eligible: null |
| | suggestion: "需要补充订单信息后才能判断" |
| | reason: "缺少订单号，无法确认购买时间和退款窗口" |

#### Step 5：Reply Agent

| 项目 | 内容 |
|------|------|
| 输出 | reply: "尊敬的客户，非常抱歉给您带来不便。关于耳机左耳无声的问题，我们需要您的订单号以便查询订单信息并为您处理退款申请。请您提供订单号（格式如 ORD-XXXX-XXX），我们将尽快为您处理。" |
| 前端展示 | ReplyCard 显示回复，黄色色条 |

#### Step 6：QA Agent

| 项目 | 内容 |
|------|------|
| 输出 | score: 0.70 |
| | risks: ["信息不足：缺少订单号"] |
| | suggestion: "请求用户补充订单号，符合流程" |
| | need_human_review: false |

### 前端最终展示

1. Timeline：节点 3 黄色，其余绿色
2. FinalResultSummary：需要补充信息
3. ReplyCard：黄色色条，请求订单号的回复
4. ToolResultPanel：显示 "需要更多信息" 提示
5. QAResultCard：评分 0.70，风险标记 "信息不足"

---

## Flow 3：物流查询流程

### 用户输入

```
"我的订单 ORD-2024-002 已经发货了，想查一下物流到哪了"
```

### Agent 执行顺序

```
Intent Agent → Retrieval Agent → Tool Agent → Policy Agent → Reply Agent → QA Agent
```

### 关键差异

#### Step 1：Intent Agent

| 项目 | 内容 |
|------|------|
| 输出 | intent: "logistics_inquiry" |
| | entities: { order_id: "ORD-2024-002" } |
| | confidence: 0.93 |

#### Step 2：Retrieval Agent

| 项目 | 内容 |
|------|------|
| 输出 | evidence: [ |
| |   { source: "logistics_policy.md", content: "物流查询处理流程..." } |
| | ] |

#### Step 3：Tool Agent

| 项目 | 内容 |
|------|------|
| 调用 | get_order("ORD-2024-002") |
| 输出 | order: { status: "shipped", shipped_at: "2026-06-09", tracking_no: "SF1234567890" } |
| 调用 | get_logistics("SF1234567890") |
| 输出 | logistics: { status: "in_transit", location: "深圳转运中心", estimated_delivery: "2026-06-13" } |
| 前端展示 | ToolResultPanel 显示物流详情 |

#### Step 4：Policy Agent

| 项目 | 内容 |
|------|------|
| 输出 | eligible: true |
| | suggestion: "物流正常运输中，预计6月13日到达" |
| | reason: "物流状态为运输中，无异常" |

#### Step 5：Reply Agent

| 项目 | 内容 |
|------|------|
| 输出 | reply: "尊敬的客户，经查询您的订单 ORD-2024-002 已于6月9日发货，快递单号 SF1234567890。当前包裹正在深圳转运中心，预计将于6月13日送达。请您耐心等待，如有其他问题请随时联系我们。" |

### 前端最终展示

1. IntentResultCard：意图 "物流查询"
2. ToolResultPanel：物流状态详情（当前位置、预计到达）
3. ReplyCard：包含物流信息的回复

---

## Flow 4：发票问题流程

### 用户输入

```
"我买了耳机需要开增值税专用发票，订单号 ORD-2024-003"
```

### Agent 执行顺序

```
Intent Agent → Retrieval Agent → Tool Agent → Policy Agent → Reply Agent → QA Agent
```

### 关键差异

#### Step 1：Intent Agent

| 项目 | 内容 |
|------|------|
| 输出 | intent: "invoice_request" |
| | entities: { order_id: "ORD-2024-003", invoice_type: "增值税专用发票" } |
| | confidence: 0.96 |

#### Step 2：Retrieval Agent

| 项目 | 内容 |
|------|------|
| 输出 | evidence: [ |
| |   { source: "invoice_policy.md", content: "发票开具政策：购买后30天内可申请..." } |
| | ] |

#### Step 3：Tool Agent

| 项目 | 内容 |
|------|------|
| 调用 | get_order("ORD-2024-003") |
| 输出 | order: { status: "delivered", amount: 299.00, purchased_at: "2026-06-05" } |
| 说明 | 不需要调用退款工具，发票问题不涉及退款 |

#### Step 4：Policy Agent

| 项目 | 内容 |
|------|------|
| 判断 | 发票请求 + 30天内 + 已完成订单 |
| 输出 | eligible: true |
| | suggestion: "可以开具增值税专用发票" |
| | reason: "订单在开票时间窗口内" |

#### Step 5：Reply Agent

| 项目 | 内容 |
|------|------|
| 输出 | reply: "尊敬的客户，您的订单 ORD-2024-003 符合开票条件。请您提供以下信息以便我们为您开具增值税专用发票：1. 公司名称 2. 纳税人识别号 3. 地址电话 4. 开户行及账号。我们将在收到信息后3个工作日内为您开具发票。" |

### 前端最终展示

1. IntentResultCard：意图 "发票请求"
2. EvidencePanel：发票政策
3. PolicyResultCard：可以开票
4. ReplyCard：请求开票信息的回复

---

## Flow 5：投诉 / 高风险流程

### 用户输入

```
"你们这个耳机质量太差了！我要投诉！已经第三次出问题了！必须给我退款加赔偿！"
```

### Agent 执行顺序

```
Intent Agent → Retrieval Agent → Tool Agent → Policy Agent → Reply Agent → QA Agent
```

### 关键差异

#### Step 1：Intent Agent

| 项目 | 内容 |
|------|------|
| 输出 | intent: "complaint + refund_request" |
| | entities: { keywords: ["投诉", "质量差", "赔偿"] } |
| | confidence: 0.88 |
| 特殊 | 检测到投诉关键词，标记为高风险场景 |

#### Step 4：Policy Agent

| 项目 | 内容 |
|------|------|
| 输出 | eligible: null |
| | suggestion: "投诉工单需人工处理，不建议自动回复" |
| | reason: "用户明确投诉，且要求赔偿，属于高风险场景" |

#### Step 6：QA Agent

| 项目 | 内容 |
|------|------|
| 输出 | score: 0.40 |
| | risks: ["高风险投诉", "用户要求赔偿", "建议不直接承诺赔偿"] |
| | suggestion: "回复不能承诺赔偿金额，需转人工处理" |
| | need_human_review: true |

### 前端最终展示

1. **Timeline**：全部完成但最终状态标记为 "需要人工审核"
2. **FinalResultSummary**：红色标记，"need_human_review"
3. **RiskBadge**：显示 "高风险" 红色标签
4. **ReplyCard**：黄色色条，回复不包含赔偿承诺
5. **QAResultCard**：评分 0.40，红色风险列表
6. **人工审核提示**：页面顶部或回复区上方显示醒目提示 "此工单需要人工处理"

---

## Flow 6：RAG 无结果流程

### 用户输入

```
"我想问一下你们公司什么时候放假？"
```

（不属于售后场景，知识库无相关内容）

### Agent 执行顺序

```
Intent Agent → Retrieval Agent (empty) → Tool Agent → Policy Agent → Reply Agent → QA Agent
```

### 关键差异

#### Step 1：Intent Agent

| 项目 | 内容 |
|------|------|
| 输出 | intent: "other" |
| | entities: {} |
| | confidence: 0.35 |
| 特殊 | 低置信度，不属于已知售后场景 |

#### Step 2：Retrieval Agent（关键差异）

| 项目 | 内容 |
|------|------|
| 输入 | intent: "other", keywords: ["放假"] |
| 输出 | evidence: [] |
| 说明 | 知识库无相关内容，返回空数组 |
| 前端展示 | EvidencePanel 显示 "未检索到相关政策" 灰色提示 |

#### Step 4：Policy Agent

| 项目 | 内容 |
|------|------|
| 输出 | eligible: null |
| | suggestion: "非售后问题，建议转人工或引导用户" |
| | reason: "无法识别为售后相关意图，无政策依据" |

#### Step 5：Reply Agent

| 项目 | 内容 |
|------|------|
| 输出 | reply: "尊敬的客户，您的问题暂时无法通过自动客服处理。建议您联系人工客服获取帮助。如有售后相关问题（如退款、换货、物流查询等），请详细描述，我们将为您处理。" |

#### Step 6：QA Agent

| 项目 | 内容 |
|------|------|
| 输出 | score: 0.60 |
| | risks: ["低置信度", "无政策依据"] |
| | suggestion: "建议转人工" |
| | need_human_review: true |

### 前端最终展示

1. Timeline：节点 2（Retrieval）完成但显示 "无结果"
2. EvidencePanel：空状态，"未检索到相关政策"
3. FinalResultSummary：需要人工审核
4. ReplyCard：引导用户联系人工客服

---

## Flow 7：Tool 调用失败流程

### 用户输入

```
"我的订单 ORD-9999-999 没收到货，要求退款"
```

（订单号在 mock 数据中不存在）

### Agent 执行顺序

```
Intent Agent → Retrieval Agent → Tool Agent (error) → Policy Agent → Reply Agent → QA Agent
```

### 关键差异

#### Step 3：Tool Agent（关键差异）

| 项目 | 内容 |
|------|------|
| 调用 | get_order("ORD-9999-999") |
| 输出 | { status: "error", message: "订单号不存在" } |
| 前端展示 | Timeline 节点 3 变红（或黄色 warning），ToolResultPanel 显示错误信息 |

**关键设计**：页面不崩溃，错误被正常处理和展示。

#### Step 4：Policy Agent

| 项目 | 内容 |
|------|------|
| 输出 | eligible: null |
| | suggestion: "订单信息查询失败，需人工核实" |
| | reason: "无法获取订单数据，不能做出判断" |

#### Step 5：Reply Agent

| 项目 | 内容 |
|------|------|
| 输出 | reply: "尊敬的客户，我们暂时无法查询到订单 ORD-9999-999 的信息。请您核实订单号是否正确，或提供其他查询信息（如收件人手机号）。如需进一步帮助，建议联系人工客服。" |

#### Step 6：QA Agent

| 项目 | 内容 |
|------|------|
| 输出 | score: 0.55 |
| | risks: ["订单查询失败", "无法确认退款条件"] |
| | suggestion: "建议人工核实订单信息" |
| | need_human_review: true |

### 前端最终展示

1. Timeline：节点 3 红色/黄色，显示 "工具调用失败"
2. ToolResultPanel：红色错误标记，"订单号不存在"
3. FinalResultSummary：需要人工审核
4. ReplyCard：引导用户核实订单号

---

## Flow 8：QA 不通过流程

### 场景

Reply Agent 生成的回复存在问题（如缺少订单号引用、承诺了不应承诺的内容）。

### QA 检查结果

| 项目 | 内容 |
|------|------|
| 输出 | score: 0.30 |
| | risks: ["回复未引用政策依据", "回复过长（超过500字）", "包含敏感词 '保证退款'"] |
| | suggestion: "不建议直接发送，需要修改后重试" |
| | need_human_review: true |

### 前端最终展示

1. **QAResultCard**：红色背景标记，评分 0.30
2. **风险列表**：红色图标 + 风险描述列表
3. **改进建议**：显示 "不建议直接发送"
4. **ReplyCard**：红色色条，回复文本标记为 "不建议发送"
5. **操作按钮**：不显示 "复制回复" 按钮（或显示为灰色 disabled）

---

## Flow 9：Eval / Bad Case 流程

### 用户操作

1. 打开 Eval 页面
2. 点击 "运行全部评估" 按钮
3. 等待评估完成
4. 查看结果

### 评估执行

```
读取 10 条固定 eval cases
    ↓
逐条执行 Agent 流程
    ↓
对比 expected vs actual
    ↓
记录 pass / fail + issues
    ↓
返回评估结果
```

### 结果展示

#### 表格视图

| ID | 输入摘要 | Expected Intent | Actual Intent | Expected Policy | Actual Policy | Status | Issues |
|----|---------|-----------------|---------------|-----------------|---------------|--------|--------|
| 01 | 耳机故障退款 | product_defect + refund | product_defect + refund | eligible | eligible | Pass | - |
| 02 | 缺订单号 | need_more_info | need_more_info | uncertain | uncertain | Pass | - |
| 03 | 物流延迟 | logistics_delay | logistics_delay | eligible | eligible | Pass | - |
| 04 | 发票请求 | invoice | invoice | eligible | eligible | Pass | - |
| 05 | 投诉 | complaint | complaint | human_review | human_review | Pass | - |
| 06 | 窗口过期 | refund_request | refund_request | not_eligible | eligible | Fail | Policy 判断错误 |
| 07 | 丢件 | logistics_lost | logistics_inquiry | eligible | eligible | Fail | Intent 分类偏差 |
| ... | ... | ... | ... | ... | ... | ... | ... |

#### 统计

```
通过：8 / 10
失败：2 / 10
通过率：80%
```

#### Case 详情（点击行展开）

```
Case ID: 06
输入："我买的耳机两个月了，现在想退款"
Expected Intent: refund_request
Actual Intent: refund_request ✓

Expected Policy: not_eligible（超过30天退款窗口）
Actual Policy: eligible ✗

Issues: Policy Agent 未正确判断退款窗口过期
Improvement: Policy Agent 需增加时间窗口校验逻辑
```

### 前端状态

#### Loading

- 运行按钮 spinner + "评估中..."
- 表格 skeleton 占位

#### Success

- 统计区域显示通过率
- 表格显示每条结果
- Pass 行绿色标签，Fail 行红色标签

#### Error

- 单个 case 执行失败：该行 Status 显示 "Error"
- API 整体失败：表格上方红色错误提示

---

## 流程通用规则

### 1. 页面不崩溃

任何 Agent 失败或 Tool 调用失败，页面都不崩溃。错误被正常捕获和展示。

### 2. 状态色一致性

| 状态 | 颜色 | 含义 |
|------|------|------|
| 绿色 | 成功、通过、可自动回复 |
| 黄色 | 警告、需要关注、信息不足 |
| 红色 | 失败、高风险、不通过 |

### 3. need_human_review 触发条件

以下任一条件触发 need_human_review = true：

- Intent 置信度 < 0.5
- Policy Agent 判断数据不完整
- QA Agent 检测到高风险
- 工单包含投诉关键词
- Tool 调用失败

### 4. 回复安全原则

- 高风险工单的回复**不能承诺赔偿金额**
- 信息不足时**请求补充信息**，不做猜测判断
- 工具失败时**说明暂时无法查询**，不假装有数据
