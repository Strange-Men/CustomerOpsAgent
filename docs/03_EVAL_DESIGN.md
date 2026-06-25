# CustomerOps Agent｜Evaluation Harness 设计

**日期**：2026-06-24
**适用阶段**：M4, M6, M8

---

## 一、Evaluation 分两层

```
第一层：Retrieval Evaluation（M4）
  └─ 衡量 retriever 的检索质量

第二层：Answer Evaluation（M8）
  └─ 衡量 answer generator 的回答质量
```

---

## 二、第一层：Retrieval Evaluation

### 指标定义

| 指标 | 定义 | 计算方式 |
|------|------|---------|
| Recall@1 | top-1 是否命中 expected_doc_ids | hit@1 / total_cases |
| Recall@3 | top-3 是否命中 expected_doc_ids | hit@3 / total_cases |
| Recall@5 | top-5 是否命中 expected_doc_ids（**核心指标**） | hit@5 / total_cases |
| MRR | 第一个命中的排名倒数 | mean(1/rank_of_first_hit) |

### 计算细节

- **expected_doc_ids**：eval case 中标注的正确文档 ID 列表
- **retrieved_doc_ids**：retriever 返回的 top-k 文档 ID 列表
- **命中判断**：retrieved_doc_ids 中是否有任意一个在 expected_doc_ids 中
- **Recall@5 对应简历**："top-5 知识召回准确率提升至 85%"

### 每个 Case 输出

```json
{
  "query": "包裹还没到怎么办",
  "expected_doc_ids": ["POL-LOGISTICS-001"],
  "retrieved_doc_ids": ["POL-LOGISTICS-001", "POL-RETURN-001", ...],
  "hit": true,
  "hit_rank": 1,
  "miss": []
}
```

---

## 三、第二层：Answer Evaluation

### 三大评估维度

对应简历："从三个维度自动批量化评估回答质量"

| 维度 | 定义 | 判断方式 |
|------|------|---------|
| **Relevance** | 回答是否切题 | 回答是否与问题相关，是否针对问题给出回应 |
| **Groundedness** | 回答是否基于知识库 | 回答内容是否基于 retrieved chunks，是否减少幻觉 |
| **Completeness** | 回答是否覆盖关键处理步骤 | 回答是否覆盖 expected_keywords 中的关键信息 |

### 辅助指标

| 指标 | 定义 | 计算方式 |
|------|------|---------|
| Citation Hit Rate | citations 中有多少命中 expected_doc_ids | hit_citations / total_citations |
| Keyword Coverage | expected_keywords 在回答中的覆盖率 | matched_keywords / total_keywords |
| Answer Pass Rate | 通过的 case 占比（**核心汇总指标**） | passed_cases / total_cases |

### 通过标准

一个 case 通过需要同时满足：
1. Relevance = true（回答切题）
2. Groundedness = true（回答基于知识库）
3. Completeness ≥ 50%（覆盖至少一半 expected_keywords）

### 注意事项

- 不要把 6 个指标都称为"6 个维度"
- 简历写的是"三个维度"：Relevance, Groundedness, Completeness
- Citation Hit Rate, Keyword Coverage, Answer Pass Rate 是辅助指标

---

## 四、防作弊约束

### 约束清单

| # | 约束 | 检查方式 |
|---|------|---------|
| 1 | retriever 不能读取 expected_doc_ids | retrieval_eval.py 调用 retriever 时只传 query |
| 2 | answer_generator 不能读取 expected_keywords | answer_generator 输入只有 query + retrieved chunks |
| 3 | optimized retriever 不能为 eval cases 写死规则 | random shuffle eval cases 后指标不应剧变 |
| 4 | baseline 和 optimized 必须跑同一份 eval set | 版本、条目、顺序一致 |
| 5 | eval report 必须输出失败 case | 不能只输出数字，必须输出 failed_cases 列表 |
| 6 | eval set 要固定版本 | 一旦生成不可随意修改，修改需记录原因 |
| 7 | 所有指标必须可复现 | 相同 eval set + 相同 config → 相同结果 |
| 8 | 测试数据不能泄露到 Prompt 组装环节 | prompt_builder 不能看到 eval case 的 expected 字段 |

### 评测隔离原则

```
retrieval_eval.py
  ├─ 输入：query（从 eval case 取）
  ├─ 调用：retriever.retrieve(query)  ← 只传 query，不传 expected
  └─ 对比：retrieved_doc_ids vs expected_doc_ids

answer_eval.py
  ├─ 输入：query + generated_answer + retrieved_chunks
  ├─ 不传：expected_keywords 给 answer_generator
  └─ 对比：answer 内容 vs expected_keywords
```

---

## 五、数据集设计

### seed_eval_cases.json（M1，20 条）

```json
{
  "query": "包裹还没到怎么办",
  "expected_doc_ids": ["POL-LOGISTICS-001"],
  "expected_keywords": ["物流", "配送", "查询", "延迟"],
  "category": "logistics",
  "difficulty": "easy",
  "market": "US",
  "language": "zh"
}
```

### bad_cases.json（M6，120+ 条）

在 seed 基础上增加：
- `bad_case_type`：检索失败 / 生成失败 / 格式失败
- `optimization_notes`：优化策略说明

### bad_case_optimization_log.md（M6）

每类问题的优化策略和效果记录。

---

## 六、评测执行顺序

```
M4：Retrieval Evaluation
  ├─ 跑 baseline BM25 retriever
  ├─ 计算 Recall@1/3/5, MRR
  └─ 保存 eval_results_baseline.json

M5：Optimized Retriever
  ├─ 跑 optimized retriever
  ├─ 计算 Recall@1/3/5, MRR
  └─ 保存 eval_results_optimized.json

M8：Answer Evaluation
  ├─ 跑 answer generator
  ├─ 计算 Relevance, Groundedness, Completeness
  ├─ 计算 Citation Hit Rate, Keyword Coverage, Answer Pass Rate
  └─ 保存 answer_eval_results.json

M10：EVAL_REPORT
  ├─ baseline vs optimized 对比
  ├─ 失败 case 分析
  └─ 优化策略总结
```
