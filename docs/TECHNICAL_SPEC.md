# CustomerOps Agent｜技术规格文档

**版本**：v1.0
**日期**：2026-06-11
**状态**：Technical Foundation — Module 4 技术地基准备

---

## 1. 技术目标

本项目技术目标：

| # | 目标 | 说明 |
|---|------|------|
| 1 | 构建可本地运行的 AI Agent MVP | 使用 FastAPI + Next.js，前后端分离，本地开发优先 |
| 2 | 后端负责核心业务编排 | Agent 编排、RAG 检索、mock tools、Schema 校验、RESTful API |
| 3 | 前端负责工单处理工作台 | ToB 风格工单分析页面、Agent Timeline、结构化结果展示 |
| 4 | 默认 mock-first | 不依赖真实 LLM，mock 响应保证无外部服务也能完整演示 |
| 5 | 当前 MVP 只做闭环 | 不做真实业务系统接入，不接真实电商 / 物流 API |
| 6 | 后续可扩展 | 真实 LLM、LangGraph 条件路由、向量库、外部 API 均可后续替换，但不进入当前 MVP |

---

## 2. 技术栈锁定

### 2.1 Fixed Stack for MVP

以下技术栈在 MVP 阶段锁定，不更换。

#### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 主语言 |
| FastAPI | latest | Web 框架，提供 RESTful API |
| Pydantic v2 | latest | 数据校验、Schema 定义、结构化输出约束 |
| pytest | latest | 单元测试和集成测试 |
| ruff | latest | 代码格式化和 lint |
| SQLite / JSON file | — | MVP 轻量持久化，优先 JSON 文件，需要查询时用 SQLite |

#### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | latest (App Router) | 前端框架，SSR + 客户端组件 |
| React | latest | UI 库 |
| TypeScript | latest | 类型安全 |
| Tailwind CSS | latest | 原子化 CSS 样式 |
| shadcn/ui | 可选 | 基础 UI 组件，不强依赖，可用原生 HTML + Tailwind 替代 |

#### Agent / AI

| 技术 | 用途 |
|------|------|
| mock-first / rule-based | MVP 默认实现方式，不调用真实 LLM |
| Pydantic Schema | Agent 输出必须使用 Pydantic 模型约束 |
| LLM client 抽象接口 | 只定义接口 + mock 实现，真实 LLM 后续接入 |

#### RAG

| 技术 | 用途 |
|------|------|
| 本地 Markdown 知识库 | 6 篇政策文档作为知识源 |
| 关键词匹配 / BM25-like scoring | 简单检索，不做向量检索 |
| 不强制 Chroma / FAISS | 后续版本可替换 |

#### Tools

| 技术 | 用途 |
|------|------|
| mock tools only | 4 个 mock 工具，返回预设数据 |
| 不执行真实业务动作 | 不退款、不支付、不发消息 |

### 2.2 Future Replaceable Stack

以下技术在 MVP 阶段**不做**，但架构设计上保留替换空间：

| 技术 | 替换目标 |
|------|---------|
| LangGraph | 条件路由、动态 Agent 编排 |
| 真实 LLM（OpenAI / Claude） | 替换 mock 响应 |
| Chroma / FAISS | 向量检索，语义搜索 |
| RAG rerank | 检索结果重排序 |
| PostgreSQL | 替换 JSON / SQLite 做持久化 |
| Docker | 容器化部署 |
| 云部署 | 生产环境部署 |
| 真实订单 / 物流 API | 对接真实电商平台 |

---

## 3. 非功能需求

### 3.1 安全

| # | 安全要求 | 说明 |
|---|---------|------|
| 1 | API Key 只允许后端环境变量 | 前端代码中不得出现任何密钥 |
| 2 | 不提交 .env | .env 必须在 .gitignore 中 |
| 3 | 用户输入必须限制长度和校验 | 防止注入、XSS、超长输入 |
| 4 | 工具调用必须走白名单 | 不允许任意工具调用 |
| 5 | LLM 输出必须结构化校验 | 使用 Pydantic Schema 约束输出格式 |
| 6 | 高风险工单必须建议人工复核 | need_human_review 必须正确标记 |
| 7 | 不无 evidence 承诺退款、赔偿或换货 | 回复必须有政策依据 |
| 8 | mock tools 不执行真实操作 | 不退款、不支付、不发客服消息 |

### 3.2 性能

| # | 性能要求 | 说明 |
|---|---------|------|
| 1 | 单次分析可接受地返回 | MVP 不做性能优化，但不能明显卡顿 |
| 2 | 避免重复检索和重复工具调用 | 相同输入不重复执行 |
| 3 | RAG top_k 控制在 3～5 | 控制检索结果数量 |
| 4 | mock-first 保证无外部服务也能演示 | 不依赖网络和外部 API |

### 3.3 可用性

| # | 可用性要求 | 说明 |
|---|-----------|------|
| 1 | 前端必须有 loading / error / empty / success 状态 | 每个状态都要有对应 UI |
| 2 | 错误信息必须用户可理解 | 不暴露技术细节 |
| 3 | Agent 每一步要有状态展示 | AgentTimeline 展示执行进度 |
| 4 | 回复草稿可以复制 | ReplyCard 提供复制按钮 |

### 3.4 成本

| # | 成本要求 | 说明 |
|---|---------|------|
| 1 | 默认不调用真实 LLM | mock-first，零外部成本 |
| 2 | 后续真实 LLM 通过环境变量开关启用 | `USE_REAL_LLM=false` |
| 3 | 真实调用失败必须 fallback | 降级到 mock 响应 |

---

## 4. 推荐项目目录结构

