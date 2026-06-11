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

### v0.0.x - 项目初始化
- [x] v0.0.1 - Context Init（项目上下文初始化）
- [ ] v0.0.2 - Project Structure Init（项目结构初始化）
- [ ] v0.0.3 - Dependencies Init（依赖和配置初始化）

### v0.1.x - 架构设计
- [ ] v0.1.0 - Idea Validation（想法压力测试）
- [ ] v0.1.1 - Architecture Design（技术架构设计）
- [ ] v0.1.2 - Mock Data（Mock 数据准备）

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
