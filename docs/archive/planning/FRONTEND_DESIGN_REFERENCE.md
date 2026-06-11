# CustomerOps Agent｜前端设计参考

**版本**：v1.0
**日期**：2026-06-11
**阶段**：Module 3 产品设计与页面流程

---

## 1. 设计参考来源

本节总结 CustomerOps Agent 可借鉴的产品类型和设计原则，不复制任何具体网页。

### 1.1 企业后台系统

**可借鉴点**：

- 清晰的信息层级（标题 → 摘要 → 详情）
- 标准化的表单布局（标签 → 输入 → 操作）
- 数据表格的规范展示（表头 → 行 → 分页）
- 状态标记的一致性（badge / tag / status dot）

**代表产品类型**：ERP、CRM、客服系统后台

### 1.2 工单处理系统

**可借鉴点**：

- 工单卡片的信息密度（工单号、状态、时间、操作）
- 工单详情页的多区域布局（基本信息 + 处理记录 + 操作区）
- 状态流转的可视化（状态标签 + 时间线）
- 操作按钮的优先级（主操作突出，次操作弱化）

**代表产品类型**：Jira、Zendesk、Freshdesk

### 1.3 电商商家后台

**可借鉴点**：

- 任务驱动的页面设计（待处理事项 → 处理 → 完成）
- 数据概览与详情的层级关系
- 批量操作与单条操作的共存
- 审核流程的可视化

**代表产品类型**：Shopify Admin、淘宝商家中心

### 1.4 AI 工作流可视化页面

**可借鉴点**：

- 流程节点的状态展示（pending → running → completed）
- 节点之间的连线和依赖关系
- 每个节点的输入输出展示
- 错误节点的高亮和错误信息展示

**代表产品类型**：LangSmith、Langflow、Dify

### 1.5 数据分析 Dashboard

**可借鉴点**：

- 数据卡片的布局（关键指标 → 趋势 → 详情）
- 图表与表格的配合使用
- 筛选和排序的操作体验
- 导出和分享功能

**代表产品类型**：Grafana、Metabase、Mixpanel

---

## 2. 可借鉴设计系统

### 2.1 Ant Design

**推荐参考内容**：

- 表单组件的规范（输入框、选择器、按钮）
- 表格组件的规范（列定义、排序、筛选）
- 卡片组件的规范（标题、内容、操作）
- 状态标签的规范（Tag、Badge）
- 布局组件的规范（Grid、Layout）

**不参考内容**：

- Ant Design 的蓝色主题可参考，但不完全照搬
- 不使用 Ant Design 的 ProComponents（过重）

### 2.2 Material Design

**推荐参考内容**：

- 信息层级理论（Elevation、Surface）
- 卡片设计规范（Card）
- 表格设计规范（Data Table）
- 状态反馈规范（Snackbar、Dialog）

**不参考内容**：

- Material Design 的圆角风格（CustomerOps 用更小圆角）
- Material Design 的 FAB 按钮（不适合 ToB 后台）

### 2.3 Shopify Polaris

**推荐参考内容**：

- 商家后台的页面布局（Page、Layout、Card）
- 表单设计规范（Form Layout）
- 状态标记规范（Badge）
- 空状态设计（Empty State）

**不参考内容**：

- Polaris 的品牌色（CustomerOps 用企业蓝）

### 2.4 Atlassian Design System

**推荐参考内容**：

- 工作流相关的组件设计
- 表格和列表的规范
- 面包屑导航的规范
- 操作反馈的规范

**不参考内容**：

- Atlassian 的品牌色

### 2.5 shadcn/ui

**推荐参考内容**：

- 组件的设计思路（可定制、可组合）
- 颜色系统的组织方式（CSS 变量）
- 组件的 API 设计

**适用场景**：

- 如果前端使用 React + Tailwind CSS，可以考虑基于 shadcn/ui 构建

### 2.6 Tailwind UI

**推荐参考内容**：

- 页面布局的模式（侧边栏 + 主内容区）
- 表单布局的模式
- 表格布局的模式
- 卡片布局的模式

---

