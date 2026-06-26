# CustomerOpsAgent｜跨境电商客服 Agent 与 RAG 评估增强

English version: [README.en.md](./README.en.md)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?logo=typescript&logoColor=white)
![Tailwind_CSS](https://img.shields.io/badge/Tailwind_CSS-UI-06B6D4?logo=tailwindcss&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Enabled-8A2BE2)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7?logo=render&logoColor=black)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?logo=vercel&logoColor=white)
![Mock_Default](https://img.shields.io/badge/Mock-Default-orange)

## 项目简介

CustomerOpsAgent 是一个面向跨境电商客服场景的 AI Agent Demo，覆盖清关延迟、退款周期、物流查询等常见咨询。系统支持 RAG 知识库检索、意图路由、Mock 物流工具、fallback 兜底和安全模型 profile 选择。

前端提供暗黑粉紫风格的客服 Agent Console，后端提供 FastAPI API。当前默认使用 Mock 模式，可在无真实模型 key 的情况下运行；DeepSeek / Doubao 是可选增强 profile。

主要阅读对象包括：评估 Agent 架构的技术 reviewer、学习 RAG + workflow 模式的 AI 应用开发者，以及想快速体验客服 Agent Demo 的项目访问者。

## 在线预览

- 前端 Demo：https://customer-ops-agent.vercel.app/
- 后端 API：https://customeropsagent.onrender.com
- API Docs：https://customeropsagent.onrender.com/docs

当前已完成前端 API 接入。线上 smoke 仍建议以 M4.5 验证结果为准；Render 免费实例可能冷启动，需要等待。

## 项目亮点

- RAG 检索增强：支持知识库命中、citation、retrieved_doc_ids。
- Agent Workflow：支持意图识别、二级意图、路由、fallback。
- 安全模型选择器：前端只传 `llm_profile`，不暴露 API key。
- Mock 默认可运行：无真实模型 key 也能完整演示。
- 前后端分离：FastAPI + React/Vite。
- 可部署演示：Render 后端 + Vercel 前端。
- 评估闭环：包含 retrieval eval、answer eval、pytest、ruff。

## 项目说明

### 背景

跨境电商客服常见问题包括清关延迟、退款周期、订单物流查询、包裹异常和政策咨询等。这类问题通常需要先判断意图，再查找政策证据或订单上下文，最后给出可解释回复。

如果只做普通聊天机器人，回答容易变成不可追溯的自由文本：用户看不到证据来源，开发者也难以复盘系统为什么走 RAG、工具或 fallback。这个项目因此把重点放在“可演示、可解释、可评估”的客服 Agent 流程上，而不是描述成真实业务系统。

### 目标

构建一个可演示的客服 Agent Demo，使访问者能在 1 分钟内理解端到端决策链路，并满足以下任务：

- 业务任务：覆盖清关延迟、退款周期、物流查询等核心客服场景。
- 技术任务：搭建支持 RAG 检索、意图路由、工具调用和 fallback 的 Agent Workflow。
- 体验任务：让前端能够展示 answer、route、intent、citations、retrieved_doc_ids、answer_source 等关键字段。
- 约束任务：前端不保存、不输入、不传递任何真实模型 key；无真实 key 时仍可用 mock 完整演示。

这些任务对应的核心问题是：

- 用户问题如何进入 Agent。
- 系统如何路由到 RAG / 工具 / fallback。
- 回答如何携带 citations、metadata、answer_source。
- 模型选择如何在不暴露 key 的前提下完成。

### 实现

为完成上述任务，项目按“核心流程 → 核心能力 → 安全适配 → 前端展示 → 部署验证”的顺序实现：

- 核心流程：后端使用 FastAPI 设计 `/api/agent/chat`，API 只封装 workflow，不复制 Agent 逻辑。
- 意图与路由：workflow 处理 `intent` / `detail_intent` / `route`，区分 RAG 知识库、Mock 物流工具和 fallback。
- RAG 证据链：知识库检索返回 citations 与 `retrieved_doc_ids`，用于解决“回答缺少证据来源”的问题。
- 工具模拟：使用 mock logistics tool 模拟物流查询，保留工具调用链路，但不接真实物流 API。
- 模型适配：LLM Adapter 默认 mock，可选支持 openai-compatible real LLM；未配置真实模型时自动 fallback mock。
- 安全选择：前端只传 `llm_profile`，后端白名单限制 mock / deepseek / doubao，并由后端环境变量解析真实配置。
- 前端展示：React + Vite + TypeScript + Tailwind 搭建客服 Agent Console，展示问答、模型 profile、fallback 和评估相关 metadata。
- 部署演示：后端部署到 Render，前端部署到 Vercel，线上 M4.5 smoke 仍待完整验证。

### 结果

- 工程质量：后端测试 254 passed，Ruff All checks passed，frontend build passed。
- 检索结果：Retrieval Eval 20 cases，Recall@5 90%，MRR 0.785。Recall@5 表示 top-5 检索结果命中预期文档的比例，MRR 用于观察相关文档是否排在更靠前的位置。
- 回答结果：Answer Eval 122 cases，citation hit rate 83.61%，pass rate 46.72%。citation hit rate 用于观察引用是否命中预期证据；pass rate 46.72% 是当前基线，不当作高分，用来暴露回答质量的后续优化空间。
- 安全与可演示性：本地 smoke 中 mock / deepseek fallback / invalid profile 422 通过；无真实模型 key 也能演示完整链路。
- 访问入口：支持 Render + Vercel 部署预览，但线上 smoke 仍以 M4.5 验证结果为准。

对不同读者的价值：

- 对开发者：可以参考 FastAPI + RAG + workflow + adapter 的可复用工程结构。
- 对评估者：可以通过 route、intent、citations、answer_source 和评估指标复盘系统行为。
- 对项目访问者：可以直接从前端 Demo 体验客服 Agent 的问答与 fallback 流程。

## 技术架构

```text
User
  ↓
React / Vite Frontend
  ↓  POST /api/agent/chat
FastAPI Backend
  ↓
Agent Workflow
  ├── Intent Routing
  ├── RAG Retriever
  ├── Mock Logistics Tool
  ├── Fallback Handler
  └── LLM Adapter
        ├── mock
        ├── deepseek profile
        └── doubao profile
```

DeepSeek / Doubao 只是 profile。key 只放后端环境变量，前端不直接调用模型服务。

## 功能清单

已完成：

- RAG knowledge base retrieval
- citations / retrieved_doc_ids
- Agent route / intent / detail_intent
- fallback workflow
- mock logistics tool
- LLM adapter
- model profile selector
- frontend API integration
- Render / Vercel demo links

进行中 / 待验证：

- M4.5 online smoke
- Metadata + Citations 展示完善
- 响应式 polish
- zh-CN / en-US language toggle

## API 示例

```bash
curl -X POST "https://customeropsagent.onrender.com/api/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "清关延迟怎么办？",
    "order_id": null,
    "conversation_history": [],
    "llm_profile": "mock"
  }'
```

- `llm_profile` 可选：mock / deepseek / doubao。
- 未配置真实模型时 deepseek / doubao 会 fallback mock。
- 不要在请求中传 API key。

## 本地运行

后端：

```powershell
cd D:\Claude_workfile\CustomerOpsAgent
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

前端：

```powershell
cd frontend
npm install
npm run dev
```

前端环境变量说明：

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

线上 Vercel：

```text
VITE_API_BASE_URL=https://customeropsagent.onrender.com
```

- `VITE_API_BASE_URL` 是公开 API 地址。
- DeepSeek / Doubao key 不能放 Vercel。
- LLM key 只能放 Render 后端环境变量。

## 测试与评估

```powershell
pytest
ruff check
cd frontend
npm run build
```

当前结果：

- pytest：254 passed
- ruff：All checks passed
- frontend build：passed
- retrieval eval 当前基线：20 cases，Recall@5 90%，MRR 0.785
- answer eval 当前基线：122 cases，citation hit rate 83.61%，pass rate 46.72%

指标口径：

- Recall@5：每个问题返回的 top-5 文档中是否命中预期文档。
- MRR：第一个命中文档排名的倒数平均值，用于衡量排序质量。
- citation hit rate：回答引用的文档是否命中预期证据。
- answer pass rate：基于当前 answer eval 规则得到的回答通过率，是后续优化基线。

## 安全边界

- 不在前端保存任何 LLM API key。
- 不允许用户在前端输入 API key。
- 前端只传 `llm_profile`。
- 后端白名单限制 profile。
- 未配置真实模型时 fallback mock。
- 当前未接真实物流 API。
- 当前未接真实订单系统。
- 当前默认 mock，可无 key 运行。

## 项目状态 / Roadmap

当前进度：

- Backend：v1.1.0-demo + Frontend M4。
- Frontend：已完成 API integration + model profile selector。
- 下一步：M4.5 online smoke，M5 Metadata + Citations 展示完善。

Roadmap：

- M4.5：线上 Render + Vercel smoke 验证。
- M5：Metadata + Citations 展示完善。
- M6：fallback / error / empty 状态完善。
- M7：响应式与视觉 polish。
- M7.5：zh-CN / en-US 切换。
- M8：最终文档与 release checklist。
- M9：fresh clone + deployment final verification。

## 项目目录

```text
CustomerOpsAgent/
├── backend/
│   └── app/
│       ├── agent/
│       ├── api/
│       ├── llm/
│       └── rag/
├── frontend/
│   └── src/
│       ├── components/
│       ├── data/
│       └── lib/
├── docs/
├── README.md
└── README.en.md
```