```
customerops-agent/
├── docs/                           # 项目文档（已有）
│   ├── PROJECT_CONTEXT.md
│   ├── PRD.md
│   ├── DESIGN.md
│   ├── TECHNICAL_SPEC.md           # 本文件
│   ├── DEV_RULES.md
│   ├── DEV_STATUS.md
│   ├── CHANGELOG.md
│   └── archive/                    # 历史文档归档
│
├── backend/                        # 后端项目
│   ├── app/
│   │   ├── main.py                 # FastAPI 入口，挂载路由
│   │   ├── api/                    # API 层：请求/响应处理
│   │   │   ├── health.py           # GET /health
│   │   │   ├── tickets.py          # POST /api/tickets/analyze, GET /api/tickets/{id}
│   │   │   ├── examples.py         # GET /api/examples
│   │   │   └── evals.py            # GET /api/evals/cases, POST /api/evals/run
│   │   ├── agents/                 # Agent 层：智能决策节点
│   │   │   ├── orchestrator.py     # Orchestrator：固定线性流程编排
│   │   │   ├── intent_agent.py     # IntentAgent：意图识别
│   │   │   ├── retrieval_agent.py  # RetrievalAgent：知识库检索
│   │   │   ├── tool_agent.py       # ToolAgent：工具调用
│   │   │   ├── policy_agent.py     # PolicyAgent：政策判断
│   │   │   ├── reply_agent.py      # ReplyAgent：回复生成
│   │   │   └── qa_agent.py         # QAAgent：质检
│   │   ├── schemas/                # Schema 层：数据结构定义
│   │   │   ├── request.py          # 请求 Schema
│   │   │   ├── response.py         # 响应 Schema
│   │   │   ├── agent_state.py      # Agent 状态 Schema
│   │   │   └── eval.py             # Eval 相关 Schema
│   │   ├── services/               # Service 层：业务编排
│   │   │   ├── ticket_service.py   # TicketService：工单分析编排
│   │   │   └── eval_service.py     # EvalService：评估执行
│   │   ├── rag/                    # RAG 层：知识库加载和检索
│   │   │   ├── loader.py           # Markdown 知识库加载器
│   │   │   ├── retriever.py        # 简单检索器（关键词 / BM25-like）
│   │   │   └── evidence_builder.py # Evidence 构建器
│   │   ├── tools/                  # Tools 层：mock 工具
│   │   │   ├── get_order.py        # 获取订单信息
│   │   │   ├── get_logistics.py    # 获取物流信息
│   │   │   ├── check_refund_window.py  # 检查退款窗口
│   │   │   └── create_ticket.py    # 创建工单
│   │   └── core/                   # Core 层：配置、错误、日志
│   │       ├── config.py           # 应用配置（环境变量读取）
│   │       ├── errors.py           # 统一错误定义
│   │       ├── logging.py          # 日志配置
│   │       └── llm_client.py       # LLM 客户端抽象接口 + mock 实现
│   ├── data/                       # 数据层
│   │   ├── knowledge_base/         # 本地 Markdown 知识库
│   │   │   ├── after_sales_policy.md
│   │   │   ├── refund_policy.md
│   │   │   ├── replacement_policy.md
│   │   │   ├── logistics_policy.md
│   │   │   ├── invoice_policy.md
│   │   │   └── earbuds_faq.md
│   │   ├── mock_orders.json        # Mock 订单数据
│   │   ├── mock_logistics.json     # Mock 物流数据
│   │   └── eval_cases.json         # 评估用例
│   ├── tests/                      # 测试层
│   │   ├── test_health.py
│   │   ├── test_intent.py
│   │   ├── test_retrieval.py
│   │   ├── test_tools.py
│   │   ├── test_policy.py
│   │   ├── test_reply.py
│   │   ├── test_qa.py
│   │   ├── test_orchestrator.py
│   │   └── test_eval.py
│   ├── requirements.txt            # Python 依赖
│   └── .env.example                # 环境变量示例
│
├── frontend/                       # 前端项目
│   ├── app/                        # Next.js App Router 页面
│   │   ├── layout.tsx              # 全局布局
│   │   ├── page.tsx                # / 工单分析工作台
│   │   ├── result/
│   │   │   └── [ticketId]/
│   │   │       └── page.tsx        # /result/:ticketId 分析结果详情
│   │   └── eval/
│   │       └── page.tsx            # /eval Eval / Bad Case 页面
│   ├── components/                 # UI 组件
│   │   ├── TicketInput.tsx
│   │   ├── ExampleTicketList.tsx
│   │   ├── AgentTimeline.tsx
│   │   ├── AgentStepCard.tsx
│   │   ├── EvidencePanel.tsx
│   │   ├── ToolResultPanel.tsx
│   │   ├── PolicyResultCard.tsx
│   │   ├── ReplyCard.tsx
│   │   ├── QAResultCard.tsx
│   │   ├── EvalTable.tsx
│   │   ├── StatusBadge.tsx
│   │   ├── RiskBadge.tsx
│   │   ├── LoadingState.tsx
│   │   ├── ErrorState.tsx
│   │   └── EmptyState.tsx
│   ├── lib/                        # 工具库
│   │   └── api.ts                  # 后端 API 调用封装
│   ├── types/                      # TypeScript 类型定义
│   │   └── ticket.ts               # 工单相关类型
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.ts
│
├── README.md                       # 项目说明和启动指南
├── .env.example                    # 环境变量示例（根目录）
└── .gitignore                      # Git 忽略规则
```

### 目录职责说明

