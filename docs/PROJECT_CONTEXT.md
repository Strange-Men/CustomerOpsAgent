# CustomerOps Agent｜项目上下文

## 1. 项目名称

CustomerOps Agent｜面向售后客服工单的多 Agent 自动化处理系统

## 2. 项目一句话定位

CustomerOps Agent 是一个面向跨境电商 / 3C 售后客服工单的垂直 AI Agent MVP，用户输入一条售后问题后，系统自动完成工单意图识别、知识库检索、订单 / 物流工具调用、售后政策判断、客服回复生成和 QA 质检。

**关键定位：CustomerOps Agent 是业务流程型 Agent，不是普通聊天机器人。**

## 3. 项目背景

跨境电商 / 3C 售后客服场景中，客服工单处理涉及多个环节：意图识别、知识检索、订单查询、物流追踪、政策判断、回复生成、质量检查。这些环节之间存在复杂的依赖关系和业务逻辑，传统的聊天机器人无法有效处理。

本项目旨在构建一个能够理解业务流程、自动编排多个 Agent 协作、并输出结构化结果的 AI Agent 系统，展示多 Agent 编排、RAG 检索、Tool Calling、结构化输出等核心能力。

## 4. 目标用户

- **直接用户**：跨境电商 / 3C 售后客服团队
- **间接用户**：需要处理售后工单的企业运营团队
- **项目展示受众**：技术团队负责人

## 5. 核心业务场景

用户输入一条售后问题，系统自动完成：意图识别 → 知识库检索 → 订单/物流查询 → 政策判断 → 回复生成 → QA 质检。

覆盖场景：产品故障售后、退款/换货咨询、物流查询、发票问题、投诉/高风险工单等。

## 6. MVP 核心能力

1. **多 Agent 编排能力**：多个专业 Agent 协作处理复杂工单
2. **RAG 知识库检索能力**：从本地知识库检索相关政策和处理流程
3. **Tool Calling / Function Calling 能力**：调用订单、物流等外部工具
4. **结构化输出和 Pydantic Schema 约束能力**：确保 LLM 输出符合业务结构
5. **FastAPI 后端工程能力**：规范的后端 API 设计和实现
6. **前后端联调能力**：前端展示和后端处理的完整流程
7. **Bad Case / Eval 评估迭代能力**：系统化的质量评估和改进机制
8. **可写进简历、适合面试讲解的垂直业务型 MVP**

## 7. 和普通 AI 客服机器人的区别

| 维度 | 普通 AI 客服机器人 | CustomerOps Agent |
|------|-------------------|-------------------|
| 架构 | 单模型对话 | 多 Agent 协作编排 |
| 流程 | 问答式，无业务流程 | 完整业务流程：识别→检索→查询→判断→回复→质检 |
| 工具调用 | 无或简单 API 调用 | 复杂 Tool Calling：订单、物流、政策查询 |
| 输出格式 | 自由文本 | 结构化输出，Pydantic Schema 约束 |
| 知识库 | 简单 FAQ 匹配 | RAG 检索，支持复杂政策文档 |
| 质量保证 | 无 | QA Agent 质检，Bad Case 评估 |
| 可解释性 | 黑盒 | 每个 Agent 决策可追溯 |

## 8. 当前交付状态（M10.5 - Demo Release Ready）

**Release Version:** v1.0.0-demo  
**Release Date:** 2026-06-25  
**Status:** Demo Release Ready

| 能力 | 状态 | 说明 |
|------|------|------|
| RAG 知识库加载/切分 | ✅ | JSONL loader + character chunker |
| Baseline BM25 retriever | ✅ | 自实现 BM25，k1=1.5, b=0.75 |
| Optimized retriever | ✅ | query expansion + metadata boost + doc diversity |
| Retrieval evaluation | ✅ | Recall@1/3/5 + MRR on 122-case eval set |
| Node-based Agent workflow | ✅ | intent → route → RAG/tool → fallback |
| Mock logistics tool | ✅ | 模拟物流查询，不接真实 API |
| Fallback rules | ✅ | 10 条兜底规则 |
| Answer quality evaluation | ✅ | 6 指标评估，122-case 全量评测 |
| FastAPI API endpoint | ✅ | POST /api/agent/chat |
| Final release checklist | ✅ | docs/FINAL_RELEASE_CHECKLIST.md |
| Final acceptance report | ✅ | docs/FINAL_ACCEPTANCE_REPORT.md |
| Release tag | ✅ | v1.0.0-demo |
| 真实 LLM | ❌ | 使用 mock answer generator |
| 真实物流 API | ❌ | 使用 mock logistics tool |
| 真实订单系统 | ❌ | 无 |
| 前端 | ❌ | 冻结为 legacy demo |

### Final Metrics

**Retrieval (M6):**
- Optimized Recall@5: 98.36%
- Optimized MRR: 0.9108
- Optimized failed_cases: 2

**Answer (M9.5):**
- answer_pass_rate: 46.72%
- fallback_rate: 13.11%
- citation_hit_rate: 83.61%
- avg_relevance: 0.7566
- avg_groundedness: 0.8328
- avg_completeness: 0.5464

**API (M10):**
- pytest: 220 passed
- ruff: All checks passed
- API smoke: passed

### Known Limitations

1. **Mock Answer Generator** — Uses predefined response templates, not real LLM generation
2. **Mock Logistics Tool** — Simulates API responses, not connected to real logistics systems
3. **Answer Quality** — Pass rate (46.72%) indicates demo quality, not production-grade performance
4. **Rule-based Intent Recognition** — May have edge cases with complex or ambiguous queries
5. **No User Session Persistence** — Each request is stateless, no conversation history maintained
6. **No Production Deployment** — Designed for local development and demo purposes only
7. **Limited Domain Coverage** — Optimized for customs and logistics queries, may not generalize to other domains

### Optional Next Steps

- **M11: Real LLM Adapter** — Integrate with OpenAI/Claude/other LLM APIs, replace mock answer generator
- **M12: Real Logistics Adapter** — Connect to actual logistics tracking APIs, replace mock tool
- **Frontend Integration** — Connect React frontend to FastAPI backend, implement chat UI
- **Deployment** — Deploy to cloud platform (AWS/GCP/Azure), configure production environment

## 9. Goal 模式上下文规则

后续 Goal 模式**主要读取**以下核心文档：

| 文档 | 说明 |
|------|------|
| `docs/PROJECT_CONTEXT.md` | 项目背景和定位（本文件） |
| `docs/PRD.md` | 产品需求文档（MVP 范围、安全边界、非目标） |
| `docs/DESIGN.md` | 设计文档（页面、组件、用户流程） |
| `docs/TECHNICAL_SPEC.md` | 技术规格文档（技术栈、API 契约、Schema、目录结构、Agent 设计） |
| `docs/DEV_RULES.md` | 开发规则（架构、安全、禁止事项） |
| `docs/DEV_STATUS.md` | 开发状态（当前阶段、已完成、下一步） |
| `docs/CHANGELOG.md` | 变更记录 |

`docs/archive/` 目录仅作为**历史参考**，不作为默认上下文。除非需要回溯决策过程，否则不需要读取。
