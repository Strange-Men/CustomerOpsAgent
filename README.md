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
- [产品需求文档](docs/PRD.md)
- [设计文档](docs/DESIGN.md)
- [技术规格文档](docs/TECHNICAL_SPEC.md)
- [开发规则](docs/DEV_RULES.md)
- [开发状态](docs/DEV_STATUS.md)
- [变更记录](docs/CHANGELOG.md)

## 技术栈

- **后端**: Python 3.11 (Conda), FastAPI, Pydantic v2
- **AI**: mock-first / rule-based (MVP)，LangGraph (Future)
- **数据**: JSON file (MVP)
- **前端**: Next.js 16, TypeScript, Tailwind CSS

## 快速开始

### 前置要求

- [Conda](https://docs.conda.io/) (Miniconda / Anaconda)
- Node.js 18+
- npm

### 后端环境（必须使用 Conda）

> **⚠️ 后端 Python 必须使用 Conda 环境，不允许使用系统 Python 或 venv。**

#### 1. 查找 Conda 路径

如果 `conda` 不在 PATH 中，需要使用完整路径调用。常见路径：

| 安装位置 | 路径 |
|---------|------|
| E 盘自定义 | `E:\Conda\Scripts\conda.exe` |
| E 盘 Miniconda | `E:\Miniconda3\Scripts\conda.exe` |
| D 盘 Miniconda | `D:\Miniconda3\Scripts\conda.exe` |
| 用户目录 | `%USERPROFILE%\miniconda3\Scripts\conda.exe` |

本机 Conda 路径：`E:\Conda\Scripts\conda.exe`

#### 2. 创建 Conda 环境

```powershell
& "E:\Conda\Scripts\conda.exe" create -n customerops-agent python=3.11 -y
```

> 将 `E:\Conda\Scripts\conda.exe` 替换为你的实际 Conda 路径。

#### 3. 安装后端依赖

```powershell
& "E:\Conda\Scripts\conda.exe" run -n customerops-agent python -m pip install -r backend/requirements.txt
```

#### 4. 运行后端测试

```powershell
& "E:\Conda\Scripts\conda.exe" run -n customerops-agent python -m pytest backend
```

#### 5. 运行代码检查

```powershell
& "E:\Conda\Scripts\conda.exe" run -n customerops-agent python -m ruff check backend
```

#### 6. 启动后端服务

```powershell
& "E:\Conda\Scripts\conda.exe" run -n customerops-agent uvicorn app.main:app --app-dir backend --reload
```

### 前端

```powershell
cd frontend
npm install
npm run dev
```

## 开发进度

Pre-MVP Readiness Audit completed. 准备进入 Goal 模式 MVP 开发。

详见 [开发状态](docs/DEV_STATUS.md) | [Pre-MVP 审查报告](docs/PRE_MVP_READINESS.md)

## 许可证

MIT License
