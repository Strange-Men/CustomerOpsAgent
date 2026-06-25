# CustomerOpsAgent Lightweight Agent Workflow

**日期**：2026-06-25
**适用阶段**：M7+

---

## 1. 为什么当前项目需要 Agent Workflow

M1-M6 已完成 RAG retrieval + evaluation harness，Optimized Retriever 在 122-case 全量评测集上 Recall@5 达到 98.36%。但客服 Agent 不应只是"检索文档"：

1. **客服场景需要先理解用户意图**。用户说"我的包裹还没到"和"怎么退货"，检索策略、prompt 模板、兜底逻辑完全不同。
2. **检索结果需要经过证据检查**。top score 过低、retrieved chunks 与 intent 不匹配、多意图冲突——这些情况不能强行回答。
3. **最终回答必须带引用**。客服回答如果不能追溯到知识库原文，就是不可信的。
4. **需要兜底机制**。知识库外的问题、真实订单状态查询、用户情绪激烈——这些场景必须有 fallback，不能编造。

这层 Agent Workflow 让项目从"RAG demo"升级为"轻量客服 Agent 系统"，更符合简历里的"客服 Agent 能力体系"表述。

---

## 2. Agent Workflow 总览

### M7 实现的节点式流程

```
Start Node
    ↓
Variable Extraction Node（变量提取）
    ↓
Intent Recognition Node（意图识别）
    ↓
Route Decision Node（路由决策）
    ├── Logistics Tool Route（物流工具路由）
    │   ↓
    │   Mock Logistics Plugin（模拟物流插件）
    │   ├── Tool Success → Friendly Logistics Reply
    │   └── Tool Failed → Fallback / Escalation
    │
    ├── RAG Knowledge Base Route（知识库路由）
    │   ↓
    │   Optimized RAG Retrieval（优化检索）
    │   ↓
    │   Evidence Check（证据检查）
    │   ↓
    │   Prompt Builder（提示构建）
    │   ↓
    │   Mock Answer Generator（模拟回答生成）
    │   ↓
    │   Citation Check（引用校验）
    │   └── No Evidence → Fallback / Escalation
    │
    └── Other Intent → Fallback / Escalation
    ↓
End Node（返回结果）
```

**关键约束**：这不是复杂多 Agent 编排，不是 LangGraph，不是 6 Agent 工单系统。这是围绕 RAG 的单链路轻量工作流，每个节点是规则驱动的函数调用。

### 节点说明

| 节点 | 说明 | 实现文件 |
|------|------|---------|
| Start Node | 接收 user_query、可选 order_id、可选 conversation_history | `workflow.py` |
| Variable Extraction Node | 用正则提取订单号 | `entity_extractor.py` |
| Intent Recognition Node | 规则版意图识别，不调用真实 LLM | `intent_recognizer.py` |
| Route Decision Node | 根据 route_intent 决定路由 | `workflow.py` |
| Logistics Tool Route | 使用 mock logistics tool，不接真实 API | `logistics_tool.py` |
| RAG Knowledge Base Route | 使用 optimized retriever 检索知识库 | `workflow.py` |
| Evidence Check | 检查检索结果质量和置信度 | `fallback_rules.py` |
| Prompt Builder | 构建结构化 prompt，不调用 LLM | `prompt_builder.py` |
| Mock Answer Generator | 模板化回答生成，不调用真实 LLM | `mock_answer_generator.py` |
| Citation Check | 校验 citation 来自 retrieved chunks | `workflow.py` |
| Fallback Rules | 覆盖多种兜底场景 | `fallback_rules.py` |
| End Node | 返回 AgentResponse | `workflow.py` |

---

## 3. Intent Recognition 意图识别

### 支持的 Intent（M9 更新）

