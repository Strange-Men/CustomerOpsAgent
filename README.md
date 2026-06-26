# CustomerOpsAgent｜跨境电商客服 Agent 与 RAG 质量评估增强

English version: [README.en.md](./README.en.md)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?logo=typescript&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Enabled-8A2BE2)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7?logo=render&logoColor=black)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?logo=vercel&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-293_passed-0A9EDC?logo=pytest&logoColor=white)

## 项目简介

CustomerOpsAgent 是一个面向跨境电商客服场景的 AI Agent 系统。项目不是普通聊天机器人，而是覆盖 **"知识库建设 → RAG 检索 → Agent 路由 → 回答生成 → 自动化评测 → Bad Case 优化 → 真实 LLM 对接 → Docker 交付"** 的完整工程闭环。

搭建分层知识库与 RAG 检索体系，优化召回策略与 Prompt 模板，在自建评测集上 Recall@5 达到 90.00%；设计 RAG Evaluation Harness，从检索命中、引用覆盖、回答合格率、fallback 率和 Bad Case 结构性通过率等维度自动化量化评估回答质量；累计构建并优化 131 条典型客服 Bad Case Bank，覆盖清关、退款、物流、支付、退换货等高频场景，回答合格率从 46.72% 提升至 60.66%，相对提升约 30%。

## 在线体验

| 入口 | 地址 |
|------|------|
| 前端 Demo | https://customer-ops-agent.vercel.app/ |
| 后端 API | https://customeropsagent.onrender.com |
| API Docs | https://customeropsagent.onrender.com/docs |

> Render 免费实例可能冷启动，首次访问需等待 30–90 秒。

## 背景与问题

跨境电商客服每天面对大量重复性咨询：清关延迟、退款到账、物流追踪、支付失败、退换货政策等。这些问题有三个共同特征：

1. **知识分散**。政策文档、物流规则、退款流程散落在不同系统中，客服需要翻资料、查表格、问同事。
2. **回复口径不统一**。不同客服对同一问题的解释方式不同，容易出现承诺不一致。
3. **效果难量化**。传统方案只做问答，没有评测闭环，无法回答"回答质量到底怎么样"和"优化后到底好了多少"。

如果只做一个普通聊天机器人，回答会变成不可追溯的自由文本——用户看不到证据来源，开发者也无法复盘系统为什么走 RAG、工具或 fallback。这个项目的目标是构建一个**可演示、可解释、可评估**的客服 Agent 能力体系。

## 解决方案

项目按照完整工程闭环来组织，核心链路如下：

```text
User Query
  ↓
Intent Recognition（意图识别 + 二级意图）
  ↓
Route Decision（路由决策）
  ├── RAG Knowledge Base（知识库检索 + 证据绑定）
  ├── Mock Logistics Tool（模拟物流查询）
  └── Fallback Handler（兜底规则）
  ↓
Answer Composer（结构化回答生成）
  ↓
Evaluation Harness（自动化质量评估）
  ↓
Bad Case Bank（典型问题迭代优化）
  ↓
Real LLM Profile / Mock Fallback
```

每一层都有独立的评估指标和优化空间，不是一次性写完就结束的 demo。

## 核心能力

| 能力 | 说明 |
|------|------|
| 分层知识库 | 14 条种子知识文档，覆盖清关/退款/物流/支付/退换货等 12 个场景 |
| RAG 检索 | 自实现 BM25 检索器 + query expansion + metadata boost + doc diversity |
| Agent Workflow | 节点式工作流：意图识别 → 路由 → RAG/工具 → 证据检查 → 回答生成 → fallback |
| Answer Composer | 结构化回答模板：结论 → 依据 → 操作建议 → 引用来源 |
| Evaluation Harness | 检索评测（Recall@1/3/5, MRR）+ 回答评测（6 维度）+ Bad Case 评测 |
| Bad Case Bank | 131 条结构化 bad case，覆盖 11 个客服场景，97.71% 结构性通过率 |
| LLM Adapter | Profile-based 模型切换，支持 mock / deepseek / doubao / mimo |
| 安全模型选择 | 前端只传 `llm_profile`，后端白名单 + 环境变量解析，不暴露 API key |
| Docker 本地运行 | Docker Compose 一键启动前后端，默认 mock 模式 |
| 线上部署 | Render 后端 + Vercel 前端，线上 smoke 已通过 |

