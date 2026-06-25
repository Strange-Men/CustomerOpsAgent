# M9 Answer Workflow Optimization Report

## 1. Summary

M9 optimized the answer workflow to improve answer quality metrics. Key changes include splitting logistics intent into status/policy sub-intents, fixing route decision for policy queries, and improving mock answer evidence coverage.

## 2. M8 Baseline Metrics

| Metric | Value |
|--------|-------|
| total_cases | 122 |
| avg_relevance | 0.5967 |
| avg_groundedness | 0.6959 |
| avg_completeness | 0.3396 |
| citation_hit_rate | 56.56% |
| answer_pass_rate | 31.97% |
| fallback_rate | 40.16% |
| failed_cases | 83 |

## 3. M9 Optimized Metrics

| Metric | Value |
|--------|-------|
| total_cases | 122 |
| avg_relevance | 0.7418 |
| avg_groundedness | 0.8205 |
| avg_completeness | 0.5225 |
| citation_hit_rate | 81.15% |
| answer_pass_rate | 44.26% |
| fallback_rate | 15.57% |
| failed_cases | 68 |

## 4. Comparison Table

| Metric | M8 | M9 | Change | % Change |
|--------|-----|-----|--------|----------|
| avg_relevance | 0.5967 | 0.7418 | +0.1451 | +24.3% |
| avg_groundedness | 0.6959 | 0.8205 | +0.1246 | +17.9% |
| avg_completeness | 0.3396 | 0.5225 | +0.1829 | +53.9% |
| citation_hit_rate | 56.56% | 81.15% | +24.59% | +43.5% |
| answer_pass_rate | 31.97% | 44.26% | +12.29% | +38.4% |
| fallback_rate | 40.16% | 15.57% | -24.59% | -61.2% |
| failed_cases | 83 | 68 | -15 | -18.1% |

## 5. Failure Analysis

### Remaining Failed Cases (68 total)

**Category: Relevance < 0.6 (most common)**
- Some queries are classified with intent that doesn't match eval category
- Example: "包裹到美国一个月了还没收到" → intent=package, eval_category=logistics
- The relevance evaluator doesn't have package→package mapping

**Category: Completeness < 0.4**
- Mock answer template may not cover all expected_keywords
- Expected keywords are not available to the agent workflow

**Category: Groundedness < 0.7**
- Fallback responses get lower groundedness score
- Some queries still fall back to unknown_intent

### Top 5 Failed Cases

1. **eval_shipping_us_delay_001**: "我的包裹到美国已经快一个月了还没收到，怎么回事？"
   - Route: rag_knowledge_base, relevance=0.30 (category mismatch)

2. **eval_refund_eu_policy_001**: "欧洲买的商品退了货，退款多久能到账？"
   - Route: rag_knowledge_base, relevance=0.50

3. **eval_order_global_cancel_001**: "订单已经付款了但还没发货，可以取消吗？退款怎么算？"
   - Route: rag_knowledge_base, relevance=0.50, completeness=0.25

4. **eval_shipping_eu_delay_001**: "寄到德国的包裹已经快三周了还没到，比美国慢这么多吗？"
   - Route: fallback (unknown_intent)

5. **eval_shipping_us_en_001**: "I ordered from the US two weeks ago and my package still hasn't arrived."
   - Route: rag_knowledge_base, relevance=0.30 (category mismatch)

## 6. Remaining Issues

1. **Category mapping mismatch**: The eval category "logistics" includes both tracking and policy queries, but our intent classification distinguishes between them. Some policy queries get classified as "package" instead of "logistics".

2. **Relevance evaluator limitations**: The relevance evaluator uses a fixed category→intent mapping that doesn't account for the new intent split.

3. **Mock answer limitations**: Mock answers are template-based and may not cover all expected keywords. Real LLM integration would improve this.

4. **Unknown intent edge cases**: Some queries with unusual phrasing still trigger unknown_intent fallback.

## 7. Next Step

Based on M9 results:
- If answer quality is sufficient: proceed to M10 API integration
- If further optimization needed: refine intent recognition for edge cases
- Consider real LLM integration for better answer generation
