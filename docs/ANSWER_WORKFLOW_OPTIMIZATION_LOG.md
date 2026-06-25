# M9 Answer Workflow Optimization Log

## 1. Optimization Scope

M9 optimizes the answer workflow to improve answer quality metrics:

**Optimized:**
- Intent recognition: split logistics into logistics_status and logistics_policy
- Route decision: policy queries route to RAG, not logistics tool
- Fallback rules: missing_order_id only for real tracking queries
- Mock answer generation: improved evidence coverage from multiple chunks
- Citation selection: citations from retrieved chunks with deduplication

**Not optimized:**
- answer_eval.py evaluation logic (unchanged)
- eval_cases_full.jsonl dataset (unchanged)
- Real LLM API integration (not done)
- Real logistics API integration (not done)

## 2. M8 Baseline Answer Quality

| Metric | M8 Value |
|--------|----------|
| total_cases | 122 |
| avg_relevance | 0.5967 |
| avg_groundedness | 0.6959 |
| avg_completeness | 0.3396 |
| citation_hit_rate | 56.56% |
| answer_pass_rate | 31.97% |
| fallback_rate | 40.16% |
| failed_cases | 83 |

## 3. Failure Patterns

M8 identified these failure patterns:

1. **Policy queries wrongly requiring order_id**: Queries like "物流多久到" were classified as logistics and required order_id, triggering missing_order_id fallback.

2. **Customs/refund/order policy routed to fallback**: Policy queries that should use RAG knowledge base were incorrectly routed to the logistics tool.

3. **Logistics policy confused with logistics tracking**: No distinction between "物流状态查询" (needs order_id) and "物流政策查询" (uses RAG).

4. **Mock answer too short**: Only used top chunk content (200 chars), resulting in low keyword coverage.

5. **Citation hit rate insufficient**: Many queries fell back to fallback, losing citations.

6. **Unknown intent too broad**: Some valid queries were classified as unknown_intent.

## 4. M9 Changes

### Intent Recognition Changes

Split "logistics" intent into two sub-intents:

- **logistics_status**: Real logistics tracking queries (need order_id)
  - Keywords: "到哪了", "什么时候到", "查快递", "track my order"
  - Route: logistics tool (requires order_id)

- **logistics_policy**: Logistics policy/timeframe queries (use RAG)
  - Keywords: "物流多久", "配送时效", "运费", "shipping time"
  - Route: RAG knowledge base

Added disambiguation rules:
1. Package keywords (丢, 碎, 坏, 赔偿) override logistics_status
2. Policy keywords (取消, 退款, 退货) override logistics_status when no tracking keywords present

### Route Decision Changes

- `logistics_status` with order_id → logistics tool
- `logistics_status` without order_id → fallback missing_order_id
- `logistics_policy` → RAG knowledge base
- `customs/refund/return/order/payment/package/coupon` → RAG knowledge base
- `trace` → RAG knowledge base

### Fallback Rule Changes

- `missing_order_id` only triggers for `logistics_status` intent
- Not triggered for logistics_policy, refund, return, order policy queries

### Mock Answer Template Changes

- Uses content from top 3 chunks instead of just 1
- Includes up to 300 chars per chunk (was 200)
- Adds citation references in answer text
- Deduplicates similar content across chunks

### Citation Selection Changes

- Citations from retrieved chunks (unchanged behavior)
- Deduplication by doc_id in citation references

## 5. M9 Results

| Metric | M8 | M9 | Change |
|--------|-----|-----|--------|
| total_cases | 122 | 122 | - |
| avg_relevance | 0.5967 | 0.7418 | +0.1451 |
| avg_groundedness | 0.6959 | 0.8205 | +0.1246 |
| avg_completeness | 0.3396 | 0.5225 | +0.1829 |
| citation_hit_rate | 56.56% | 81.15% | +24.59% |
| answer_pass_rate | 31.97% | 44.26% | +12.29% |
| fallback_rate | 40.16% | 15.57% | -24.59% |
| failed_cases | 83 | 68 | -15 |

### Remaining Failed Cases

Some remaining failures are due to:

1. **Category mismatch**: Queries like "包裹到美国一个月了还没收到" are classified as "package" intent but eval category is "logistics", causing relevance < 0.6.

2. **Relevance evaluator limitations**: The relevance evaluator doesn't map "package" → {"package"}, so package queries routed to RAG don't get category match bonus.

3. **Edge cases**: Some queries have ambiguous intent that's hard to classify without real LLM understanding.

## 6. Remaining Risks

- Mock answer generator is not a real LLM; real LLM integration may produce different results
- Mock logistics tool is not a real API; real API integration may change behavior
- Answer quality metrics are rule-based evaluation, not human judgment
- Intent recognition is keyword-based; complex queries may be misclassified
- Route decision rules may overfit to the eval dataset