| 目录 | 职责 |
|------|------|
| `backend/app/api/` | API 层：只处理请求和响应，调用 Service 层 |
| `backend/app/services/` | Service 层：负责业务编排，协调多个 Agent |
| `backend/app/agents/` | Agent 层：负责智能决策节点，每个 Agent 单一职责 |
| `backend/app/schemas/` | Schema 层：Pydantic 数据结构定义，数据校验 |
| `backend/app/rag/` | RAG 层：知识库加载、检索、Evidence 构建 |
| `backend/app/tools/` | Tools 层：mock 工具实现，封装外部 API 接口 |
| `backend/app/core/` | Core 层：配置管理、错误定义、日志、LLM 客户端抽象 |
| `backend/data/` | 数据层：mock 数据文件、知识库文档、eval 用例 |
| `backend/tests/` | 测试层：单元测试和集成测试 |
| `frontend/app/` | 前端页面层：Next.js App Router 页面 |
| `frontend/components/` | 前端组件层：可复用 UI 组件 |
| `frontend/lib/` | 前端工具库：API 调用封装 |
| `frontend/types/` | 前端类型定义：TypeScript 类型 |

---

## 5. 后端模块设计

### 5.1 API 层 (`backend/app/api/`)

| 模块 | 职责 |
|------|------|
| `health.py` | 健康检查接口，返回服务状态 |
| `tickets.py` | 工单分析接口：接收工单输入，返回完整分析结果；查询历史分析结果 |
| `examples.py` | 示例工单接口：返回预设的示例工单列表 |
| `evals.py` | 评估接口：返回 eval cases，运行评估 |

### 5.2 Service 层 (`backend/app/services/`)

| 模块 | 职责 |
|------|------|
| `TicketService` | 工单分析编排：接收请求 → 调用 Orchestrator → 保存结果 → 返回响应 |
| `EvalService` | 评估执行：加载 eval cases → 逐条执行 → 对比结果 → 统计通过率 |

### 5.3 Agent 层 (`backend/app/agents/`)

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| `Orchestrator` | 固定线性流程编排 6 个 Agent | TicketAnalysisRequest | AgentState（完整结果） |
| `IntentAgent` | 意图识别 + 实体提取 | message, order_id, product_type | IntentResult（intent, entities, confidence） |
| `RetrievalAgent` | 知识库检索 | intent, entities | Evidence[]（source, content, score） |
| `ToolAgent` | 工具调用 | intent, entities, order_id | ToolResults（order, logistics, errors） |
| `PolicyAgent` | 政策判断 | intent, evidence, tool_results | PolicyResult（eligible, suggestion, reason） |
| `ReplyAgent` | 回复生成 | intent, evidence, tool_results, policy_result | ReplyResult（reply） |
| `QAAgent` | 质检 | reply, intent, policy_result | QAResult（score, risks, suggestion, need_human_review） |

**Agent 通用规则**：

- 每个 Agent 输入输出必须结构化（Pydantic Schema）
- 某个节点失败时不崩溃，记录 error 并继续可控降级
- MVP 采用固定主流程，后续可升级 LangGraph 条件路由

**Agent 失败处理**：

| Agent | 失败时行为 |
|-------|-----------|
| IntentAgent | 默认 intent="other", confidence=0.0, 继续流程 |
| RetrievalAgent | evidence=[], 继续流程，PolicyAgent 会标记信息不足 |
| ToolAgent | 对应工具结果为 error，继续流程，PolicyAgent 会标记数据不完整 |
| PolicyAgent | eligible=false, suggestion="建议人工处理", 继续流程 |
| ReplyAgent | 生成通用兜底回复，继续流程 |
| QAAgent | need_human_review=true, 继续流程 |

**Agent 实现方式（MVP）**：

| Agent | 实现方式 |
|-------|---------|
| IntentAgent | rule-based：关键词匹配 + 正则表达式 |
| RetrievalAgent | rule-based：关键词匹配 + BM25-like scoring |
| ToolAgent | mock：查询 mock JSON 数据 |
| PolicyAgent | rule-based：条件判断（时间窗口 + 状态匹配） |
| ReplyAgent | rule-based：模板 + 上下文填充 |
| QAAgent | rule-based：规则检查（必要字段、超长、禁用词） |

### 5.4 RAG 层 (`backend/app/rag/`)

| 模块 | 职责 |
|------|------|
| `loader.py` | Markdown 知识库加载器：读取 `data/knowledge_base/` 下的 .md 文件 |
| `retriever.py` | 简单检索器：基于关键词匹配 + BM25-like scoring，返回 top_k 结果 |
| `evidence_builder.py` | Evidence 构建器：将检索结果格式化为 Evidence Schema |

### 5.5 Tools 层 (`backend/app/tools/`)

| 工具 | 职责 | 输入 | 输出 |
|------|------|------|------|
| `get_order` | 获取订单信息 | order_id | OrderInfo（status, amount, created_at, shipped_at）或 error |
| `get_logistics` | 获取物流信息 | order_id | LogisticsInfo（status, carrier, tracking_no, last_update）或 error |
| `check_refund_window` | 检查退款窗口 | order_id | eligible: bool, reason: string |
| `create_ticket` | 创建工单 | intent, message | ticket_id |

**Tools 通用规则**：

- 所有工具为 mock 实现，查询本地 JSON 数据
- 不执行真实退款、真实支付、真实客服发送
- 工具调用走白名单，不允许任意调用

### 5.6 Core 层 (`backend/app/core/`)

| 模块 | 职责 |
|------|------|
| `config.py` | 应用配置：从环境变量读取配置（USE_REAL_LLM, LOG_LEVEL 等） |
| `errors.py` | 统一错误定义：自定义异常类，错误码 |
| `logging.py` | 日志配置：结构化日志，不输出敏感信息 |
| `llm_client.py` | LLM 客户端抽象接口 + mock 实现，后续替换为真实 LLM |

---

## 6. 前端模块设计

### 6.1 Pages（页面）