| Intent | 说明 | 示例 Query |
|--------|------|-----------|
| `logistics_status` | 物流状态查询（需订单号） | "快递到哪了"、"track my order" |
| `logistics_policy` | 物流政策/时效查询（走 RAG） | "物流多久到"、"shipping time" |
| `customs` | 清关 | "清关要多久"、"customs clearance" |
| `return` | 退货 | "怎么退货"、"return policy" |
| `refund` | 退款 | "退款多久到账"、"refund status" |
| `exchange` | 换货 | "可以换颜色吗"、"exchange item" |
| `address` | 地址修改 | "改收货地址"、"change address" |
| `order` | 订单查询 | "订单状态"、"order status" |
| `payment` | 支付问题 | "付款失败"、"payment failed" |
| `package` | 包裹问题 | "包裹破损"、"package lost" |
| `coupon` | 优惠券 | "优惠码不能用"、"coupon not working" |
| `unknown` | 无法识别 | 非客服问题、语言无法判断 |

### M9 关键改进

- **物流意图拆分**：`logistics_status`（需订单号）vs `logistics_policy`（走 RAG）
- **消歧规则**：包裹问题关键词（丢、碎、坏）优先于物流状态；政策关键词（取消、退款）优先于物流状态
- **missing_order_id 只适用于真实物流状态查询**，不适用于政策查询

### 实现策略

- **M7 先用规则实现，不接 LLM**
- 基于 query 中的关键词 / category signals 判断 intent
- 复用 M5 `optimized_retriever.py` 中的 `infer_query_signals()` 推断 category
- intent 用途：
  - 辅助检索（metadata filter 优先匹配对应 category）
  - prompt 选择（不同 intent 用不同 prompt 模板）
  - fallback 判断（unknown intent 不能强行回答）
- `unknown` intent 直接走 fallback，不进入 answer generation

### 设计原则

- 宁可返回 `unknown`，不可错判 intent 后编造回答
- 同义词覆盖（中英文、口语表达）
- 多 intent 时标记为 `multi`，交由 Evidence Check 处理

---

## 4. Evidence Check 证据检查

### 检查项

| # | 检查项 | 说明 | 不通过处理 |
|---|--------|------|-----------|
| 1 | retrieved_chunks 非空 | 检索是否有结果 | → Fallback: "知识库无相关内容" |
| 2 | top score ≥ 阈值 | 最高分是否达到可信阈值 | → Fallback: "需要人工确认" |
| 3 | Top-K 含高相关 category | 是否有与 intent 匹配的 category | → 降低置信度 |
| 4 | citations 可用 | 至少一个 chunk 有 doc_id + source | → Fallback: "无法提供引用来源" |
| 5 | 覆盖用户 intent | retrieved content 是否与 intent 相关 | → Fallback: "问题超出当前知识库覆盖" |
| 6 | 无多意图冲突 | 是否同时命中多个不相关 category | → 先确认用户最想处理的问题 |

### 设计原则

- **证据不足时，不允许编造回答**
- 检查失败走 Fallback，不进入 Answer Generation
- 阈值可配置，M7 先用经验值

---

## 5. Citation Check 引用校验

### 校验规则

1. **最终回答必须带 citation**。每个核心断言至少引用一个 doc_id。
2. **不能引用不存在的 doc_id**。answer 中的引用必须在 retrieved_chunks 中存在。
3. **没有 citation 不能返回正式客服答案**。无引用回答只允许出现在 fallback 场景。
4. **citation 来源必须来自 retrieved chunks**。不能凭空编造来源。

### Citation 结构

```json
{
  "doc_id": "POL-LOGISTICS-001",
  "title": "跨境物流配送政策",
  "source": "official_2026Q1",
  "chunk_id": "POL-LOGISTICS-001::chunk_001",
  "score": 8.5
}
```

### 设计原则

- Citation 是客服回答可信度的底线
- 宁可少回答，不可无引用
- M7 先实现 mock citation（从 retrieved chunks 直接提取），不做真实引用格式化

---

## 6. Fallback / Escalation 兜底规则