## 3. 页面设计关键词

以下关键词定义了 CustomerOps Agent 前端设计的核心方向：

| 关键词 | 含义 | 设计影响 |
|--------|------|---------|
| enterprise dashboard | 企业级仪表盘 | 信息密度高，布局规范 |
| agent workflow | Agent 工作流 | Timeline 组件，节点状态 |
| support ticket console | 客服工单控制台 | 工单输入，结果审核 |
| evidence-first AI | 证据优先的 AI | Evidence 展示优先级高 |
| human review | 人工审核 | need_human_review 状态突出 |
| operation workspace | 运营工作台 | 操作驱动，非浏览驱动 |
| structured result | 结构化结果 | 分区域展示，非自由文本 |
| audit trail | 审计追踪 | Timeline + Agent Trace |

---

## 4. 禁止的前端风格

以下风格**明确禁止**在 CustomerOps Agent 中使用：

| 禁止项 | 原因 |
|--------|------|
| 普通聊天机器人页面 | 本系统重点是 Agent 工作流和结构化结果，不是对话 |
| 大面积紫色渐变 | 不符合 ToB 专业气质，过于 consumer 风格 |
| 过多玻璃拟态（Glassmorphism） | 影响可读性，不适合信息密集的后台 |
| 过度炫酷动画 | 分散注意力，不适合运营工作台 |
| Landing page 风格大于业务系统 | 营销风格不适合日常工作台 |
| 没有信息层级的卡片堆叠 | 所有信息同等权重 = 没有权重 |
| 只展示最终答案，不展示过程 | Agent 的价值在于可追溯的过程 |
| 只展示聊天气泡，不展示证据和工具调用 | 聊天气泡无法展示结构化信息 |

---

## 5. 推荐布局方案

### 5.1 方案 A：左右分栏（推荐）

```
┌─────────────────────────────────────────────────┐
│  顶部导航栏                                        │
├───────────────────┬─────────────────────────────┤
│                   │                             │
│  工单输入区         │  Agent Timeline              │
│  ─────────────── │  ─────────────────────── │
│  Example Tickets  │  IntentResultCard            │
│                   │  EvidencePanel               │
│                   │  ToolResultPanel             │
│                   │  PolicyResultCard            │
│                   │  ReplyCard                   │
│                   │  QAResultCard                │
│                   │                             │
└───────────────────┴─────────────────────────────┘
```

**适用**：工单分析工作台 + 结果详情（合并为单页）

### 5.2 方案 B：上下布局

```
┌─────────────────────────────────────────────────┐
│  顶部导航栏                                        │
├─────────────────────────────────────────────────┤
│  工单输入区（顶部，全宽）                             │
├─────────────────────────────────────────────────┤
│  Agent Timeline（左侧）    │  结果详情（右侧）        │
│                           │                       │
└─────────────────────────────────────────────────┘
```

**适用**：输入区需要更大空间时

### 5.3 Eval 页面布局

```
┌─────────────────────────────────────────────────┐
│  顶部导航栏                                        │
├─────────────────────────────────────────────────┤
│  Eval 控制区（运行按钮 + 统计）                      │
├─────────────────────────────────────────────────┤
│  EvalTable（结果表格）                              │
│  ┌─────────────────────────────────────────┐    │
│  │ ID | 输入 | Expected | Actual | Status   │    │
│  └─────────────────────────────────────────┘    │
├─────────────────────────────────────────────────┤
│  CaseDetailPanel（点击行后展开）                     │
└─────────────────────────────────────────────────┘
```

### 5.4 结果页组件排列建议

按优先级从上到下排列：

1. AgentTimeline（左侧或顶部，始终可见）
2. FinalResultSummary（状态 + 风险标记）
3. ReplyCard（客服回复，核心输出）
4. IntentResultCard（意图识别）
5. EvidencePanel + ToolResultPanel（并排或上下排列）
6. PolicyResultCard（政策判断）
7. QAResultCard（QA 质检）
8. RawJsonPanel（折叠，最后）

---

## 6. 后续 Goal 模式的前端指令摘要