| 页面 | 路由 | 说明 |
|------|------|------|
| 工单分析工作台 | `/` | 首页：输入工单 + 选择示例 + 启动分析 |
| 分析结果详情 | `/result/[ticketId]` | 展示完整 Agent 处理结果：Timeline + Evidence + Tools + Policy + Reply + QA |
| Eval / Bad Case | `/eval` | 展示评估用例 + 运行评估 + 结果对比 |

### 6.2 Components（组件）

| 组件 | 说明 |
|------|------|
| `TicketInput` | 工单输入表单：textarea（必填）+ order_id + product_type + 提交按钮 |
| `ExampleTicketList` | 示例工单标签列表，点击自动填充表单 |
| `AgentTimeline` | 垂直时间线，6 个节点展示 Agent 执行状态（pending / running / completed / failed） |
| `AgentStepCard` | 可展开的详情卡片，展示单个 Agent 的输入输出和耗时 |
| `EvidencePanel` | 政策引用列表，白色卡片 + 左侧蓝色色条标记来源 |
| `ToolResultPanel` | 工具结果分组面板（Order / Logistics），键值对展示 |
| `PolicyResultCard` | 政策判断结果卡片，状态色左侧色条（绿 = eligible / 红 = not eligible / 黄 = 需关注） |
| `ReplyCard` | 客服回复文本 + 复制按钮，绿色色条（auto_reply）/ 黄色色条（need_human_review） |
| `QAResultCard` | 质量评分 + 风险列表 + 改进建议 |
| `EvalTable` | 评估结果表格，Pass 绿色标签，Fail 红色标签 |
| `StatusBadge` | 圆角胶囊形状态标签（pending 灰 / running 蓝脉冲 / completed 绿 / failed 红） |
| `RiskBadge` | 红色风险标签（"高风险" / "需要人工审核" / "证据不足"） |
| `LoadingState` | 加载占位，Timeline 节点逐个完成，当前执行节点蓝色脉冲动画 |
| `ErrorState` | 错误占位，红色图标 + 错误描述 + 重试按钮 |
| `EmptyState` | 空内容占位，灰色图标 + 提示文字 |

### 6.3 lib / types

| 文件 | 说明 |
|------|------|
| `frontend/lib/api.ts` | 后端 API 调用封装：fetch wrapper，错误处理，类型推断 |
| `frontend/types/ticket.ts` | TypeScript 类型定义：与后端 Pydantic Schema 对齐 |

### 6.4 设计约束

- 前端**不是**聊天机器人页面，是 ToB 工单处理工作台
- 必须展示 Agent 流程、evidence、tool results、QA
- UI 风格遵守 `docs/DESIGN.md`（企业蓝、白色卡片、4px 网格、状态色）

---

## 7. Agent 工作流技术设计

### 7.1 MVP 主流程

```
用户输入工单
  → Intent Agent（意图识别 + 实体提取）
  → Retrieval Agent（知识库检索 → evidence）
  → Tool Agent（工具调用 → order / logistics）
  → Policy Agent（政策判断 → eligible + suggestion）
  → Reply Agent（回复生成 → reply）
  → QA Agent（质检 → score + risks + need_human_review）
  → Final Result
```

### 7.2 工作流特性

| 特性 | 说明 |
|------|------|
| 编排方式 | 固定线性流程，不做条件分支和动态路由 |
| 结构化约束 | 每个 Agent 输入输出必须使用 Pydantic Schema |
| 失败降级 | 某个节点失败时不崩溃，记录 error 并继续 |
| 可追溯 | AgentState 记录每个 Agent 的输入输出和状态 |
| 可扩展 | 后续可升级为 LangGraph 条件路由 |

### 7.3 每个 Agent 详细设计

#### IntentAgent

| 项目 | 内容 |
|------|------|
| 输入 | `message: str`, `order_id: str | None`, `product_type: str | None` |
| 输出 | `IntentResult(intent: str, entities: dict, confidence: float)` |
| 实现 | rule-based：关键词匹配 + 正则表达式 |
| 失败处理 | 默认 intent="other", confidence=0.0 |
| mock | ✅ 纯 rule-based，无需 mock |

#### RetrievalAgent

| 项目 | 内容 |
|------|------|
| 输入 | `intent: str`, `entities: dict` |
| 输出 | `Evidence[](source: str, content: str, score: float)` |
| 实现 | rule-based：关键词匹配 + BM25-like scoring |
| 失败处理 | evidence=[]，继续流程 |
| mock | ✅ 纯 rule-based，无需 mock |

#### ToolAgent

| 项目 | 内容 |
|------|------|
| 输入 | `intent: str`, `entities: dict`, `order_id: str | None` |
| 输出 | `ToolResults(order: OrderInfo | None, logistics: LogisticsInfo | None, errors: list)` |
| 实现 | mock：查询 `data/mock_orders.json` 和 `data/mock_logistics.json` |
| 失败处理 | 对应工具结果为 error，继续流程 |
| mock | ✅ 天然 mock |

#### PolicyAgent

| 项目 | 内容 |
|------|------|
| 输入 | `intent: str`, `evidence: Evidence[]`, `tool_results: ToolResults` |
| 输出 | `PolicyResult(eligible: bool, suggestion: str, reason: str)` |
| 实现 | rule-based：条件判断（时间窗口 + 状态匹配） |
| 失败处理 | eligible=false, suggestion="建议人工处理" |
| mock | ✅ 纯 rule-based，无需 mock |

#### ReplyAgent

| 项目 | 内容 |
|------|------|
| 输入 | `intent: str`, `evidence: Evidence[]`, `tool_results: ToolResults`, `policy_result: PolicyResult` |
| 输出 | `ReplyResult(reply: str)` |
| 实现 | rule-based：模板 + 上下文填充 |
| 失败处理 | 生成通用兜底回复 |
| mock | ✅ 纯 rule-based，无需 mock |

