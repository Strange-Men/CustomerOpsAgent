# CustomerOps Agent｜想法判断结论

## 1. 最终判断

**可以做，但需要收窄范围。**

CustomerOps Agent 是一个有真实业务场景、技术栈匹配、差异化明显的项目。但它存在过度设计和范围膨胀的风险，必须严格收窄 MVP 范围，聚焦核心能力验证。

## 2. 为什么可以做

**垂直场景明确**：售后客服工单处理是一个具体的、可定义的业务场景。不是"做一个聊天机器人"这种模糊需求，而是"处理一条售后工单"这个明确任务。

**技术栈匹配 AI Agent 岗位**：LangGraph、RAG、Tool Calling、FastAPI、Pydantic、结构化输出——这些技术栈完全匹配深圳 AI Agent 应用开发类实习岗位的要求。

**MVP 可控**：2-4 天可以完成。6 个 Agent + 4 个 mock tools + 5-6 篇知识库 + 基础前端 + 基础 Eval。没有不可控的技术难点。

**和 CodePilot 差异化明显**：CodePilot 是开发者工具 Agent，CustomerOps Agent 是业务流程 Agent。两者不重复，形成组合优势。

**简历表达有价值**：可以说"设计并实现了 6 个 Agent 协作的售后工单处理系统，支持 RAG 检索、Tool Calling、结构化输出和 QA 质检"。这是一个有技术深度和业务理解的项目描述。

## 3. 为什么必须收窄

如果不收窄，CustomerOps Agent 会变成：

**大而全客服系统**：加入用户登录、权限系统、多租户、真实电商 API 接入——这不是 MVP，这是一个产品。

**普通聊天机器人**：如果只做"用户问什么，AI 回什么"，就失去了业务流程 Agent 的核心价值。

**过度设计的伪 ToB 系统**：加入复杂数据库、异步任务队列、长期记忆、多语言支持——这些是生产级系统的需求，不是 MVP 的需求。

**开发周期失控**：如果范围不收窄，2-4 天根本做不完，会变成一个"永远在开发中"的项目。

**Goal 模式容易跑偏**：在 Goal 模式下，如果不明确边界，AI 会倾向于"做得更完整"，导致范围膨胀。

**收窄的核心原则**：MVP 只验证技术能力，不验证商业可行性。mock-first，不接真实服务。

## 4. 适合作为简历第几项目

**建议**：

| 优先级 | 项目 | 理由 |
|--------|------|------|
| 第一核心项目 | CodePilot | 技术深度更强，面试讲解更方便 |
| 第二核心项目 | CustomerOps Agent | 业务理解 + Agent 编排，形成差异化 |
| 辅助展示项目 | ProfileAgent | 产品能力 + 前端展示 |

**理由**：CodePilot 的技术点更集中（代码分析、RAG、Tool Calling），面试时更容易讲清楚。CustomerOps Agent 的业务场景更复杂，适合作为第二项目展示业务理解能力。

## 5. 和 CodePilot、ProfileAgent 的组合关系

```
CodePilot（第一核心项目）
├── 定位：AI 代码审查与仓库理解 Agent
├── 展示：技术深度、AI 工程能力
├── 技术点：代码分析、RAG、Tool Calling、结构化输出
└── 面试讲解：技术方案、实现细节

CustomerOps Agent（第二核心项目）
├── 定位：售后客服工单业务流程 Agent
├── 展示：业务理解、多 Agent 编排
├── 技术点：Agent Workflow、RAG、Tool Calling、FastAPI
└── 面试讲解：业务场景、流程设计、技术实现

ProfileAgent（辅助展示项目）
├── 定位：个人作品集与求职问答 Agent
├── 展示：产品能力、前端设计
├── 技术点：对话设计、前端展示
└── 面试讲解：产品思路、用户体验
```

**组合效果**：三个项目覆盖 AI 应用开发的不同维度——技术深度（CodePilot）、业务广度（CustomerOps Agent）、产品能力（ProfileAgent）。

## 6. 2～4 天 MVP 开发建议

### Day 1：后端地基 + 核心 Agent

**上午**：
- 项目目录结构初始化
- Pydantic Schema 定义（所有 Agent 的输入输出）
- mock 数据准备（订单、物流、政策）
- 知识库 Markdown 文档编写

**下午**：
- Intent Agent 实现
- Retrieval Agent 实现
- Tool Agent 实现（4 个 mock tools）
- 基础测试

### Day 2：业务 Agent + 编排

**上午**：
- Policy Agent 实现
- Reply Agent 实现
- QA Agent 实现

**下午**：
- Orchestrator 实现（编排 6 个 Agent）
- Analyze API 实现（FastAPI 接口）
- 端到端测试

### Day 3：前端 + 联调

**上午**：
- 前端项目初始化
- 工单输入页面
- Agent Timeline 组件

**下午**：
- 结果展示页面（Evidence、Tool Result、Policy、Reply、QA）
- 前后端联调
- 基础样式

### Day 4：Eval + 收尾

**上午**：
- Eval 测试用例准备（10 条 bad case）
- Eval API 实现
- Eval 页面

**下午**：
- README 编写
- 文档完善
- 简历包装准备
- 最终测试

## 7. 明确不能进入 MVP 的功能

以下功能**必须删除**，不进入 MVP：

| 功能 | 原因 |
|------|------|
| 用户登录 | MVP 不需要用户系统 |
| 多租户 | MVP 只服务一个场景 |
| 权限系统 | MVP 不需要权限控制 |
| 真实支付 | MVP 使用 mock 数据 |
| 真实退款 | MVP 使用 mock 数据 |
| 真实电商平台 API | MVP 不接真实业务系统 |
| 真实在线客服发送 | MVP 只生成建议，不发送 |
| 复杂知识库管理后台 | MVP 直接读取本地文件 |
| 大规模向量数据库 | MVP 使用本地 Markdown 文件 |
| 复杂长期记忆 | MVP 不需要会话记忆 |
| 异步任务队列 | MVP 使用同步处理 |
| 多语言客服 | MVP 只做中文 |

**后续扩展方向**（不进入 MVP）：
- 接入真实 LLM
- 接入 Chroma / FAISS
- 接入真实电商 API
- 接入真实客服系统
- Docker 部署
- 更完整的 Eval 指标
- 多轮客服会话
- 知识库管理后台
