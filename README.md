# CustomerOps Agent

面向售后客服工单的多 Agent 自动化处理系统

## 项目简介

CustomerOps Agent 是一个面向跨境电商 / 3C 售后客服工单的垂直 AI Agent MVP。用户输入一条售后问题后，系统自动完成工单意图识别、知识库检索、订单 / 物流工具调用、售后政策判断、客服回复生成和 QA 质检。

## 核心能力

1. **多 Agent 编排能力** - 多个专业 Agent 协作处理复杂工单
2. **RAG 知识库检索能力** - 从本地知识库检索相关政策和处理流程
3. **Tool Calling / Function Calling 能力** - 调用订单、物流等外部工具
4. **结构化输出和 Pydantic Schema 约束能力** - 确保 LLM 输出符合业务结构
5. **FastAPI 后端工程能力** - 规范的后端 API 设计和实现
6. **前后端联调能力** - 前端展示和后端处理的完整流程
7. **Bad Case / Eval 评估迭代能力** - 系统化的质量评估和改进机制

## 文档

- [项目上下文](docs/PROJECT_CONTEXT.md)
- [开发规则](docs/DEV_RULES.md)
- [开发状态](docs/DEV_STATUS.md)
- [变更记录](docs/CHANGELOG.md)

## 技术栈

- **后端**: Python, FastAPI
- **AI**: LangGraph, LangChain
- **数据**: Pydantic, SQLite
- **前端**: 待定

## 开发进度

当前处于 Step 0.1：项目上下文初始化阶段

详见 [开发状态](docs/DEV_STATUS.md)

## 许可证

MIT License
