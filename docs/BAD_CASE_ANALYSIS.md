# Bad Case Analysis — CustomerOpsAgent v1.3.0-quality

> 分析时间：2026-06-26
> 数据来源：`app.eval.answer_eval` 运行结果

## 1. 概述

| 阶段 | Failed Cases | Pass Rate |
|------|-------------|-----------|
| Baseline | 65 | 46.72% |
| After Optimization | 48 | 60.66% |
| 已修复 | 17 | +13.94 pp |

## 2. Bad Case 分类

### 2.1 已修复的 Bad Cases（17 条）

#### A. Relevance 修复（主要来源）
- **原因**：`_CATEGORY_INTENT_MAP` 映射不完整
- **修复**：扩展 category-to-intent 映射为多对多
- **影响**：relevance 分数从 0.30 提升到 0.50-1.00

#### B. Fallback 误触发修复
- **原因**：
  - intent 关键词覆盖不足 → unknown_intent fallback
  - sensitive_info_request 误判 → "pin" 匹配 "shipping"
  - needs_clarification 过度触发
- **修复**：
  - 新增 30+ intent 关键词
  - sensitive detection 改用 word-boundary
  - 新增 disambiguation 规则
- **影响**：fallback rate 从 13.11% 降到 0.82%

### 2.2 未修复的 Bad Cases（48 条）

#### A. Completeness 不足（主要瓶颈）
- **数量**：~42 条
- **表现**：回答中缺少 expected_keywords
- **典型 case**：
  - `eval_customs_en_delay_001`：expected "customs inspection, clearance delay, identity information, 15 business days"，answer 中无匹配
  - `eval_shipping_eu_delay_001`：expected "10-20个工作日, 英国脱欧, 海关抽检, 17track"，answer 返回 US 特定内容
- **根因**：
  - Retriever 返回的 evidence 不包含目标关键词
  - 知识库文档只有 14 篇，覆盖面有限
  - 部分 expected_keywords 需要跨文档组合才能覆盖

#### B. Citation Hit 不足
- **数量**：2 条
- **表现**：RAG route 但 citation_doc_ids 与 expected_doc_ids 无交集
- **根因**：retriever 返回了错误的文档

#### C. 剩余 Fallback Cases
- **数量**：1 条（`eval_package_lost_hard_001`）
- **表现**：多意图问题（签收但没收到 + 异常扣款），仍触发 missing_order_id
- **根因**：复杂多意图场景需要更智能的路由逻辑

## 3. 优先优化方向

### 3.1 短期（可行）
- ✅ 已完成：intent 关键词扩展
- ✅ 已完成：category 映射修复
- ✅ 已完成：sensitive detection 修复

### 3.2 中期（需要数据）
- 扩充知识库文档（当前 14 篇 → 目标 30+ 篇）
- 增加 EU/UK 特定物流文档
- 增加英文知识文档（当前仅 2/14）

### 3.3 长期（架构改进）
- 引入向量检索（embedding-based）替代纯 BM25
- 支持跨文档证据组合
- 多意图问题的智能拆分与路由

## 4. 原则

- **不改 eval 数据**：所有 122 条 eval cases 保持不变
- **不删失败用例**：48 条失败 case 如实记录
- **不伪造提升**：所有数据基于实际 eval 运行结果
- **区分优化来源**：
  - eval 代码修复（category map）≠ 回答模板优化
  - intent 关键词扩展 ≠ 知识库扩充
