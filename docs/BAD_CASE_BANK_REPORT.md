# Bad Case Bank Report — v1.4.0-badcase

## Overview

v1.4.0 建立了 **131 条典型客服 Bad Case Bank**，覆盖跨境电商客服全部高频场景。
每条 case 都有结构化字段，包括场景分类、预期路由、预期行为、失败类型、优化动作和修复状态。

## Bad Case Bank 总数

| 指标 | 数值 |
|------|------|
| Total Bad Cases | 131 |
| Scenarios Covered | 11 |
| Evaluation Harness | `bad_case_eval.py` |
| Schema Definition | `bad_case_schema.py` |
| Data File | `bad_cases.jsonl` |

## 场景分布

| Scenario | Count | Description |
|----------|-------|-------------|
| logistics | 15 | 物流配送、时效、追踪 |
| customs | 15 | 清关延迟、海关抽检、关税 |
| package | 15 | 包裹破损、丢失、理赔 |
| mixed | 15 | 多意图复合场景 |
| payment | 10 | 支付失败、风控、支付方式 |
| coupon | 10 | 优惠券使用、过期、叠加 |
| exchange | 9 | 换货流程、时效、运费 |
| address | 9 | 地址修改、发货前后差异 |
| out_of_scope | 9 | 超出服务范围的非客服问题 |
| return | 8 | 退货条件、流程、运费 |
| refund | 8 | 退款时间、到账、异常 |
| order | 8 | 订单取消、优惠券退回 |

## Failure Type 分布

| Failure Type | Count | 说明 |
|-------------|-------|------|
| incomplete_answer | 122 | 回答不完整，缺少关键信息 |
| missing_next_step | 122 | 缺少下一步操作建议 |
| retrieval_miss | 122 | 可能检索不到相关知识 |
| missing_citation | 122 | RAG 场景可能缺少引用 |
| route_error | 31 | 复杂场景可能路由错误 |
| out_of_scope_error | 9 | 超范围问题可能错误回答 |
| over_fallback | 9 | 超范围问题可能过度兜底 |

## Bad Case Evaluation 结果

运行 `python -m app.eval.bad_case_eval` 得到以下结果：

| 指标 | 数值 |
|------|------|
| Total | 131 |
| Pass | 128 |
| Partial | 0 |
| Fail | 3 |
| Pass Rate | 97.71% |
| Citation Coverage | 97.54% |
| Fallback Rate | 7.63% |

### 场景通过率

| Scenario | Count | Pass Rate |
|----------|-------|-----------|
| address | 9 | 100.00% |
| coupon | 10 | 100.00% |
| customs | 15 | 100.00% |
| exchange | 9 | 88.89% |
| logistics | 15 | 86.67% |
| mixed | 15 | 100.00% |
| order | 8 | 100.00% |
| out_of_scope | 9 | 100.00% |
| package | 15 | 100.00% |
| payment | 10 | 100.00% |
| refund | 8 | 100.00% |
| return | 8 | 100.00% |

### 失败案例（3 条）

1. **full_logistics_us_parcel_001** — "My parcel hasn't moved for a week"
   - 问题：系统路由到 logistics_tool，预期为 rag_knowledge_base
   - 原因：含物流追踪关键词，被识别为 logistics_status

2. **full_exchange_global_color_001** — "Can I exchange for a different color"
   - 问题：系统路由到 fallback/trace，预期为 rag_knowledge_base/exchange
   - 原因：intent recognition 中 trace 和 exchange 关键词重叠

3. **full_variant_shipment_001** — "The shipment status hasn't changed in 12 days"
   - 问题：系统路由到 logistics_tool，预期为 rag_knowledge_base
   - 原因：含物流状态关键词，被识别为 logistics_status

## 典型 Bad Case 示例

### 示例 1：清关延迟（customs）
```
case_id: eval_customs_global_delay_001
user_query: 物流信息显示清关中已经两周了，是不是被海关扣了？
expected_route: rag_knowledge_base
expected_behavior: 回答应包含清关延迟原因（海关抽检、资料缺失、节假日等）、预计时间范围、建议操作
failure_type: incomplete_answer, missing_next_step, retrieval_miss, missing_citation
```

### 示例 2：退款到账（refund）
```
case_id: eval_refund_eu_policy_001
user_query: 欧洲买的商品退了货，退款多久能到账？
expected_route: rag_knowledge_base
expected_behavior: 回答应包含退款时间范围、支付方式影响、建议提供订单号或支付方式
failure_type: incomplete_answer, missing_next_step, retrieval_miss, missing_citation
```

### 示例 3：支付失败（payment）
```
case_id: eval_payment_global_failure_001
user_query: 付款的时候一直提示支付失败，换了好几张卡都不行
expected_route: rag_knowledge_base
expected_behavior: 回答应说明支付失败原因（余额、风控、银行卡等）、建议换卡或联系银行
failure_type: incomplete_answer, missing_next_step, retrieval_miss, missing_citation
```

### 示例 4：退换货（return + exchange）
```
case_id: eval_return_exchange_hard_001
user_query: 收到的衣服颜色和图片差太多了，我想退货，但如果换货更快的话我也能接受换货，怎么选？
expected_route: rag_knowledge_base
expected_behavior: 回应覆盖退货和换货两种方案，分别说明时效和流程
failure_type: incomplete_answer, missing_next_step, retrieval_miss, missing_citation, route_error
```

### 示例 5：超范围问题（out_of_scope）
```
case_id: bc_out_of_scope_essay_001
user_query: 你能帮我写一篇关于人工智能的论文吗？
expected_route: fallback
expected_behavior: 不回答论文写作问题，说明只支持跨境电商客服，引导输入订单/物流/退款等问题
failure_type: out_of_scope_error, over_fallback
```

## 结论

- ✅ 累计构建 **131 条典型客服 Bad Case Bank**
- ✅ 覆盖 customs / refund / logistics / payment / order / package / return / exchange / address / coupon / out_of_scope 全部 11 个场景
- ✅ 每条 case 都有结构化字段（case_id, user_query, scenario, expected_route, expected_behavior, failure_type, optimization_action, after_status）
- ✅ 实现了 `bad_case_eval.py` 评测框架，可自动运行并输出 case-level 报告
- ✅ Bad Case Bank 建立于 v1.4.0，用于后续持续追踪
- ✅ 整体 answer eval 使用 v1.3.0 前后指标对比（pass rate 46.72% → 60.66%，相对提升约 30%）