#### QAAgent

| 项目 | 内容 |
|------|------|
| 输入 | `reply: str`, `intent: str`, `policy_result: PolicyResult` |
| 输出 | `QAResult(score: float, risks: list, suggestion: str, need_human_review: bool)` |
| 实现 | rule-based：规则检查（必要字段、超长、禁用词） |
| 失败处理 | need_human_review=true |
| mock | ✅ 纯 rule-based，无需 mock |

---

## 8. API 契约

### 8.1 GET /health

**方法**：GET
**路径**：`/health`

**响应**：

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | "ok" |
| version | string | 服务版本 |

**失败情况**：服务不可用时返回 503

**验收标准**：
- 返回 200 + `{"status": "ok"}`
- 响应时间 < 100ms

---

### 8.2 GET /api/examples

**方法**：GET
**路径**：`/api/examples`

**响应**：

| 字段 | 类型 | 说明 |
|------|------|------|
| examples | array | 示例工单列表 |
| examples[].id | string | 示例 ID |
| examples[].title | string | 示例标题 |
| examples[].message | string | 示例工单内容 |
| examples[].order_id | string | 示例订单号（可选） |
| examples[].product_type | string | 产品类型（可选） |

**失败情况**：无

**验收标准**：
- 返回 5-6 条示例工单
- 覆盖主要场景（产品故障、退款、物流、发票、投诉）

---

### 8.3 POST /api/tickets/analyze

**方法**：POST
**路径**：`/api/tickets/analyze`

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 是 | 用户售后问题文本，最大 2000 字符 |
| order_id | string | 否 | 订单号，如 ORD-2024-001 |
| product_type | string | 否 | 产品类型，如 earbuds、headphones |

**响应体**：

| 字段 | 类型 | 说明 |
|------|------|------|
| ticket_id | string | 工单唯一标识 |
| intent_result | IntentResult | 意图识别结果 |
| evidence | Evidence[] | 检索到的政策文档片段 |
| tool_results | ToolResults | 工具调用结果 |
| policy_result | PolicyResult | 政策判断结果 |
| reply_result | ReplyResult | 回复生成结果 |
| qa_result | QAResult | 质检结果 |
| need_human_review | boolean | 是否需要人工审核 |
| final_result | string | "auto_reply" 或 "need_human_review" |

**失败情况**：

| 场景 | 状态码 | 说明 |
|------|--------|------|
| message 为空 | 422 | 请求校验失败 |
| message 超长 | 422 | 请求校验失败 |
| 内部错误 | 500 | 服务端异常 |

**验收标准**：
- 正常输入返回完整分析结果
- 所有 Agent 结果都有值（即使是降级结果）
- need_human_review 正确标记
- 响应时间可接受（< 5s）

---

### 8.4 GET /api/tickets/{ticket_id}

**方法**：GET
**路径**：`/api/tickets/{ticket_id}`

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| ticket_id | string | 工单 ID |

**响应体**：与 POST /api/tickets/analyze 响应相同

**失败情况**：

| 场景 | 状态码 | 说明 |
|------|--------|------|
| ticket_id 不存在 | 404 | 工单未找到 |

**持久化说明**：MVP 使用内存 / JSON 文件轻量保存分析结果，服务重启后数据丢失。

**验收标准**：
- 已分析的工单可通过 ticket_id 查询
- 不存在的 ticket_id 返回 404

---

### 8.5 GET /api/evals/cases

**方法**：GET
**路径**：`/api/evals/cases`

**响应体**：

| 字段 | 类型 | 说明 |
|------|------|------|
| cases | array | 评估用例列表 |
| cases[].id | string | 用例 ID |
| cases[].input | object | 输入（message, order_id, product_type） |
| cases[].expected | object | 期望输出（intent, need_human_review 等关键字段） |

**失败情况**：无

**验收标准**：
- 返回 10 条 eval cases
- 覆盖核心场景

---

### 8.6 POST /api/evals/run

**方法**：POST
**路径**：`/api/evals/run`

**请求体**：无（运行全部 eval cases）

**响应体**：

| 字段 | 类型 | 说明 |
|------|------|------|
| total | number | 总用例数 |
| passed | number | 通过数 |
| failed | number | 失败数 |
| results | array | 每条用例的结果 |
| results[].case_id | string | 用例 ID |
| results[].passed | boolean | 是否通过 |
| results[].expected | object | 期望输出 |
| results[].actual | object | 实际输出 |
| results[].diff | string | 差异说明（失败时） |

**失败情况**：

| 场景 | 状态码 | 说明 |
|------|--------|------|
| 内部错误 | 500 | 服务端异常 |

**验收标准**：
- 运行 10 条 eval cases
- 返回每条的 pass/fail 和差异
- 返回总体通过率

---

## 9. Pydantic Schema 设计

以下是核心 Schema 的字段定义。Goal 模式实现时必须优先实现这些 Schema，不要频繁改字段名。

### 9.1 TicketAnalysisRequest

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | str | 是 | 用户售后问题文本，max_length=2000 |
| order_id | str \| None | 否 | 订单号 |
| product_type | str \| None | 否 | 产品类型 |

### 9.2 TicketAnalysisResponse

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ticket_id | str | 是 | 工单唯一标识 |
| intent_result | IntentResult | 是 | 意图识别结果 |
| evidence | list[Evidence] | 是 | 检索到的政策文档片段 |
| tool_results | ToolResults | 是 | 工具调用结果 |
| policy_result | PolicyResult | 是 | 政策判断结果 |
| reply_result | ReplyResult | 是 | 回复生成结果 |
| qa_result | QAResult | 是 | 质检结果 |
| need_human_review | bool | 是 | 是否需要人工审核 |
| final_result | str | 是 | "auto_reply" 或 "need_human_review" |