## 技术架构

```text
User
  ↓
React / Vite / TypeScript Frontend
  ↓  POST /api/agent/chat
FastAPI Backend
  ↓
Agent Workflow
  ├── Intent Recognition（11 个意图分类）
  ├── RAG Retriever（BM25 + query expansion + metadata boost）
  ├── Mock Logistics Tool（模拟物流查询）
  ├── Fallback Rules（10 条兜底规则）
  ├── Answer Composer（结构化模板）
  └── LLM Adapter
        ├── mock（默认）
        ├── deepseek profile
        ├── doubao profile
        └── mimo profile（真实 LLM 已验证）
```

DeepSeek / Doubao / Mimo 只是 profile，key 只放后端环境变量，前端不直接调用模型服务。

## RAG 与 Agent 工作流

### RAG 检索体系

- **知识库**：14 条 JSONL 格式知识文档，每条包含 category / market / language / policy_type 等结构化 metadata。
- **Chunking**：按字符切分，max_chars=320, overlap=40，保留 chunk 级 metadata。
- **Baseline Retriever**：自实现 BM25，支持英文分词 + CJK 字符级 bigram。
- **Optimized Retriever**：在 baseline 基础上增加跨语言同义词扩展、category/market/language 推断、metadata-aware score adjustment 和 doc-level diversity。

### Agent 工作流

```text
Start → Entity Extraction → Intent Recognition → Route Decision
  ↓
  ├── RAG Route: Retrieval → Evidence Check → Prompt Builder → Answer Generator → Citation Check
  ├── Logistics Route: Mock Tool → Answer Generator
  └── Fallback Route: Fallback Rules → Fallback Answer
  ↓
Response（answer / route / intent / citations / answer_source / llm_model）
```

工作流覆盖 11 个意图分类（customs / refund / logistics_status / logistics_policy / return / exchange / address / order / payment / package / coupon），通过规则驱动的消歧逻辑处理多意图冲突。

## 质量评测与 Bad Case 优化

### 评测体系三层结构

| 层级 | 工具 | 指标 |
|------|------|------|
| 检索评测 | `retrieval_eval.py` | Recall@1/3/5, MRR |
| 回答评测 | `answer_eval.py` | Relevance, Groundedness, Completeness, Citation Hit Rate, Answer Pass Rate, Fallback Rate |
| Bad Case 评测 | `bad_case_eval.py` | Structural Pass Rate, Citation Coverage, Fallback Rate |

### 核心指标

| 指标 | 数值 | 说明 |
|------|------|------|
| Recall@5 | **90.00%** | top-5 检索命中预期文档 |
| Answer Pass Rate | 46.72% → **60.66%** | 回答合格率，相对提升约 30% |
| Citation Hit Rate | 83.61% → **95.90%** | 引用命中率，+12.29pp |
| Fallback Rate | 13.11% → **0.82%** | 兜底率，-12.29pp |
| Bad Case Bank | **131 条** | 覆盖 11 个客服场景 |
| Bad Case Pass | **128 / 131** | 结构性通过率 97.71% |
| pytest | **293 passed** | 后端全量测试 |
| ruff | **All checks passed** | 代码质量检查 |

### Bad Case Bank 场景覆盖

| 场景 | 数量 | 说明 |
|------|------|------|
| logistics | 15 | 物流配送、时效、追踪 |
| customs | 15 | 清关延迟、海关抽检、关税 |
| package | 15 | 包裹破损、丢失、理赔 |
| mixed | 15 | 多意图复合场景 |
| payment | 10 | 支付失败、风控 |
| coupon | 10 | 优惠券使用、过期 |
| exchange | 9 | 换货流程、时效 |
| address | 9 | 地址修改 |
| out_of_scope | 9 | 超出服务范围 |
| return | 8 | 退货条件、流程 |
| refund | 8 | 退款时间、到账 |
| order | 8 | 订单取消、优惠券退回 |

### 优化路径

- **v1.3.0 优化前（baseline）**：pass rate 46.72%，citation hit rate 83.61%，fallback rate 13.11%
- **v1.3.0 优化后**：pass rate 60.66%，citation hit rate 95.90%，fallback rate 0.82%
- **v1.4.0**：建立 131 条 Bad Case Bank + bad_case_eval 评测框架
- **详细报告**：[docs/RAG_QUALITY_IMPROVEMENT_REPORT.md](docs/RAG_QUALITY_IMPROVEMENT_REPORT.md) · [docs/BAD_CASE_BANK_REPORT.md](docs/BAD_CASE_BANK_REPORT.md)

