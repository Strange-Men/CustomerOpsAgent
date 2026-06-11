# CustomerOps Agent｜项目范围锁定

**版本**：v1.0
**日期**：2026-06-11
**用途**：Goal 模式开发时必须读取并遵守

---

## 1. 当前版本唯一目标

验证售后客服工单是否能通过多 Agent 流程完成结构化处理。

**不做**：替代真实客服系统、验证商业可行性、构建可部署的 SaaS 产品。

---

## 2. In Scope（必须做）

| # | 功能 | 说明 |
|---|------|------|
| 1 | 工单输入 | 前端页面输入 message、order_id、product_type |
| 2 | Intent Agent | 意图识别 + 实体提取 + 置信度 |
| 3 | Retrieval Agent | 本地 Markdown 知识库检索，输出 evidence |
| 4 | Tool Agent | 4 个 mock 工具：get_order、get_logistics、check_refund_window、create_ticket |
| 5 | Policy Agent | 简单条件判断，输出 eligible + suggestion + reason |
| 6 | Reply Agent | 基于上下文生成客服回复 |
| 7 | QA Agent | 规则检查，输出 score + risks + need_human_review |
| 8 | Orchestrator | 固定线性流程编排 6 个 Agent |
| 9 | Analyze API | POST /api/analyze |
| 10 | Eval API | POST /api/eval |
| 11 | Health API | GET /api/health |
| 12 | 前端展示 | 工单输入 + Agent Timeline + 结果展示 + Eval 页面 |
| 13 | 示例工单 | 10 条覆盖常见场景 |
| 14 | 知识库 | 6 篇 Markdown 政策文档 |
| 15 | 基础测试 | 核心模块单元测试 |

---

## 3. Out of Scope（禁止做）

| # | 功能 | 禁止原因 |
|---|------|---------|
| 1 | 用户登录 / 注册 | MVP 单用户模式 |
| 2 | 权限系统 | 不需要 |
| 3 | 多租户 | 只服务一个场景 |
| 4 | 真实支付 | 资金安全 |
| 5 | 真实退款 | 资金安全，只生成建议 |
| 6 | 真实电商平台 API | 不接外部系统 |
| 7 | 真实客服消息发送 | 只生成建议 |
| 8 | 复杂知识库管理后台 | 读本地文件 |
| 9 | 大规模向量数据库 | 用本地检索 |
| 10 | 异步任务队列 | 用同步处理 |
| 11 | 多语言客服 | 只做中文 |
| 12 | 复杂长期记忆 | 不需要跨会话 |
| 13 | 移动端适配 | 只做桌面端 |
| 14 | 生产级部署 | 本地运行 |
| 15 | 数据库（SQLite、PostgreSQL 等） | 用 JSON / mock 数据 |
| 16 | ORM（SQLAlchemy 等） | 不需要数据库 |
| 17 | Docker | 不需要容器化 |
| 18 | CI/CD | 不需要自动化部署 |
| 19 | 复杂日志系统 | 用 print / 简单 logging |
| 20 | 监控 / 告警 | 不需要 |

---

## 4. Allowed Simplifications（允许的简化）

| # | 简化方式 | 说明 |
|---|---------|------|
| 1 | mock-first | 所有工具使用 mock 实现，返回预设数据 |
| 2 | rule-based fallback | Policy Agent 和 QA Agent 使用规则判断，不依赖 LLM |
| 3 | 本地 Markdown 检索 | 知识库使用本地 Markdown 文件，关键词匹配检索 |
| 4 | JSON mock data | 订单、物流数据使用 JSON 文件，不引入数据库 |
| 5 | 简单前端展示 | 前端使用最简单的组件实现，不做复杂交互 |
| 6 | 固定 eval cases | 评估使用固定的 10 条测试用例，不做自动评估框架 |
| 7 | 真实 LLM 可后续再接 | MVP 默认使用 mock 响应，可选接入真实 LLM |
| 8 | 同步处理 | 所有请求同步处理，不做异步队列 |
| 9 | 单文件配置 | 配置使用 .env 文件，不做复杂配置管理 |

---

## 5. Hard Boundaries（硬边界）

以下边界**绝对不可突破**：

| # | 硬边界 | 说明 |
|---|--------|------|
| 1 | **不真实退款** | 系统只生成退款建议，不执行任何退款操作 |
| 2 | **不真实支付** | 系统不涉及任何资金操作 |
| 3 | **不发送真实客服消息** | 系统只生成回复建议，不发送到任何渠道 |
| 4 | **不接真实电商平台** | 不对接 Shopify / Amazon / 淘宝等任何平台 |
| 5 | **不提交 API Key** | 代码中不得出现任何真实 API Key |
| 6 | **不把业务逻辑堆在单文件** | 每个模块独立文件，遵循分层架构 |
| 7 | **不破坏后续 API / Schema 契约** | API 输入输出格式一旦确定，不可随意修改 |

---

## 6. Goal 模式开发必须遵守

### 清单（Goal 模式启动时必须读取并遵守）

- [ ] **读取本文档**：开始开发前必须读取 PROJECT_SCOPE.md
- [ ] **读取 DEV_RULES.md**：遵守开发规则和禁止事项
- [ ] **不添加用户系统**：不实现登录、注册、权限、JWT、session
- [ ] **不引入数据库**：不使用 SQLite、PostgreSQL、MongoDB、SQLAlchemy
- [ ] **不引入向量数据库**：不使用 Chroma、FAISS、Pinecone
- [ ] **不引入消息队列**：不使用 Celery、RabbitMQ、Redis
- [ ] **不引入 Docker**：不做容器化
- [ ] **不接真实 LLM**：默认 mock 响应，除非用户明确要求
- [ ] **不接真实外部 API**：不对接任何电商平台、支付网关、物流服务
- [ ] **不发送真实消息**：不发送邮件、短信、客服消息
- [ ] **不做复杂前端**：用最简单的组件，不做复杂交互、动画、状态管理
- [ ] **保持 Agent 轻量**：每个 Agent 内部逻辑不超过 100 行
- [ ] **保持 Orchestrator 简单**：固定线性流程，不做条件分支和动态路由
- [ ] **保持 RAG 简单**：关键词匹配 + 本地文件读取，不做向量检索
- [ ] **保持 Policy 简单**：简单条件判断，不做规则引擎
- [ ] **保持 QA 简单**：规则检查，不做 NLP 质检
- [ ] **写测试**：核心 Agent 和 API 必须有单元测试
- [ ] **不硬编码密钥**：API Key 只放 .env，.env 不提交 Git
- [ ] **不破坏 API 契约**：API 输入输出格式一旦确定，不可随意修改
- [ ] **不破坏分层架构**：API → Service → Agent → RAG / Tools → Schema
- [ ] **不扩大 MVP 范围**：只做 In Scope 中列出的功能

### 违反后果

如果 Goal 模式开发过程中违反以上任何一条，应立即停止并回退到符合范围的状态。
