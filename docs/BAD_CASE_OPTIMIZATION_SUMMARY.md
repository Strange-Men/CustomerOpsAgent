# Bad Case Optimization Summary — v1.4.0-badcase

## 优化前问题

v1.3.0-quality 完成后，系统存在以下不足：

1. **缺少结构化 Bad Case Bank**：122 条 answer eval cases 不能直接等同于 Bad Case
2. **缺少 case-level 失败分析**：没有逐条记录失败原因和优化策略
3. **缺少可验证的优化证据链**：没有 baseline → after 的结构化对比
4. **场景覆盖不完整**：缺少 out_of_scope 场景的评测用例

## 优化动作

### 1. 建立 Bad Case Bank（131 条）

- 新建 `backend/app/eval/bad_case_schema.py`：定义 BadCase 结构化 schema
- 新建 `backend/app/eval/bad_cases.jsonl`：131 条结构化 Bad Case
- 覆盖 11 个场景：customs / refund / logistics / payment / order / package / return / exchange / address / coupon / out_of_scope
- 每条 case 包含：case_id, user_query, scenario, expected_route, expected_intent, expected_behavior, required_evidence, failure_type, baseline_status, optimization_action, after_status

### 2. 实现 Bad Case Evaluation Harness

- 新建 `backend/app/eval/bad_case_eval.py`：自动化评测框架
- 功能：
  - 加载 bad_cases.jsonl
  - 调用 agent workflow（mock 模式，不调用真实 LLM）
  - 逐条判断：route 匹配、intent 匹配、citation 覆盖、下一步建议、out_of_scope 拒答
  - 输出整体指标和 case-level 报告
  - 支持命令行运行：`python -m app.eval.bad_case_eval`

### 3. Answer Composer 优化（基于 v1.3.0）

v1.3.0 已完成的优化包括：
- RAG 场景：直接结论 + 2-4 条原因/依据 + 可执行建议 + 引用提示
- 物流场景：有订单号返回 mock 状态，无订单号提示补充
- 退款场景：退款时间范围 + 支付方式影响说明
- 清关场景：海关查验、资料缺失、节假日等原因
- 支付失败：余额、风控、银行卡等原因
- 退换货：退货条件、时效、运费说明
- out_of_scope：不回答无关问题，引导客服相关问题

## 优化后指标

### Answer Eval（v1.3.0 → 当前）

| 指标 | Baseline (v1.3.0 前) | After (v1.3.0 后) | 变化 |
|------|----------------------|-------------------|------|
| Answer Pass Rate | 46.72% | 60.66% | +13.94pp (~30% relative) |
| Citation Hit Rate | 83.61% | 95.90% | +12.29pp |
| Fallback Rate | 13.11% | 0.82% | -12.29pp |
| Recall@5 | 90.00% | 90.00% | 持平 |

### Bad Case Eval（v1.4.0 新建）

| 指标 | 数值 |
|------|------|
| Total | 131 |
| Pass | 128 |
| Partial | 0 |
| Fail | 3 |
| Pass Rate | 97.71% |
| Citation Coverage | 97.54% |
| Fallback Rate | 7.63% |

## 与简历目标表述的对应关系

### ✅ 可以真实写的表述

1. "搭建分层知识库与 RAG 检索体系，优化召回策略与 Prompt 模板"
   - 证据：14 个知识文档、18 个 chunks、BM25+optimized retriever、Prompt 模板优化

2. "在自建评测集上 top-5 知识召回准确率达到 85%+"
   - 证据：Recall@5 = 90.00%（20 条 retrieval eval cases）

3. "设计 RAG Evaluation Harness 评测框架，从多个维度自动化量化评估回答质量"
   - 证据：answer_eval.py（relevance/groundedness/completeness/citation）、retrieval_eval.py（Recall@1/3/5/MRR）、bad_case_eval.py（route/intent/citation/next_step）

4. "累计构建 131 条典型客服 Bad Case Bank，覆盖清关、退款、物流、支付、退换货等 11 个高频场景"
   - 证据：bad_cases.jsonl（131 条）、bad_case_eval.py 运行结果

5. "高频咨询场景回答合格率相对提升约 30%"
   - 证据：answer pass rate 46.72% → 60.66%，相对提升 (60.66-46.72)/46.72 ≈ 29.8%

### ⚠️ 需要注意的表述

- "累计优化 120+ 典型问题 Bad Case" — 需要区分：
  - Bad Case Bank 总数 = 131 ✅
  - 结构性通过率（bad_case_eval）= 97.71%（128/131）
  - 内容质量通过率（answer_eval）= 60.66%（74/122）
  - 建议表述："累计构建 131 条典型客服 Bad Case Bank，结构性通过率 97.71%，内容质量通过率 60.66%"

### ❌ 不能写的表述

- "生产级系统" — 这是 demo/学习项目
- "接入真实物流 API" — 使用 mock logistics tool
- "真实 LLM 回答" — mock 模式下为模板回答
- "所有 Bad Case 都已优化通过" — 3 条仍有 route/intent 失败

## 文件清单

| 文件 | 说明 |
|------|------|
| `backend/app/eval/bad_case_schema.py` | BadCase 结构化 schema |
| `backend/app/eval/bad_cases.jsonl` | 131 条 Bad Case 数据 |
| `backend/app/eval/bad_case_eval.py` | Bad Case 评测框架 |
| `docs/BAD_CASE_BANK_REPORT.md` | Bad Case Bank 详细报告 |
| `docs/BAD_CASE_OPTIMIZATION_SUMMARY.md` | 本文档 |
