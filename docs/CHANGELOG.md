# CustomerOps Agent｜变更记录

本文件记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## 变更类型说明

- **Added** - 新增功能
- **Changed** - 变更现有功能
- **Deprecated** - 即将废弃的功能
- **Removed** - 移除的功能
- **Fixed** - Bug 修复
- **Security** - 安全相关变更

## [未发布]

### Added
- 无

### Changed
- 无

### Fixed
- 无

## [0.0.8] - Pre-MVP Readiness Audit

**发布日期**：2026-06-11

**版本说明**：Pre-MVP Readiness Audit，审查 M0-M6 是否严格符合"开发前 9 步准备"，验证工程准备状态，修复文档不一致问题。

### Added

- Added `docs/PRE_MVP_READINESS.md` — Pre-MVP 审查报告
  - 9-Step Checklist 全部 Pass
  - Engineering Readiness Checklist 全部 Pass
  - Goal Mode Entry Conditions 全部满足
  - 结论：Ready for Goal Mode MVP Development

### Changed

- Updated `README.md`
  - 修正开发进度为 "Pre-MVP Readiness Audit completed"
  - 修正技术栈描述（AI 改为 mock-first / rule-based，数据改为 JSON file）
  - 补充文档链接（新增 PRD / DESIGN / TECHNICAL_SPEC）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Pre-MVP Readiness Audit completed
  - 新增 Pre-MVP 审查完成记录
  - 更新下一步为 Goal 模式 MVP 开发
  - 更新禁止事项为 Goal 模式规则
  - 核心文档列表新增 PRE_MVP_READINESS.md

## [0.0.7.3] - Official Frontend Design Skill Review

**发布日期**：2026-06-11

**版本说明**：Module 6.3 安装官方 frontend-design skill，重新审查首页，优化为更成熟的 ToB 工单处理工作台。

### Changed

- Installed official frontend-design skill from Anthropic skills repository
  - 来源：https://github.com/anthropics/skills
  - 安装方式：手动下载（npx skills 命令不可用）
  - 路径：`.claude/skills/frontend-design/SKILL.md`
  - 已读取 SKILL.md 并基于其指导进行设计审查

- Re-reviewed homepage using frontend-design skill guidance
  - 审查结论：无视觉焦点、信息层级扁平、Agent Timeline 缺乏流程感、空状态过多、缺少签名元素、布局节奏单调
  - 可保留：色彩系统、Header 结构、卡片边框风格、12 栏网格、模块划分

- Refined homepage into a more mature ToB support ticket workflow console
  - 新增 Pipeline 进度条（签名元素）：6 步带编号水平进度条 + 0/6 complete 计数
  - Agent Workflow 升级为 8 栏主区域，成为视觉主角
  - Review Summary + Reply Preview 降为 4 栏副区域
  - Agent 步骤增加编号（1-6）和执行时间列
  - 空状态改为真实占位内容（订单号、产品类型、物流公司等）
  - Evidence 增加真实文档名和相关度分数
  - Tool Results 增加真实数据展示
  - 标题使用 uppercase tracking-wider 建立视觉层级
  - 字号分层：标题 10px uppercase、正文 11-12px、辅助 10px

- Updated development status
  - `docs/DEV_STATUS.md` 更新为 Module 6.3 completed
  - 记录 skill 来源、安装方式、审查结论、重构结果

## [0.0.7.2] - Frontend Design Skill Repair

**发布日期**：2026-06-11

**版本说明**：Module 6.2 使用 frontend/design skill 对首页进行设计审查和重构，将 AI demo 风格的占位页优化为专业 ToB 工单处理工作台。

### Changed

- Used frontend/design skill to review and refine the placeholder homepage
  - 本地无可用 frontend/design/UI/UX skill（`.claude/skills/` 目录不存在）
  - 直接基于 `docs/DESIGN.md` 设计规范进行专业设计审查
  - 审查结论：Agent 名称错误、无信息层级、缺少必要模块、内容空洞、无导航结构、整体像模板页