### 9.3 AgentState

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ticket_id | str | 是 | 工单 ID |
| request | TicketAnalysisRequest | 是 | 原始请求 |
| intent_result | IntentResult \| None | 否 | 意图识别结果（流程中逐步填充） |
| evidence | list[Evidence] | 否 | 检索结果（默认空列表） |
| tool_results | ToolResults \| None | 否 | 工具调用结果 |
| policy_result | PolicyResult \| None | 否 | 政策判断结果 |
| reply_result | ReplyResult \| None | 否 | 回复生成结果 |
| qa_result | QAResult \| None | 否 | 质检结果 |
| errors | list[str] | 否 | 流程中的错误记录（默认空列表） |

### 9.4 IntentResult

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| intent | str | 是 | 意图类型（refund_request, exchange_request, logistics_query, invoice_request, complaint, product_defect, other） |
| entities | dict | 是 | 提取的实体（order_id, product_type 等） |
| confidence | float | 是 | 置信度 0.0-1.0 |

### 9.5 Evidence

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | str | 是 | 来源文件名（如 refund_policy.md） |
| content | str | 是 | 匹配的内容片段 |
| score | float | 是 | 相关性评分 0.0-1.0 |

### 9.6 ToolResults

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order | OrderInfo \| None | 否 | 订单信息 |
| logistics | LogisticsInfo \| None | 否 | 物流信息 |
| errors | list[str] | 否 | 工具调用错误列表 |

### 9.7 OrderInfo

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order_id | str | 是 | 订单号 |
| status | str | 是 | 订单状态（pending, shipped, delivered, returned） |
| amount | float | 是 | 订单金额 |
| created_at | str | 是 | 下单时间 |
| shipped_at | str \| None | 否 | 发货时间 |
| product_type | str | 是 | 产品类型 |

### 9.8 LogisticsInfo

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order_id | str | 是 | 订单号 |
| status | str | 是 | 物流状态（in_transit, delivered, exception, unknown） |
| carrier | str | 是 | 物流承运商 |
| tracking_no | str | 是 | 物流单号 |
| last_update | str | 是 | 最后更新时间 |
| last_location | str | 是 | 最后位置 |

### 9.9 PolicyResult

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| eligible | bool | 是 | 是否符合条件 |
| suggestion | str | 是 | 处理建议 |
| reason | str | 是 | 判断理由 |

### 9.10 ReplyResult

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reply | str | 是 | 客服回复文本 |

### 9.11 QAResult

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| score | float | 是 | 质量评分 0.0-1.0 |
| risks | list[str] | 是 | 风险列表 |
| suggestion | str | 是 | 改进建议 |
| need_human_review | bool | 是 | 是否需要人工审核 |

### 9.12 EvalCase

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | str | 是 | 用例 ID |
| input | TicketAnalysisRequest | 是 | 输入 |
| expected_intent | str | 是 | 期望意图 |
| expected_need_human_review | bool | 是 | 期望是否需要人工审核 |
| description | str | 是 | 用例描述 |

### 9.13 EvalResult

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| case_id | str | 是 | 用例 ID |
| passed | bool | 是 | 是否通过 |
| expected | dict | 是 | 期望输出关键字段 |
| actual | dict | 是 | 实际输出关键字段 |
| diff | str \| None | 否 | 差异说明 |

### 9.14 ErrorResponse

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| error | str | 是 | 错误类型 |
| message | str | 是 | 错误描述 |
| detail | str \| None | 否 | 错误详情（开发模式） |

---

## 10. Mock 数据设计

### 10.1 mock_orders.json

至少包含以下 4 条订单：

| 订单号 | 状态 | 说明 | 场景 |
|--------|------|------|------|
| ORD-2024-001 | delivered | 正常已签收订单，30 天内 | 退款 / 换货正常流程 |
| ORD-2024-002 | shipped | 未签收订单，运输中 | 物流查询 |
| ORD-2024-003 | delivered | 已签收但超出 30 天售后期 | 退款窗口超期 |
| ORD-9999-999 | — | 不存在的订单 | 订单不存在异常 |

### 10.2 mock_logistics.json

至少包含以下 4 条物流信息：

| 订单号 | 物流状态 | 说明 | 场景 |
|--------|---------|------|------|
| ORD-2024-001 | delivered | 已签收 | 正常签收 |
| ORD-2024-002 | in_transit | 运输中 | 物流查询 |
| ORD-2024-005 | exception | 异常物流（滞留） | 物流异常 |
| ORD-2024-006 | — | 无物流信息 | 物流查询失败 |

### 10.3 eval_cases.json

至少 10 条 eval case，覆盖以下场景：

| # | 场景 | 期望意图 | 期望 need_human_review |
|---|------|---------|----------------------|
| 1 | 产品故障售后 | product_defect | false |
| 2 | 退款咨询 | refund_request | false |
| 3 | 换货咨询 | exchange_request | false |
| 4 | 物流查询 | logistics_query | false |
| 5 | 发票问题 | invoice_request | false |
| 6 | 投诉高风险 | complaint | true |
| 7 | 缺订单号 | other / refund_request | true |
| 8 | 不存在订单 | refund_request | true |
| 9 | RAG 无结果 | other | true |
| 10 | QA 不通过 | complaint | true |

---

## 11. Knowledge Base 设计

MVP 使用本地 Markdown 文件作为知识库，存放在 `backend/data/knowledge_base/` 目录下。

### 11.1 after_sales_policy.md

