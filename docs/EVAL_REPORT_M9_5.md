# M9.5 Answer Quality Polish Report

## 1. Overview

M9.5 is a targeted optimization pass on top of M9, focusing on fixing remaining failure patterns in the answer workflow without major restructuring.

## 2. M9 Baseline Metrics

| Metric | M9 Value |
|--------|----------|
| total_cases | 122 |
| avg_relevance | 0.7418 |
| avg_groundedness | 0.8205 |
| avg_completeness | 0.5225 |
| citation_hit_rate | 81.15% |
| answer_pass_rate | 44.26% |
| fallback_rate | 15.57% |
| failed_cases | 68 |

## 3. M9.5 Metrics

| Metric | M9.5 Value |
|--------|-----------|
| total_cases | 122 |
| avg_relevance | 0.7566 |
| avg_groundedness | 0.8328 |
| avg_completeness | 0.5464 |
| citation_hit_rate | 83.61% |
| answer_pass_rate | 46.72% |
| fallback_rate | 13.11% |
| failed_cases | 65 |

## 4. Comparison Table

| Metric | M9 | M9.5 | Change |
|--------|-----|------|--------|
| avg_relevance | 0.7418 | 0.7566 | +0.0148 |
| avg_groundedness | 0.8205 | 0.8328 | +0.0123 |
| avg_completeness | 0.5225 | 0.5464 | +0.0239 |
| citation_hit_rate | 81.15% | 83.61% | +2.46pp |
| answer_pass_rate | 44.26% | 46.72% | +2.46pp |
| fallback_rate | 15.57% | 13.11% | -2.46pp |
| failed_cases | 68 | 65 | -3 |

All metrics improved. Fallback rate decreased by 2.46 percentage points, and 3 additional cases now pass.

## 5. Fixed Failure Patterns

### 5.1 Shipping Delay vs Package Disambiguation

**Problem**: Queries like "我的包裹到美国已经快一个月了还没收到" were classified as `package` intent because "包裹" and "没收到" triggered package keywords. The correct classification is `logistics_policy` (shipping delay, not package lost).

**Fix**: Added delay-aware disambiguation rules in `intent_recognizer.py`:
- Added shipping delay keywords to `logistics_policy` (e.g., "还没到", "快一个月", "hasn't arrived", "taking too long")
- Added Rule 1b: when both `logistics_status` and `package` match, delay indicators (time expressions + "not received") route to `logistics_policy` instead of `package`
- Damage/loss indicators ("丢", "破损", "damaged", "lost") still correctly route to `package`

**Result**: Shipping delay queries now route to RAG knowledge base instead of being misclassified as package issues.

### 5.2 English Shipping Delay Routing

**Problem**: English queries like "I ordered from the US two weeks ago and my package still hasn't arrived" were not recognized as logistics delay queries.

**Fix**: Added English shipping delay keywords to `logistics_policy`:
- "hasn't arrived", "has not arrived", "still hasn't arrived"
- "not arrived", "taking too long", "shipping delay", "delivery delay"
- "two weeks", "three weeks", "a month"

**Result**: English shipping delay queries now correctly route to RAG.

### 5.3 Refund Policy Relevance

**Problem**: "欧洲买的商品退了货，退款多久能到账？" was classified as `logistics_policy` instead of `refund` because "多久能到" (a logistics keyword) matched as a substring of "退款多久能到账".

**Fix**: Added Rule 1b for refund vs logistics_policy disambiguation:
- When both `refund` and `logistics_policy` match, and refund-specific keywords ("退款", "退钱") are present, `refund` takes precedence.

**Result**: Refund queries with logistics-like substrings now correctly classify as `refund`.

### 5.4 Multi-intent Order Cancel + Refund

**Problem**: Queries like "订单已经付款了但还没发货，可以取消吗？退款怎么算？" had low completeness because the answer template only covered one aspect.

**Fix**: Updated `mock_answer_generator.py`:
- Added multi-intent detection in the `order` template: when the query also contains refund keywords, the answer covers both order cancellation and refund processing
- Updated the `refund` template to include more comprehensive refund processing information
- Increased `max_chars_per_chunk` from 300 to 400 for better evidence extraction

**Result**: Multi-intent queries get more comprehensive answers covering both aspects.

### 5.5 Citation Diversity

**Problem**: Citations could all come from the same doc_id, reducing information diversity.

**Fix**: Updated `_build_citations()` in `mock_answer_generator.py`:
- First pass: one citation per unique doc_id (preserving order)
- Second pass: fill remaining slots with any chunks
- Ensures diverse doc_ids in citations when available

**Result**: Citations now prefer diverse sources from different documents.

### 5.6 Colloquial Package Keywords

**Problem**: "包裹丢了怎么办" (colloquial) didn't match "丢失" (formal), resulting in `unknown` intent.

**Fix**: Added colloquial variants to `package` keywords:
- "丢了", "包裹丢了", "找不到包裹", "包裹找不到"

**Result**: Colloquial package loss expressions are now correctly recognized.

## 6. Remaining Failed Cases (65)

Some cases still fail due to:

1. **Category mismatch in eval dataset**: Shipping delay cases (eval_shipping_us_delay_001, eval_shipping_eu_delay_001, eval_shipping_us_en_001) have `expected_category: "package"` in the eval dataset, but the correct intent is `logistics_policy`. The answer_eval.py relevance evaluator caps relevance at 0.30 when the agent's category doesn't match the expected category, even though the answer is factually correct and well-grounded.

2. **Multi-intent completeness**: Order cancel + refund cases still have lower completeness because the mock answer template can't dynamically extract all relevant keywords from evidence.

3. **Edge cases**: Some queries with ambiguous intent or unusual phrasing still fall through the rule-based classifier.

## 7. Remaining Limitations

1. **Mock answer generator**: Still template-based, not a real LLM. Real LLM integration would produce more natural and comprehensive answers.

2. **Mock logistics tool**: Still returns hardcoded data, not connected to real logistics APIs.

3. **Rule-based answer eval**: The relevance evaluator uses category matching which can penalize correctly-classified intents when the eval dataset has incorrect category labels.

4. **Intent recognition is keyword-based**: Complex queries with unusual phrasing may still be misclassified. A real LLM-based intent classifier would handle these better.

## 8. Next Step Recommendation

Based on M9.5 results:

- **If the goal is to demonstrate the system**: M9.5 results (46.72% pass rate, 13.11% fallback) are sufficient to show a working customer service agent with RAG, intent recognition, and evaluation harness.
- **If higher pass rate is needed**: Consider M9.6 to fix eval dataset category labels for shipping delay cases, which would improve relevance scores without changing the agent logic.
- **If moving to production**: Enter M10 (API integration) to connect real LLM for answer generation and real logistics API for tracking.