- Reworked homepage into a ToB support ticket workflow console
  - 新增 Header：项目名 + Tickets/Eval 导航 + Mock Mode 状态指示 + 版本号
  - Ticket Intake：Customer Message + Order ID + Product Type + Analyze 按钮 + Quick tickets 快捷标签
  - Agent Workflow：6 个 Agent 正确名称垂直时间线（Intent → Retrieval → Tool → Policy → Reply → QA）
  - Review Summary：Final Result / Risk Level / QA Score 三栏 + Human Review 状态 + Ticket ID
  - Reply Preview：回复草稿占位区域
  - Evidence Preview：3 个 policy document 占位卡片（来源 + 相关度）
  - Tool Results：get_order + get_logistics 两个工具结果面板（键值对格式）
  - QA / Human Review：QA Score + Risks Detected + Suggestion + Risk List

- Reduced AI-demo visual style
  - 移除大面积空白和灰色占位 box
  - 使用 DESIGN.md 规范的企业蓝主色 + 状态色体系
  - 信息密集型布局，12 栏栅格系统
  - 细边框白色卡片，无渐变无玻璃拟态
  - 系统字体栈（移除 Google Fonts 网络依赖）

- Updated development status
  - `docs/DEV_STATUS.md` 更新为 Module 6.2 completed
  - 记录 design skill 使用情况、审查结论、重构结果

## [0.0.7.1] - Conda Environment Fix

**发布日期**：2026-06-11

**版本说明**：Module 6.1 修正后端验证环境，从系统 Python 切换到 Conda 环境，补充 Windows Conda 路径指引。

### Changed

- Revalidated backend initialization using the customerops-agent Conda environment
  - M6 问题：最初后端验证使用了系统 Python 3.11.5，已修正为 Conda 环境
  - Conda 路径：`E:\Conda\Scripts\conda.exe`（conda 25.9.1）
  - 环境名：`customerops-agent`（新建）
  - Python 版本：3.11.15 (conda-forge)
  - Python executable：`E:\Conda\envs\customerops-agent\python.exe`
  - pytest: 2/2 passed
  - ruff: All checks passed
  - frontend build: Successfully compiled (Next.js 16.2.9)

- Added Windows Conda path guidance to README
  - 补充 Conda 路径查找表格
  - 补充完整 Conda 命令示例（create / pip install / pytest / ruff / uvicorn）
  - 说明路径可替换

- Updated development status with Conda environment verification results
  - `docs/DEV_STATUS.md` 更新为 Module 6.1 completed
  - 记录 M6 问题、修正措施、验证结果
  - 下一步进入 Module 7

## [0.0.7] - Project Initialization

**发布日期**：2026-06-11

**版本说明**：Module 6 项目初始化，创建 backend / frontend 基础结构，FastAPI health API，Next.js 占位首页。

### Changed

- Initialized backend FastAPI project structure
  - 创建 `backend/app/` 目录结构（api / core / agents / schemas / services / rag / tools / data）
  - 创建 `backend/app/main.py` FastAPI 应用入口
  - 创建 `backend/app/api/routes_health.py` health 端点
  - 创建 `backend/app/core/config.py` 基础配置
  - 创建 `backend/requirements.txt` 依赖列表
  - 创建 `backend/conftest.py` pytest 配置

- Added health API and health test
  - `GET /health` 返回 `{"status": "ok", "service": "customerops-agent", "mode": "mock"}`
  - `backend/tests/test_health.py` 包含 2 个测试用例

- Initialized frontend Next.js project structure
  - 使用 `create-next-app` 创建 Next.js 16 + TypeScript + Tailwind CSS 项目
  - 创建 `frontend/app/page.tsx` ToB 工作台占位首页
  - 创建 `frontend/app/globals.css` 设计系统变量
  - 创建 `frontend/app/layout.tsx` 布局和元数据
  - 创建 `frontend/lib/api.ts` API 客户端占位
  - 创建 `frontend/types/ticket.ts` 类型定义占位

- Added placeholder ToB workspace homepage
  - 显示项目名 CustomerOps Agent
  - 显示定位：售后客服工单多 Agent 工作台
  - 工单输入区域占位设计
  - Agent Timeline 占位区域（6 个 Agent 步骤）
  - Evidence / Tool Result / QA 占位卡片

- Added README, .env.example, and .gitignore
  - `README.md` 包含项目简介、技术栈、启动说明、当前状态
  - `.env.example` 包含示例配置（无真实密钥）
  - `.gitignore` 排除敏感文件和缓存目录

