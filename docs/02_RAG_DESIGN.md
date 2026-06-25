# CustomerOps Agent｜RAG 设计文档

**日期**：2026-06-24
**适用阶段**：M1-M9

---

## 一、RAG 流程

```
knowledge base (Markdown + metadata)
    ↓
loader (读取 .md + frontmatter)
    ↓
chunker (按标题/段落切分，保留 metadata)
    ↓
retriever (BM25 baseline → optimized)
    ↓
prompt builder (组装 retrieved chunks + query)
    ↓
answer generator (mock-first, rule-based)
    ↓
output: answer + citations (doc_id, chunk_id, source, score)
```

---

## 二、分层知识库 Schema

### 文档格式

Markdown + YAML frontmatter：

```yaml
---
doc_id: "POL-LOGISTICS-001"
title: "跨境物流配送政策"
category: "logistics"
market: "US"
language: "zh"
policy_type: "shipping"
priority: 1
source: "official_2026Q1"
---

（Markdown 正文）
```

### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| doc_id | string | 唯一标识 | "POL-LOGISTICS-001" |
| title | string | 文档标题 | "跨境物流配送政策" |
| category | string | 分类 | "logistics" / "customs" / "return" / "refund" / "exchange" / "payment" |
| market | string | 目标市场 | "US" / "EU" / "SEA" |
| language | string | 语言代码 | "zh" / "en" |
| policy_type | string | 政策类型 | "shipping" / "return" / "customs" / "payment" |
| priority | int | 优先级 | 1=高, 2=中, 3=低 |
| source | string | 来源 | "official_2026Q1" |

### 知识库覆盖（6 篇）

| 文档 | category | policy_type |
|------|----------|-------------|
| 跨境物流配送政策 | logistics | shipping |
| 清关指南 | customs | customs |
| 退货政策 | return | return |
| 退款流程 | refund | payment |
| 换货政策 | exchange | return |
| 支付问题解答 | payment | payment |

---

## 三、Chunking 策略

- **切分方式**：按标题 + 段落切分
- **chunk 大小**：100-500 tokens
- **metadata 传递**：每个 chunk 继承文档级全部 metadata（doc_id, category, market, language, policy_type, priority, source）
- **chunk 额外字段**：chunk_index（在文档中的序号）

### 切分规则

1. 按 `##` / `###` 标题切分为 sections
2. 每个 section 内按段落（空行分隔）切分为 chunks
3. 超长段落（>500 tokens）按句子边界二次切分
4. 短 chunks（<100 tokens）与相邻 chunks 合并

---

## 四、Retriever 设计

### Baseline：BM25

- 纯关键词匹配
- 可解释、可调试
- 作为 Recall@5 的基线数值

### Optimized：BM25 + 优化策略

```
Optimized Retriever:
  ├─ BM25（保留）
  ├─ + metadata filter（category, market, language, policy_type）
  ├─ + synonym expansion（同义词映射表）
  ├─ + query rewrite（规则化 query 改写）
  └─ + optional embedding adapter（mock/stub，保留接口）
```

### Metadata Filter

- **何时应用**：检索前，减少候选集
- **支持字段**：category, market, language, policy_type
- **language filter**：支持多语种检索，只返回指定语言的 chunks
- **组合方式**：AND 逻辑（同时满足所有 filter 条件）

### Synonym Expansion

- 同义词映射表（JSON 文件）
- 示例："包裹" → ["快递", "物流", "shipment"]
- 在 BM25 检索前扩展 query

### Query Rewrite

- 规则化改写（正则 + 映射表）
- 示例："我的快递还没到" → "物流 配送 延迟 查询"
- 不依赖 LLM

### Embedding Adapter

- 接口预留，MVP 用 stub
- stub 返回空结果，不影响 BM25 检索
- 接口：`def embed(text: str) -> list[float]`

---

## 五、Citations 设计

citations 一路保留以下信息：

| 字段 | 说明 |
|------|------|
| doc_id | 来源文档 ID |
| chunk_id | chunk 唯一标识 |
| source | 文档来源（from metadata） |
| score | 检索分数 |

### Citation 流程

1. retriever 返回 chunks with metadata
2. prompt builder 将 chunk 的 doc_id, source 注入 prompt
3. answer generator 在回答中标注 `[1]`, `[2]` 等引用
4. response 结构中附带 citations 列表

---

## 六、多语种知识库快速迁移

### 数据结构支持

- knowledge_base 文档必须包含 language 字段
- eval_cases 必须包含 language 字段
- 至少包含 zh / en 两种语言样例

### 检索接口支持

- retriever 支持 language filter
- metadata filter 自动支持新语种

### 迁移流程

1. 在 `backend/data/knowledge_base/{language}/` 下新增对应语种 .md 文件
2. frontmatter 中设置 language 字段
3. 新增对应的 eval cases（含 language 字段）
4. retriever 的 metadata filter 自动支持新语种，无需改代码

### 不做的事

- 不做复杂翻译服务
- 不做自动翻译
- 只做数据结构和检索接口支持

---

## 七、RAG 与 Agent Workflow 的关系

### 职责划分

| 层 | 职责 | 说明 |
|----|------|------|
| RAG（Retrieval） | 找证据 | 从知识库中检索与用户问题相关的 chunks |
| Agent Workflow | 做决策 | 判断用户意图、检查证据质量、组织回答、执行兜底 |

### 协作流程

```
User Query
    ↓
Agent Workflow: Intent Recognition（识别意图）
    ↓
RAG: Optimized Retrieval（检索相关 chunks）
    ↓
Agent Workflow: Evidence Check（检查证据是否充分）
    ↓
Agent Workflow: Prompt Builder + Answer Generator（组装回答）
    ↓
Agent Workflow: Citation Check（校验引用合法性）
    ↓
Agent Workflow: Fallback / Escalation（兜底或输出）
    ↓
Final Response
```

### 核心原则

- **RAG 负责找证据，Agent 负责判断和决策**
- **没有证据时不能强答**：Evidence Check 不通过时走 Fallback
- **RAG 是 Agent 的工具，不是 Agent 的全部**：Agent 还负责意图识别、引用校验、兜底策略
- **检索质量是基础**：M5 Optimized Retriever 的 Recall@5 = 98.36% 是 Agent 可靠工作的前提

### 详细设计

完整的 Agent Workflow 设计（Intent Recognition / Evidence Check / Citation Check / Fallback Rules）见 `docs/AGENT_WORKFLOW.md`。
