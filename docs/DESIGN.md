# CustomerOps Agent｜设计文档

**版本**：v2.0
**日期**：2026-06-11
**状态**：Consolidated — 合并自 DESIGN_GUIDE、PAGE_PLAN、USER_FLOW、FRONTEND_DESIGN_REFERENCE

---

## 1. 设计定位

CustomerOps Agent 是 **ToB 客服工单处理工作台**，不是聊天机器人页面，不是 landing page，不是 demo 展示页。

核心价值：**让客服人员看到 AI Agent 如何处理一条工单，并审核其结果。**

设计关键词：

| 关键词 | 含义 |
|--------|------|
| Professional | 专业、可信、可交付 |
| Structured | 结构化展示，信息有层级 |
| Auditable | 结果可审核、可追溯 |
| Operational | 面向日常运营，不是面向演示 |

---

## 2. 视觉基调

### 色彩

| 用途 | 色彩 | 说明 |
|------|------|------|
| 主色 | `#1E40AF`（Blue-700）至 `#3B82F6`（Blue-500） | 企业蓝 |
| 背景色 | `#F8FAFC`（Slate-50）至 `#F1F5F9`（Slate-100） | 浅灰白 |
| 文字主色 | `#0F172A`（Slate-900） | 正文 |
| 文字次色 | `#64748B`（Slate-500） | 辅助说明 |
| 边框色 | `#E2E8F0`（Slate-200） | 卡片和分割线 |
| 卡片背景 | `#FFFFFF` | 纯白 |

**状态色**（只用于状态标识，不用于大面积装饰）：

| 状态 | 色彩 | 使用场景 |
|------|------|---------|
| Success | `#16A34A`（Green-600） | Agent 完成、QA 通过、auto_reply |
| Warning | `#D97706`（Amber-600） | 低置信度、需要关注 |
| Error | `#DC2626`（Red-600） | Agent 失败、QA 不通过、高风险 |
| Info | `#2563EB`（Blue-600） | 一般信息提示 |

### 字体

| 用途 | 字体 | 说明 |
|------|------|------|
| 正文 | 系统默认 sans-serif（Inter / -apple-system / 微软雅黑） | 14px，行高 1.6 |
| 标题 | 同上，font-weight 600-700 | 16-20px |
| 代码 / JSON | JetBrains Mono / Fira Code / monospace | 13px，行高 1.5 |

### 间距

采用 **4px 基础网格**：组件内 8-12px，卡片内边距 16-20px，卡片间距 16px，区块间距 24-32px。

### 卡片风格

白色背景、`1px solid #E2E8F0` 细边框、6-8px 圆角、极轻阴影或无阴影。用边框分隔区域，不依赖阴影。

### 状态色使用原则

- 状态色**只用于** StatusBadge、RiskBadge 和关键状态标记
- **不要**用状态色做大面积背景
- 高风险状态使用左侧色条（`border-left: 3px solid #DC2626`），不用整块红色背景

---

## 3. MVP 页面

当前 MVP **只做**以下页面：

| # | 页面 | 路由 | 说明 |
|---|------|------|------|
| 1 | 工单分析工作台 | `/` | 首页，输入工单 + 启动分析 |
| 2 | 分析结果详情 | `/result/:ticketId` | 展示完整 Agent 处理结果 |
| 3 | Eval / Bad Case | `/eval` | 展示评估用例和结果 |
| 4 | About / Architecture | 首页底部区域 | 项目简介，可选，不单独做页面 |

### Page 1：工单分析工作台

- **TicketInput**：textarea（必填）+ order_id + product_type + 提交按钮
- **ExampleTicketList**：5-6 条可点击的示例工单标签
- 提交后跳转结果页或在下方展示 Timeline + 结果

### Page 2：分析结果详情页

按优先级从上到下：

1. **AgentTimeline**：6 个 Agent 的执行状态时间线（左侧或顶部）
2. **FinalResultSummary**：最终处理建议（status + risk）
3. **ReplyCard**：客服回复草稿 + 复制按钮
4. **IntentResultCard**：意图识别结果
5. **EvidencePanel** + **ToolResultPanel**：并排或上下排列
6. **PolicyResultCard**：政策判断结果
7. **QAResultCard**：QA 质检结果
8. **RawJsonPanel**：完整 JSON（折叠）

### Page 3：Eval / Bad Case 页面

- **EvalControlBar**：运行按钮 + 通过/失败统计
- **EvalTable**：结果表格（ID / 输入 / Expected / Status / Issue）
- **CaseDetailPanel**：点击行展开 case 详情（Expected vs Actual）

---

## 4. Future Pages

以下页面**后续可以扩展**，但不进入当前 MVP：

| # | 页面 | 说明 |
|---|------|------|
| 1 | 历史工单页面 | 工单持久化后的历史查询 |
| 2 | 知识库管理页面 | 可视化管理知识库文档 |
| 3 | 人工审核工作台 | 客服主管审核 AI 建议 |
| 4 | Eval Dashboard | 更丰富的评估指标和可视化 |
| 5 | 系统设置页 | 配置管理 |
| 6 | 团队空间 / 多租户页面 | 多团队支持 |

---

## 5. 核心组件