- Updated development status
  - `docs/DEV_STATUS.md` 更新为 Module 6 completed
  - `docs/CHANGELOG.md` 新增本条记录

## [0.0.6] - Development Rules and Initialization Checklist

**发布日期**：2026-06-11

**版本说明**：Module 5 开发规矩 / Git 策略 / 初始化前检查，为后续项目初始化和 Goal 模式开发建立最终规则。

### Changed

- Updated `docs/DEV_RULES.md`
  - 新增 Goal 模式开发总规则（11 条）
  - 新增 Claude / AI 开发前必读文档列表（6 个文档）
  - 新增 Claude 每轮输出要求（6 项）
  - 新增分层职责规则（8 层职责定义）
  - 强化 Git 策略规则（8 个 checkpoint 节点）
  - 新增推荐提交信息规范（8 种场景）
  - 新增禁止提交内容清单（12 项）

- Updated `docs/TECHNICAL_SPEC.md`
  - 新增 Initialization Readiness Checklist 章节（第 15 节）
  - 文档准备检查（6 项）
  - 范围准备检查（4 项）
  - 技术准备检查（6 项）
  - 初始化必须创建（9 项）
  - 初始化禁止（8 项）
  - 初始化验收（9 项）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Module 5 Development Rules, Git Strategy, and Initialization Checklist completed
  - 已完成：开发规矩、AI 协作规则、Git 策略、初始化检查清单
  - 下一步：Module 6 项目初始化

## [0.0.5.1] - Conda Environment Rule

**发布日期**：2026-06-11

**版本说明**：Module 4.1 补充 Python Conda 环境开发规则，明确后端 Python 必须使用 Conda 虚拟环境管理。

### Changed

- Updated `docs/TECHNICAL_SPEC.md`
  - 新增 Python Environment（Conda）章节
  - 明确推荐环境名 `customerops-agent`、Python 3.11
  - 明确禁止使用全局 Python 和 venv
  - 添加后续初始化时的 Conda 环境创建和常用命令示例

- Updated `docs/DEV_RULES.md`
  - 新增 Python 开发环境规则（Conda）章节
  - 明确 Conda 环境要求、依赖管理、Claude 协作规则
  - 新增开发环境禁止项（禁止 base 环境安装依赖、禁止全局 Python、禁止 venv）

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Module 4.1 Conda Environment Rule Added
  - 已完成：Conda 环境规则补充
  - 下一步：Module 5 开发规矩 / Git 策略 / 初始化前检查

## [0.0.5] - Technical Foundation Planning

**发布日期**：2026-06-11

**版本说明**：Module 4 技术地基准备阶段，完成技术栈锁定、模块设计、API 契约、Schema 定义、Mock 数据规划等核心技术文档。

### Added

- Added `docs/TECHNICAL_SPEC.md` - 技术规格文档
  - 技术目标定义
  - Fixed Stack（Python 3.11+ / FastAPI / Pydantic v2 / Next.js / React / TypeScript / Tailwind CSS）+ Future Replaceable Stack（LangGraph / 真实 LLM / Chroma / PostgreSQL / Docker）
  - 非功能需求（安全 / 性能 / 可用性 / 成本）
  - 项目目录结构设计（backend + frontend 完整目录树）
  - 后端模块设计（API / Service / Agent / RAG / Tools / Core 六层）
  - 前端模块设计（3 页面 + 15 组件 + lib / types）
  - Agent 工作流设计（6 Agent 固定线性流程 + 输入输出 + 失败处理 + 实现方式）
  - API 契约（6 个接口：health / examples / tickets analyze / tickets get / evals cases / evals run）
  - Pydantic Schema 设计（14 个核心 Schema 字段定义）
  - Mock 数据设计（mock_orders / mock_logistics / eval_cases）
  - Knowledge Base 设计（6 篇 Markdown 知识库）
  - 测试计划（11 类测试 + 验收标准）
  - 项目初始化要求（11 项）
  - Goal 模式技术指令摘要

### Changed

- Updated `docs/PROJECT_CONTEXT.md`
  - Goal 模式上下文文档列表新增 `docs/TECHNICAL_SPEC.md`

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Module 4 Technical Foundation Planning completed
  - 已完成：技术地基规划全部内容
  - 下一步：Module 5 开发规矩 / Git 策略 / 初始化前检查
  - 更新禁止事项