## 真实 LLM 与安全模型切换

系统支持通过后端环境变量配置真实 LLM，已验证 Mimo 真实 profile：

- `answer_source=real_llm`，`llm_model=mimo-v2.5-pro`
- 真实 key 仅保存在 Render 后端环境变量，前端只传 `llm_profile`
- 未配置真实模型时自动 fallback 到 mock
- 详细报告：[docs/REAL_MIMO_SMOKE_REPORT.md](docs/REAL_MIMO_SMOKE_REPORT.md)

## Docker 本地运行

使用 Docker Compose 一键启动前后端，无需手动安装 Python/Node 环境：

```bash
docker compose build --no-cache
docker compose up -d
```

| 服务 | 地址 |
|------|------|
| Frontend | http://localhost:8080 |
| Backend API Docs | http://localhost:8000/docs |

默认使用 mock profile，无需真实 LLM key。停止服务：`docker compose down`。

详细说明见 [docs/DOCKER_RUNBOOK.md](docs/DOCKER_RUNBOOK.md)。

## 本地开发

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

前端环境变量：

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 测试与评估

```powershell
# 后端测试
$env:PYTHONPATH="backend"
pytest -v

# 代码质量
ruff check backend/app/rag/schemas.py backend/app/rag/loader.py backend/app/rag/chunker.py backend/app/rag/retriever.py backend/app/rag/optimized_retriever.py backend/app/eval/retrieval_eval.py backend/app/eval/answer_eval.py backend/app/eval/bad_case_eval.py backend/app/eval/bad_case_schema.py backend/app/agent backend/app/api backend/app/llm backend/tests

# 前端构建
cd frontend
npm run build
```

当前验证结果：

- pytest：293 passed
- ruff：All checks passed
- frontend build：passed
- Docker Compose：本地验证通过

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

`llm_profile` 可选：mock / deepseek / doubao / mimo。未配置真实模型时自动 fallback mock。不要在请求中传 API key。

## 安全边界

- 前端不保存、不输入、不传递任何 LLM API key。
- 前端只传 `llm_profile`，后端白名单限制 profile。
- 未配置真实模型时自动 fallback mock。
- 当前未接真实物流 API，使用 mock logistics tool 模拟。
- 当前未接真实订单系统。
- `.env` 不提交 Git，真实 key 仅通过 Render 环境变量配置。

## 项目状态与 Roadmap

**当前版本**：v1.6.0-final-docs

| 阶段 | 状态 | 说明 |
|------|------|------|
| M0–M6 | ✅ | RAG + Eval + Agent Workflow + API + LLM Adapter |
| Frontend M1–M7 | ✅ | React scaffold → 单栏聊天 → API 接入 → 响应式 → 线上 smoke |
| v1.3.0-quality | ✅ | RAG 质量优化，pass rate +13.94pp |
| v1.4.0-badcase | ✅ | 131 条 Bad Case Bank + evaluation harness |
| v1.4.1-real-mimo | ✅ | Mimo 真实 LLM profile 验证通过 |
| v1.5.0-docker | ✅ | Docker Compose 本地一键运行 |
| v1.6.0-final-docs | ✅ | 最终文档收口 |

可选后续：

- 扩大知识库文档规模
- 接入真实物流工具 API
- case-level before/after 追踪
- 多语言知识库迁移

## 项目目录

```text
CustomerOpsAgent/
├── backend/
│   └── app/
│       ├── agent/          # Agent Workflow（intent, route, fallback, answer）
│       ├── api/            # FastAPI API endpoint
│       ├── eval/           # Evaluation Harness（retrieval, answer, bad case）
│       ├── llm/            # LLM Adapter（mock, openai-compatible）
│       └── rag/            # RAG（schemas, loader, chunker, retriever）
├── frontend/
│   └── src/
│       ├── components/     # React 组件
│       ├── data/           # 示例数据
│       └── lib/            # API client, types, constants
├── docs/                   # 项目文档
├── docker-compose.yml      # Docker Compose 配置
├── README.md
└── README.en.md
```