| # | 触发条件 | 响应策略 | 示例话术 |
|---|---------|---------|---------|
| 1 | 检索无结果 | 返回"当前知识库无法确认"，建议转人工 | "抱歉，当前知识库中未找到相关信息，建议您联系人工客服获取帮助。" |
| 2 | Top score 太低 | 不强答，提示需要人工确认 | "您的问题我找到了一些相关信息，但置信度不够高，建议与人工客服确认。" |
| 3 | Citation 缺失 | 不输出最终客服答复 | "抱歉，我无法提供有依据的回答，请联系人工客服。" |
| 4 | 用户询问真实订单状态 | 提示需要订单号或人工系统查询 | "订单状态查询需要您的订单号，建议您登录账户查看或联系人工客服。" |
| 5 | 知识库外问题 | 说明当前客服知识库不覆盖 | "您的问题超出了当前客服知识库的覆盖范围，建议您联系人工客服。" |
| 6 | 多意图冲突 | 先确认用户最想处理的问题 | "您提到了退货和物流两个问题，请问您最想处理哪一个？" |
| 7 | 政策风险问题 | 只基于知识库回答，不承诺额外赔偿、具体到账时间或平台外政策 | "退款到账时间以支付平台实际处理为准，我无法承诺具体日期。" |
| 8 | 用户情绪激烈 / 投诉 | 给安抚话术并建议转人工 | "非常抱歉给您带来不好的体验，我理解您的心情。建议您联系人工客服，我们会优先为您处理。" |
| 9 | 涉及隐私或支付敏感信息 | 不要求用户提供完整银行卡、密码、验证码等 | "为了您的账户安全，请不要在对话中提供银行卡号、密码或验证码。" |
| 10 | 低置信度回答 | 优先解释限制，而不是编造 | "根据知识库中的信息，以下内容仅供参考，具体以实际政策为准。" |

### 设计原则

- Fallback 不是失败，是安全机制
- 宁可转人工，不可编造
- 话术要友好、专业、不推卸
- M7 先实现规则匹配，不做情绪识别 LLM

---

## 7. M7 开发范围

### M7 应实现

| 模块 | 文件 | 说明 |
|------|------|------|
| 意图识别 | `backend/app/agent/intent_recognizer.py` | 规则驱动，基于关键词 + category signals |
| Prompt 构建 | `backend/app/agent/prompt_builder.py` | 根据 intent + retrieved chunks 组装结构化 prompt |
| Mock 回答生成 | `backend/app/agent/mock_answer_generator.py` | 规则模板生成客服回答，带 citation 标记 |
| 兜底规则 | `backend/app/agent/fallback_rules.py` | 10 条 fallback 规则的规则引擎 |
| 引用校验 | `backend/app/agent/citation_checker.py` | 校验 answer 中的 citation 合法性 |
| Workflow 编排 | `backend/app/agent/workflow.py` | 串联以上模块的主流程 |
| 测试 | `backend/tests/test_agent_workflow.py` | 覆盖各节点 + 集成测试 |

### M7 不做

| 禁止项 | 原因 |
|--------|------|
| LLM API 调用 | mock-first，M7 用规则模板 |
| FastAPI API 层 | M9 才做 |
| 前端 | 冻结 |
| LangGraph | 单链路工作流不需要 |
| 多 Agent 编排 | 轻量 Agent，不是 6 Agent 系统 |
| 真实订单查询 | mock data 足够 |
| 真实物流 API | mock data 足够 |
| 情绪识别（LLM） | M7 用关键词规则 |

---

## 8. 设计原则总结

1. **Rule-first**：M7 全部用规则实现，不接 LLM，确保可测试、可解释。
2. **Fail-safe**：每个节点的失败都走 fallback，不编造。
3. **Citation-required**：没有引用的回答不是客服回答。
4. **Single-pipeline**：单链路工作流，不是多 Agent 编排。
5. **Intent-aware**：不同 intent 用不同策略，不一视同仁。