## [0.0.4.1] - Documentation Consolidation and Scope Correction

**发布日期**：2026-06-11

**版本说明**：文档收敛与 PRD 范围修正，将阶段性文档整合为核心文档，明确 MVP / Future Scope / Permanent Safety Boundaries 区分。

### Changed

- Consolidated PRD-related documents into `docs/PRD.md`
  - 合并自：01_IDEA、02_IDEA_PRESSURE_TEST、03_IDEA_DECISION、04_PRD_DRAFT、05_PRD_REVIEW、06_PRD_FINAL、MVP_SCOPE、PROJECT_SCOPE
  - 明确 Current MVP Scope（20 项）
  - 明确 MVP Out of Scope but Future Possible（15 项）
  - 明确 Permanent Safety Boundaries（11 项）
  - 明确 Explicit Non-goals（7 项）
  - 明确后续版本路线（MVP → V1 → V2 → V3 → V4）

- Consolidated design-related documents into `docs/DESIGN.md`
  - 合并自：07_DESIGN_GUIDE、08_PAGE_PLAN、09_USER_FLOW、FRONTEND_DESIGN_REFERENCE
  - 明确 MVP 页面（3 个 + 1 个可选）
  - 明确 Future Pages（6 个）
  - 保留 15 个核心组件定义
  - 保留 9 个用户流程
  - 保留视觉基调和禁止风格

- Archived planning documents under `docs/archive/planning/`
  - 01_IDEA.md → archive
  - 02_IDEA_PRESSURE_TEST.md → archive
  - 03_IDEA_DECISION.md → archive
  - 04_PRD_DRAFT.md → archive
  - 05_PRD_REVIEW.md → archive
  - 06_PRD_FINAL.md → archive
  - MVP_SCOPE.md → archive
  - PROJECT_SCOPE.md → archive
  - 07_DESIGN_GUIDE.md → archive
  - 08_PAGE_PLAN.md → archive
  - 09_USER_FLOW.md → archive
  - FRONTEND_DESIGN_REFERENCE.md → archive

- Updated `docs/PROJECT_CONTEXT.md`
  - 新增 Goal 模式上下文规则：核心文档列表 + archive 说明

- Updated `docs/DEV_STATUS.md`
  - 当前阶段：Document consolidation and PRD scope correction completed
  - 已完成：文档收敛、PRD 合并、Design 合并、范围区分、历史归档
  - 下一步：Module 4 技术地基准备
  - 更新禁止事项

## [0.0.4] - Product Design and User Flow

**发布日期**：2026-06-11

**版本说明**：Module 3 产品设计与页面流程阶段，完成设计基调定义、页面结构规划、核心用户流程设计和前端设计参考整理。

### Added

- Added `docs/07_DESIGN_GUIDE.md` - 产品设计指南
  - 设计定位：ToB 客服运营后台，不是聊天机器人
  - 视觉风格：企业蓝主色、4px 基础网格、白色卡片 + 细边框
  - 信息层级：8 级优先级定义
  - 组件设计：15 个核心组件的设计原则（TicketInput、AgentTimeline、EvidencePanel 等）
  - 响应式原则：桌面端为主，1280px / 1024px 断点

- Added `docs/08_PAGE_PLAN.md` - 页面规划
  - Page 1：工单分析工作台（首页）— 输入工单、选择示例、启动分析
  - Page 2：分析结果详情页 — Agent Timeline + 结构化结果展示
  - Page 3：Eval / Bad Case 页面 — 评估用例和结果展示
  - Page 4：About / Architecture（可选，不单独做页面）
  - 每个页面的布局、核心模块、用户操作、对应 API、状态设计

- Added `docs/09_USER_FLOW.md` - 核心用户流程
  - 9 个核心流程：正常售后、缺订单号、物流查询、发票问题、投诉高风险、RAG 无结果、Tool 失败、QA 不通过、Eval
  - 每个流程的 Agent 执行顺序、输入输出、前端展示
  - 关键差异点和异常处理