| 项目 | 内容 |
|------|------|
| 用途 | 总体售后政策，定义售后处理的基本原则和流程 |
| 应包含内容 | 售后受理条件、处理流程、时效要求、客户沟通规范 |
| 可检索关键词 | 售后、退换货、维修、保修、售后流程、处理时效 |
| 对应场景 | 通用售后咨询、产品故障 |

### 11.2 refund_policy.md

| 项目 | 内容 |
|------|------|
| 用途 | 退款政策，定义退款条件、时间窗口、流程 |
| 应包含内容 | 退款条件（签收后 30 天内）、退款流程、退款方式、不予退款情形 |
| 可检索关键词 | 退款、退钱、refund、30 天、退款条件、退款流程 |
| 对应场景 | 退款咨询、退款窗口判断 |

### 11.3 replacement_policy.md

| 项目 | 内容 |
|------|------|
| 用途 | 换货政策，定义换货条件、时间窗口、流程 |
| 应包含内容 | 换货条件（签收后 15 天内、产品质量问题）、换货流程、不予换货情形 |
| 可检索关键词 | 换货、换新、replacement、15 天、质量问题、换货条件 |
| 对应场景 | 换货咨询、质量问题处理 |

### 11.4 logistics_policy.md

| 项目 | 内容 |
|------|------|
| 用途 | 物流政策，定义物流查询、延迟处理、丢件处理 |
| 应包含内容 | 物流查询方式、物流延迟处理（超过 7 天未更新可申请退款）、丢件赔偿 |
| 可检索关键词 | 物流、快递、发货、shipping、物流延迟、丢件、7 天 |
| 对应场景 | 物流查询、物流延迟投诉 |

### 11.5 invoice_policy.md

| 项目 | 内容 |
|------|------|
| 用途 | 发票政策，定义开票条件、流程、时间 |
| 应包含内容 | 开票条件、开票方式（电子发票 / 纸质发票）、开票时效、补开流程 |
| 可检索关键词 | 发票、开票、invoice、电子发票、纸质发票、补开 |
| 对应场景 | 发票问题 |

### 11.6 earbuds_faq.md

| 项目 | 内容 |
|------|------|
| 用途 | 耳机产品常见问题解答 |
| 应包含内容 | 耳机常见故障（无法连接、单侧无声、充电问题）、保修政策、维修流程 |
| 可检索关键词 | 耳机、earbuds、蓝牙、连接、无声、充电、保修、维修 |
| 对应场景 | 耳机产品故障咨询 |

---

## 12. 测试计划

### 12.1 测试分类

| # | 测试类型 | 覆盖范围 | 验收标准 |
|---|---------|---------|---------|
| 1 | Health API 测试 | GET /health | 返回 200 + status="ok" |
| 2 | Intent 分类测试 | IntentAgent | 各意图类型正确识别，置信度合理，未知意图返回 "other" |
| 3 | RAG 检索测试 | RetrievalAgent | 相关文档被检索到，top_k ≤ 5，无关查询返回空 |
| 4 | Mock Tools 测试 | ToolAgent | 正常订单返回数据，不存在订单返回 error，缺 order_id 返回 need_more_info |
| 5 | Policy 判断测试 | PolicyAgent | 符合条件返回 eligible=true，超期返回 eligible=false，信息不足返回建议人工 |
| 6 | Reply 生成测试 | ReplyAgent | 回复包含政策引用，回复不为空，高风险回复不承诺赔偿 |
| 7 | QA 检查测试 | QAAgent | 正常回复 score > 0.8，高风险标记 need_human_review=true |
| 8 | Orchestrator 完整路径测试 | Orchestrator | happy path 完整执行，所有 Agent 结果都有值 |
| 9 | 缺 order_id 路径测试 | ToolAgent + PolicyAgent | ToolAgent 返回 need_more_info，PolicyAgent 标记信息不足 |
| 10 | 高风险投诉路径测试 | 全流程 | complaint 意图 → need_human_review=true |
| 11 | Eval 运行测试 | EvalService | 10 条 case 全部可执行，返回 pass/fail 统计 |

### 12.2 测试原则

- 测试独立，不依赖外部服务
- 测试可重复执行
- 覆盖正常和异常情况
- 每个 Agent 独立可测

---

## 13. 项目初始化要求

后续 Module 5 / Module 6 初始化项目时必须做到：

| # | 要求 | 说明 |
|---|------|------|
| 1 | 创建 backend / frontend 基础结构 | 按本目录结构创建空目录和占位文件 |
| 2 | 后端 health API 可运行 | `GET /health` 返回 200 |
| 3 | 前端首页占位可运行 | `/` 页面可以打开，显示占位内容 |
| 4 | .env.example 存在 | 说明需要的环境变量 |
| 5 | .gitignore 正确 | 忽略 .env, node_modules, venv, .next, __pycache__, 缓存文件 |
| 6 | README 有启动说明 | 前后端分别如何启动 |
| 7 | pytest 至少有 health check | `test_health.py` 通过 |
| 8 | 不实现完整业务逻辑 | 初始化只搭骨架，不做 Agent / RAG / Tools |
| 9 | 不接真实 LLM | mock-first |
| 10 | 不提交密钥 | .env 不在 Git 中 |
| 11 | 初始化后必须 Git commit | commit message: "feat: init project structure" |

### Python Environment（Conda）

后端 Python 环境**必须使用 Conda 虚拟环境**管理。

| 规则 | 说明 |
|------|------|
| 环境管理工具 | Conda（已安装） |
| 推荐环境名 | `customerops-agent` |
| 推荐 Python 版本 | 3.11 |
| 禁止使用全局 Python | 不允许直接使用系统全局 Python 安装项目依赖 |
| 禁止默认使用 venv | 不使用 Python 内置 venv，统一使用 Conda |
| 依赖管理 | requirements.txt（pip），后续可增加 environment.yml |
| README 必须说明 | Conda 环境创建和启动步骤 |