以下指令供后续 Goal 模式开发前端时直接读取：

---

**前端开发指令**：

CustomerOps Agent 的前端必须做成**专业 ToB 工单处理工作台**，重点展示 Agent 流程、结构化结果、evidence、tool results、QA 质检和人工复核状态。

**必须做到**：

- 使用 Agent Timeline 展示 6 个 Agent 的执行状态
- 使用结构化卡片展示每个 Agent 的输出
- Evidence 和 Tool Results 有独立展示区域
- QA 质检结果包含评分、风险列表和改进建议
- need_human_review 状态有醒目提示
- 回复草稿区域可复制

**不允许**：

- 不允许做成普通聊天机器人页面
- 不允许只展示最终答案不展示过程
- 不允许大面积渐变、玻璃拟态、过度动画
- 不允许没有信息层级的卡片堆叠
- 不允许隐藏 evidence 和 tool results

**设计基调**：

- 主色企业蓝（#1E40AF - #3B82F6）
- 背景浅灰白（#F8FAFC）
- 白色卡片 + 细边框（1px #E2E8F0）
- 状态色只用于状态标记（绿 = 成功，黄 = 警告，红 = 错误）
- 4px 基础网格
- 6-8px 圆角
- 极轻阴影或无阴影

**技术选型建议**：

- React + TypeScript（或 Vue 3 + TypeScript）
- Tailwind CSS（或 Ant Design）
- 状态管理：React hooks（MVP 不需要 Redux / Zustand）
- 路由：React Router（或 Vue Router）

---

## 7. 组件与设计系统对照

| CustomerOps 组件 | 可参考的设计系统组件 |
|-----------------|-------------------|
| TicketInput | Ant Design: Form + Input.Textarea |
| ExampleTicketList | Ant Design: Tag + Space |
| AgentTimeline | Ant Design: Timeline / 自定义 |
| AgentStepCard | Ant Design: Collapse + Card |
| EvidencePanel | Ant Design: List + Card |
| ToolResultPanel | Ant Design: Descriptions + Card |
| PolicyResultCard | Ant Design: Result + Alert |
| ReplyCard | Ant Design: Card + Typography.Paragraph |
| QAResultCard | Ant Design: Card + Progress + List |
| EvalTable | Ant Design: Table |
| StatusBadge | Ant Design: Badge / Tag |
| RiskBadge | Ant Design: Tag (color=red) |
| EmptyState | Ant Design: Empty |
| ErrorState | Ant Design: Result (status=error) + Button |
| LoadingState | Ant Design: Skeleton + Spin |

---

## 8. 颜色系统参考

### 8.1 主色板

```css
:root {
  /* 主色 */
  --color-primary: #2563EB;        /* Blue-600 */
  --color-primary-hover: #1D4ED8;  /* Blue-700 */
  --color-primary-light: #DBEAFE;  /* Blue-100 */

  /* 背景 */
  --color-bg-page: #F8FAFC;        /* Slate-50 */
  --color-bg-card: #FFFFFF;
  --color-bg-elevated: #F1F5F9;    /* Slate-100 */

  /* 文字 */
  --color-text-primary: #0F172A;   /* Slate-900 */
  --color-text-secondary: #64748B; /* Slate-500 */
  --color-text-tertiary: #94A3B8;  /* Slate-400 */

  /* 边框 */
  --color-border: #E2E8F0;         /* Slate-200 */
  --color-border-hover: #CBD5E1;   /* Slate-300 */

  /* 状态色 */
  --color-success: #16A34A;        /* Green-600 */
  --color-warning: #D97706;        /* Amber-600 */
  --color-error: #DC2626;          /* Red-600 */
  --color-info: #2563EB;           /* Blue-600 */
}
```

### 8.2 状态色背景

```css
/* 状态色只用于标记，不用做大面积背景 */
--color-success-light: #F0FDF4;    /* Green-50 */
--color-warning-light: #FFFBEB;    /* Amber-50 */
--color-error-light: #FEF2F2;      /* Red-50 */
--color-info-light: #EFF6FF;       /* Blue-50 */
```