- Added `docs/FRONTEND_DESIGN_REFERENCE.md` - 前端设计参考
  - 设计参考来源：企业后台、工单系统、电商后台、AI 工作流、数据分析
  - 可借鉴设计系统：Ant Design、Material Design、Shopify Polaris、Atlassian、shadcn/ui
  - 页面设计关键词
  - 禁止风格清单
  - 推荐布局方案
  - Goal 模式前端指令摘要
  - 颜色系统参考（CSS 变量）

### Changed

- Changed `docs/DEV_STATUS.md` - 更新开发状态
  - 当前阶段：Module 3 产品设计与页面流程完成
  - 已完成：Module 3 全部文档
  - 下一步：Module 4 技术地基准备
  - 更新禁止事项和验收标准

## [0.0.3] - PRD and Scope Finalization

**发布日期**：2026-06-11

**版本说明**：Module 2 PRD 生成与固化阶段，完成 PRD 初版、PRD 审查、最终 PRD 固化和项目范围锁定。

### Added

- Added `docs/04_PRD_DRAFT.md` - PRD 初版文档
  - 项目背景和定位
  - 目标用户定义
  - 5 个核心场景（产品故障、退款换货、物流查询、发票问题、投诉高风险）
  - 12 项 MVP 核心功能
  - 输入输出定义
  - 核心流程（6 Agent 线性编排）
  - 13 项验收标准
  - 14 项暂不实现范围
  - 6 个风险点及控制方式

- Added `docs/05_PRD_REVIEW.md` - PRD 审查文档
  - 项目定位审查：未误解
  - MVP 范围审查：合理，部分功能需保持轻量
  - 15 项必须保留功能
  - 14 项必须删除功能
  - 10 项后续扩展方向
  - 6 项 Goal 模式风险及控制方式
  - PRD 收窄建议

- Added `docs/06_PRD_FINAL.md` - 最终 PRD 文档
  - 15 项 MVP 必做功能
  - 14 项明确禁止功能
  - 用户使用路径
  - 系统输入输出定义
  - 6 个 Agent 详细定义（职责、输入、输出、失败处理）
  - 16 项功能验收标准
  - 9 项 MVP 成功标准

- Added `docs/PROJECT_SCOPE.md` - 项目范围锁定文档
  - 唯一目标
  - 15 项 In Scope
  - 20 项 Out of Scope
  - 9 项 Allowed Simplifications
  - 7 项 Hard Boundaries
  - 21 项 Goal 模式必须遵守清单

### Changed

- Changed `docs/DEV_STATUS.md` - 更新开发状态
  - 当前阶段：Module 2 PRD 生成与固化完成
  - 已完成：Module 2 全部文档
  - 下一步：Module 3 产品设计与页面流程
  - 更新禁止事项和验收标准

## [0.0.2] - Idea Validation and MVP Scope

**发布日期**：2026-06-11

**版本说明**：Module 1 想法验证 + MVP 收窄阶段，完成项目想法定义、压力测试、判断结论和 MVP 范围锁定。

### Added

#### 想法验证文档
- Added `docs/01_IDEA.md` - 想法定义文档
  - 项目想解决什么问题
  - 目标用户是谁
  - 用户为什么需要它
  - 和普通方案的区别
  - 最小可行版本定义
  - 项目希望证明的能力
  - 适合写进简历的原因
  - 适合深圳 AI Agent 岗位的原因

- Added `docs/02_IDEA_PRESSURE_TEST.md` - 想法压力测试文档
  - 需求是否真实
  - 用户场景是否明确
  - 项目是否有差异化
  - MVP 是否足够小
  - 技术实现是否可控
  - 成本是否可接受
  - 是否适合当前阶段开发
  - 是否适合写进简历
  - 是否存在伪需求
  - 是否存在过度设计风险
  - 是否和岗位匹配
  - 是否和 CodePilot 互补
  - 压力测试结论

- Added `docs/03_IDEA_DECISION.md` - 想法判断结论文档
  - 最终判断：可以做，但需要收窄范围
  - 为什么可以做
  - 为什么必须收窄
  - 简历项目优先级建议
  - 和 CodePilot、ProfileAgent 的组合关系
  - 2-4 天 MVP 开发建议
  - 明确不能进入 MVP 的功能

- Added `docs/MVP_SCOPE.md` - MVP 范围文档
  - MVP 一句话范围
  - 当前版本必须做
  - 当前版本不做
  - 输入输出定义
  - 核心 Agent 定义
  - 核心工具定义
  - 知识库范围
  - 验收标准
  - 后续扩展方向