| 组件 | 说明 |
|------|------|
| **TicketInput** | 工单输入表单（textarea + order_id + product_type + 提交按钮） |
| **ExampleTicketList** | 示例工单标签列表，点击自动填充 |
| **AgentTimeline** | 垂直时间线，6 个节点：Intent → Retrieval → Tool → Policy → Reply → QA |
| **AgentStepCard** | 可展开的详情卡片，展示 Agent 输入输出和耗时 |
| **EvidencePanel** | 政策引用列表，每条用白色卡片 + 左侧蓝色色条标记来源 |
| **ToolResultPanel** | 工具结果分组面板（Order / Logistics），键值对展示 |
| **PolicyResultCard** | 政策判断结果卡片，状态色左侧色条（绿/红/黄） |
| **ReplyCard** | 客服回复文本 + 复制按钮，绿色色条（auto_reply）/ 黄色色条（need_human_review） |
| **QAResultCard** | 质量评分 + 风险列表 + 改进建议 |
| **EvalTable** | 评估结果表格，Pass 绿色标签，Fail 红色标签 |
| **StatusBadge** | 圆角胶囊形状态标签（pending 灰 / running 蓝脉冲 / completed 绿 / failed 红） |
| **RiskBadge** | 红色风险标签（"高风险" / "需要人工审核" / "证据不足"） |
| **EmptyState** | 空内容占位（灰色图标 + 提示文字） |
| **ErrorState** | 错误占位（红色图标 + 错误描述 + 重试按钮） |
| **LoadingState** | Timeline 节点逐个完成，当前执行节点蓝色脉冲动画 |

---

## 6. 用户流程

### Flow 1：正常售后流程

```
用户输入工单 → Intent Agent → Retrieval Agent → Tool Agent → Policy Agent → Reply Agent → QA Agent
→ Timeline 全绿 → ReplyCard 绿色色条 → 可复制回复
```

### Flow 2：缺订单号流程

```
用户输入（无 order_id）→ Intent Agent → Retrieval Agent → Tool Agent（need_more_info）→ Policy Agent → Reply Agent → QA Agent
→ Timeline 节点 3 黄色 → ReplyCard 黄色色条 → 请求补充订单号
```

### Flow 3：物流查询流程

```
用户查询物流 → Intent=logistics → Retrieval → Tool（get_logistics）→ Policy → Reply（含物流状态）→ QA
→ ToolResultPanel 显示物流详情
```

### Flow 4：发票问题流程

```
用户请求开发票 → Intent=invoice → Retrieval（invoice_policy）→ Tool（get_order）→ Policy → Reply（请求开票信息）→ QA
→ PolicyResultCard 显示可以开票
```

### Flow 5：投诉高风险流程

```
用户投诉 → Intent=complaint（高风险标记）→ Retrieval → Tool → Policy（建议人工处理）→ Reply（安抚性）→ QA（need_human_review=true）
→ RiskBadge 红色标签 → 页面顶部醒目提示
```

### Flow 6：RAG 无结果流程

```
非售后问题 → Intent=other（低置信度）→ Retrieval（evidence=[]）→ Tool → Policy（无法判断）→ Reply（引导联系人工）→ QA（need_human_review=true）
→ EvidencePanel 空状态
```

### Flow 7：Tool 失败流程

```
订单号不存在 → Intent → Retrieval → Tool（error）→ Policy（数据不完整）→ Reply（说明无法查询）→ QA（need_human_review=true）
→ ToolResultPanel 红色错误标记
```

### Flow 8：QA 不通过流程

```
回复质量问题 → ... → Reply → QA（score 低，risks 列表）→ need_human_review=true
→ QAResultCard 红色标记 → ReplyCard 红色色条 → 不显示复制按钮
```

### Flow 9：Eval 流程

```
打开 Eval 页 → 点击"运行全部评估" → 逐条执行 → 对比 expected vs actual → 展示 pass/fail
→ 统计通过率 → 点击行展开详情
```

### 通用规则

- **页面不崩溃**：任何 Agent 失败或 Tool 调用失败，页面都不崩溃
- **状态色一致**：绿 = 成功，黄 = 警告，红 = 失败
- **need_human_review 触发条件**：Intent 置信度 < 0.5 / Policy 数据不完整 / QA 检测高风险 / 投诉关键词 / Tool 调用失败
- **回复安全原则**：高风险不承诺赔偿、信息不足请求补充、工具失败说明无法查询

---

## 7. 禁止风格

以下风格**明确禁止**：

| 禁止项 | 原因 |
|--------|------|
| 普通聊天机器人页面 | 重点是 Agent 工作流和结构化结果，不是对话 |
| 大面积紫色渐变 | 不符合 ToB 专业气质 |
| 玻璃拟态堆砌 | 影响可读性，不适合信息密集后台 |
| 炫酷动画优先 | 分散注意力，不适合运营工作台 |
| Landing page 风格大于业务系统 | 营销风格不适合日常工作台 |
| 没有信息层级的卡片堆叠 | 所有信息同等权重 = 没有权重 |
| 只展示最终答案，不展示 Agent 流程、evidence、tool result、QA | Agent 的价值在于可追溯的过程 |