**后续初始化时应创建 Conda 环境**：

```bash
conda create -n customerops-agent python=3.11
conda activate customerops-agent
```

**后端依赖安装和常用命令**（均需在 Conda 环境激活后执行）：

```bash
conda activate customerops-agent
cd backend
pip install -r requirements.txt
pytest
ruff check .
uvicorn app.main:app --reload
```

> **注意**：以上命令仅为后续初始化时的参考示例，当前不执行。不创建 requirements.txt，不安装依赖，不创建 Conda 环境。

---

## 14. Goal 模式技术指令摘要

以下内容供后续 Goal 模式读取：

```
只实现 PRD.md 的 Current MVP Scope。
遵守 DESIGN.md 的 ToB 工作台风格。
遵守 TECHNICAL_SPEC.md 的 API 契约、Schema 定义、目录结构。
mock-first，不接真实 LLM。
不接真实业务系统（订单、物流、退款）。
不实现 Future Scope（LangGraph、向量库、Docker、云部署）。
不突破安全边界（不暴露密钥、不无 evidence 承诺、高风险必须人工复核）。
每个核心模块需要测试（Agent、API、RAG、Tools）。
完成后更新 DEV_STATUS.md 和 CHANGELOG.md。
```

---

## 15. Initialization Readiness Checklist

本章节用于 Module 6 项目初始化前检查。所有项目必须满足以下条件后才能开始初始化。

### 15.1 文档准备

| # | 文档 | 状态 | 说明 |
|---|------|------|------|
| 1 | `docs/PROJECT_CONTEXT.md` | ✅ 已完成 | 项目背景和定位 |
| 2 | `docs/PRD.md` | ✅ 已完成 | 产品需求文档 |
| 3 | `docs/DESIGN.md` | ✅ 已完成 | 设计文档 |
| 4 | `docs/TECHNICAL_SPEC.md` | ✅ 已完成 | 技术规格文档 |
| 5 | `docs/DEV_RULES.md` | ✅ 已完成 | 开发规则 |
| 6 | `docs/DEV_STATUS.md` | ✅ 已完成 | 开发状态 |

### 15.2 范围准备

| # | 范围 | 状态 | 说明 |
|---|------|------|------|
| 1 | Current MVP Scope 明确 | ✅ | PRD.md 第 3 节，20 项 |
| 2 | Future Possible Scope 不进入当前 MVP | ✅ | PRD.md 第 4 节，15 项 |
| 3 | Permanent Safety Boundaries 明确 | ✅ | PRD.md 第 5 节，11 项 |
| 4 | Explicit Non-goals 明确 | ✅ | PRD.md 第 6 节，7 项 |

### 15.3 技术准备

| # | 技术 | 状态 | 说明 |
|---|------|------|------|
| 1 | 后端使用 FastAPI + Pydantic v2 | ✅ | 技术栈已锁定 |
| 2 | 前端使用 Next.js + React + TypeScript + Tailwind | ✅ | 技术栈已锁定 |
| 3 | 后端 Python 使用 Conda 环境 `customerops-agent` | ✅ | 环境规则已确认 |
| 4 | MVP mock-first | ✅ | 不调用真实 LLM |
| 5 | 不接真实 LLM | ✅ | mock 响应 |
| 6 | 不接真实业务系统 | ✅ | mock tools |

### 15.4 初始化必须创建

Module 6 初始化时**必须创建**以下内容：

| # | 内容 | 说明 |
|---|------|------|
| 1 | `backend/` 基础目录 | 按 TECHNICAL_SPEC.md 目录结构创建 |
| 2 | `frontend/` 基础目录 | 按 TECHNICAL_SPEC.md 目录结构创建 |
| 3 | `README.md` | 项目说明和启动指南 |
| 4 | `.env.example` | 环境变量示例，无真实密钥 |
| 5 | `.gitignore` | Git 忽略规则 |
| 6 | `backend/requirements.txt` | Python 依赖 |
| 7 | Health API | `GET /health` 返回 200 |
| 8 | 前端首页占位 | `/` 页面可以打开 |
| 9 | 基础测试 | `test_health.py` 通过 |

### 15.5 初始化禁止

Module 6 初始化时**禁止**以下行为：

| # | 禁止 | 说明 |
|---|------|------|
| 1 | 不实现完整业务逻辑 | 初始化只搭骨架 |
| 2 | 不实现完整 Agent | Agent 在 Goal 模式实现 |
| 3 | 不接真实 LLM | mock-first |
| 4 | 不接真实电商平台 | mock tools |
| 5 | 不写真实 API Key | `.env.example` 无真实密钥 |
| 6 | 不把 Future Scope 提前塞进初始化 | 保持初始化轻量 |
| 7 | 不跳过测试 | 至少有 health test |
| 8 | 不跳过 Git commit | 初始化完成后必须 commit |

### 15.6 初始化验收

Module 6 完成后**必须满足**以下条件：

| # | 验收项 | 说明 |
|---|--------|------|
| 1 | Git working tree 初始前干净 | 初始化前无未提交更改 |
| 2 | Conda 环境创建或初始化命令明确 | README 有说明 |
| 3 | 后端 health API 可运行 | `GET /health` 返回 200 |
| 4 | 前端首页可运行 | `/` 页面可以打开 |
| 5 | pytest 至少有 health test | `test_health.py` 通过 |
| 6 | README 有启动说明 | 前后端分别如何启动 |
| 7 | `.gitignore` 正确 | 忽略 .env, node_modules, venv 等 |
| 8 | `.env.example` 存在且无真实密钥 | 环境变量示例 |
| 9 | Git commit 完成 | `chore: initialize project structure` |