### Changed

- Changed `docs/DEV_STATUS.md` - 更新开发状态
  - 当前阶段：Module 1 想法验证 + MVP 收窄
  - 已完成：Module 1 全部文档
  - 下一步：Module 2 PRD 生成与固化
  - 更新禁止事项和验收标准

## [0.0.1] - Context Init

**发布日期**：2026-06-11

**版本说明**：项目上下文初始化阶段，建立开发文档和规则。

### Added

#### 文档层
- Added `docs/PROJECT_CONTEXT.md` - 项目上下文文档
  - 项目名称和定位
  - 项目背景和目标用户
  - 核心业务场景
  - MVP 核心能力
  - 多 Agent 设计方向
  - 项目边界（不做什么）
  - 和普通 AI 客服机器人的区别
  - 和 CodePilot 的差异化
  - 适合简历和面试展示的原因

- Added `docs/DEV_RULES.md` - 开发规则文档
  - 总开发原则（小步快跑、渐进式开发、文档先行）
  - AI 协作规则
  - 每轮开发规则（开始前、开发中、结束后）
  - 文件修改规则
  - 模块拆分规则（分层架构）
  - API 契约规则
  - 安全规则
  - LLM 使用规则
  - 测试规则
  - Git 回滚规则
  - 禁止事项

- Added `docs/DEV_STATUS.md` - 开发状态文档
  - 当前阶段：Step 0.1 项目上下文初始化
  - 当前项目状态：初始化中
  - 已完成内容
  - 未开始内容
  - 当前限制
  - 下一步建议
  - 当前可修改范围
  - 当前禁止修改范围
  - 当前验收标准
  - 后续开发路线

- Added `docs/CHANGELOG.md` - 变更记录文档（本文件）
  - 变更记录格式说明
  - 当前版本记录

### Changed
- 无

### Fixed
- 无

### Security
- 无

## 版本规划

### v0.0.x - 项目初始化与验证
- [x] v0.0.1 - Context Init（项目上下文初始化）
- [x] v0.0.2 - Idea Validation and MVP Scope（想法验证 + MVP 收窄）
- [x] v0.0.3 - PRD Generation（PRD 生成与固化）
- [x] v0.0.4 - Product Design and User Flow（产品设计与页面流程）
- [x] v0.0.5 - Technical Foundation Planning（技术地基准备）
- [x] v0.0.6 - Development Rules and Initialization Checklist（开发规矩和初始化检查）
- [x] v0.0.7 - Project Initialization（项目初始化）
- [x] v0.0.7.1 - Conda Environment Fix（Conda 环境修正与复验）
- [x] v0.0.7.2 - Frontend Design Skill Repair（前端首页设计审查与重构）
- [x] v0.0.7.3 - Official Frontend Design Skill Review（官方 skill 安装与审查）

### v0.1.x - 设计阶段
- [x] v0.1.0 - Architecture Design（技术架构设计）— 已在 v0.0.5 完成
- [x] v0.1.1 - UI/UX Design（UI/UX 设计）— 已在 v0.0.4 完成
- [x] v0.1.2 - Schema Design（数据与 Schema 设计）— 已在 v0.0.5 完成

### v0.2.x - 核心功能
- [ ] v0.2.0 - Core Agents（核心 Agent 实现）
- [ ] v0.2.1 - Business Flow（业务流程实现）
- [ ] v0.2.2 - API Layer（API 接口实现）

### v0.3.x - 前端和集成
- [ ] v0.3.0 - Frontend（前端实现）
- [ ] v0.3.1 - Integration Test（集成测试）
- [ ] v0.3.2 - Evaluation（评估和优化）

### v0.4.x - 完善和展示
- [ ] v0.4.0 - Documentation（文档完善）
- [ ] v0.4.1 - Demo（演示准备）
- [ ] v0.4.2 - Resume（简历优化）

### v1.0.0 - MVP 完成
- [ ] 完整的售后客服工单处理流程
- [ ] 多 Agent 协作演示
- [ ] RAG 知识库检索演示
- [ ] Tool Calling 演示
- [ ] 结构化输出演示
- [ ] 基础评估机制
- [ ] 前后端联调
- [ ] 演示文档和视频
