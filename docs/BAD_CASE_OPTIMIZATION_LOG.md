# Bad Case Optimization Log

## 1. 文档目的

本文档记录 CustomerOps Agent RAG 检索系统在 bad case 扩展和优化过程中的完整工作记录，包括：

- Bad cases 的来源和构建方法
- Baseline BM25 retriever 的典型失败类型
- Optimized retriever 的优化策略
- Baseline vs Optimized 在 full eval set 上的对比结果
- 仍失败 cases 的分析和后续优化方向

## 2. 数据集说明

### Seed Eval Set（M1）

- 数量：20 条
- 用途：早期链路验证，确保 loader → chunker → retriever → eval harness 全链路可用
- 局限：样本量过小，无法暴露 retriever 在多样场景下的真实表现

### Full Eval Set（M6）

- 数量：122 条
- 用途：更可信的评估，覆盖多 category / market / language / difficulty
- 构建方法：seed 20 条 + 新增 102 条扩展 bad cases

**Full Eval Set 分布：**

| 维度 | 分布 |
|------|------|
| category | logistics(18), customs(16), package(18), return(10), refund(10), exchange(10), address(10), order(10), payment(10), coupon(10) |
| market | US(37), EU(16), GLOBAL(69) |
| language | zh(82), en(40) |
| difficulty | easy(16), medium(75), hard(31) |

**问题类型覆盖：**

- 直问型："美国标准物流多久到？"
- 口语型："我的快递卡在一个地方好几天不动了咋办？"
- 模糊型："东西卡在海关了，要等多久才能出来？"
- 复合型："我想退货但包装坏了还能退吗？"
- 跨语言型：英文 query 对中文知识
- 市场限定型：US / EU / GLOBAL
- 边界型："我用了优惠券还能退款吗？"
- 多意图型："地址写错了还想取消订单怎么办？"
- 拼写变化型：shipping / delivery / parcel / package 混用
- 高频客服型：退款、物流、清关、包裹破损、支付失败

## 3. 优化策略摘要

M5 optimized retriever 采用以下策略（详见 `backend/app/rag/optimized_retriever.py`）：

1. **Query Expansion（查询扩展）**：跨语言同义词扩展，如 shipping → 物流、customs → 清关，共 12 组领域词典
2. **Synonym Expansion（同义词扩展）**：英文同义词映射，如 delivery → shipping、parcel → package
3. **Query Signal Inference（查询信号推断）**：从 query 文本推断 category / market / language，无需用户标注
4. **Metadata-Aware Boosting（元数据感知加权）**：基于推断信号对检索结果进行 category ×1.15、market ×1.10、language ×1.08、GLOBAL ×1.03 的可解释加权
5. **Doc-Level Diversity（文档级多样性）**：同一文档的多个 chunk 去重，避免单一文档霸占 top-k

## 4. Baseline 典型失败类型

### 失败类型 1：英文 query 对中文知识无法匹配

- **失败表现**：英文问题如 "My package has been stuck in customs for 10 days" 无法命中中文知识文档 `customs_global_delay_001`
- **原因**：BM25 基于词频匹配，英文 token 与中文 token 完全不重叠
- **优化策略**：query expansion 将 customs → 清关、delay → 延迟，扩展后命中中文文档

### 失败类型 2：多意图问题导致单一关键词偏移

- **失败表现**：问题如 "我想改地址但订单已经在处理了，是不是只能取消重新下单" 同时涉及 address 和 order，BM25 只命中其中一个
- **原因**：BM25 对整段 query 计算单一 score，多意图导致 score 分散
- **优化策略**：query expansion 覆盖多意图关键词，metadata boost 保留语义相近的文档

### 失败类型 3：物流 / 清关相互干扰

- **失败表现**：清关相关问题被物流文档拦截，因为两者共享"包裹""物流""延迟"等词
- **原因**：BM25 无法区分 logistics 和 customs 的语义边界
- **优化策略**：category 推断 + category boost，将 customs 相关文档加权

### 失败类型 4：refund / return / exchange 语义接近导致混淆

- **失败表现**：退款问题召回退货文档，换货问题召回退款文档
- **原因**：三者共享"退货""退款""商品"等高频词
- **优化策略**：category 推断区分 refund / return / exchange，精准 boost 对应文档

### 失败类型 5：package lost / damaged 混淆

- **失败表现**：丢件问题召回破损文档，破损问题召回丢件文档
- **原因**：两者都涉及"包裹""签收""理赔"
- **优化策略**：query expansion 区分 lost/丢失 vs damaged/破损，boost 对应文档

### 失败类型 6：market 限定信息未被充分利用

- **失败表现**：美国用户问物流，召回欧洲物流文档
- **原因**：BM25 不感知 market metadata
- **优化策略**：market 推断 + market boost，US 问题优先 US 文档，EU 问题优先 EU 文档

## 5. M4 Seed Failed Cases 回顾

### eval_customs_en_delay_001

- **问题**：My package has been stuck in customs for 10 days. Is this normal? What should I do?
- **expected_doc_ids**：`customs_global_delay_001`
- **Baseline 失败原因**：英文 customs/delay/stuck 无法匹配中文"清关延迟"，BM25 召回了英文的 `shipping_us_enquiry_001`
- **M5 修复方式**：query expansion 将 customs → 清关、stuck → 卡住/延迟，扩展后命中 `customs_global_delay_001`

### eval_shipping_customs_en_001

- **问题**：I'm in the EU and my order has been in transit for 3 weeks. The tracking says it's in customs. Should I be worried?
- **expected_doc_ids**：`shipping_eu_standard_001` + `customs_global_delay_001`
- **Baseline 失败原因**：英文 query 无法同时命中两个中文文档，BM25 只召回了 `refund_global_enquiry_001`
- **M5 修复方式**：query expansion 覆盖 transit/运输、customs/清关，EU market boost 加权，两个文档均被召回

## 6. Full Eval Baseline vs Optimized 结果

**数据集**：eval_cases_full.jsonl（122 条）

| 指标 | Baseline | Optimized | 提升 |
|------|----------|-----------|------|
| Recall@1 | 64.75% | 85.25% | +20.50pp |
| Recall@3 | 74.59% | 96.72% | +22.13pp |
| Recall@5 | 75.41% | 98.36% | +22.95pp |
| MRR | 0.6956 | 0.9108 | +0.2152 |
| Failed Cases | 30 | 2 | -28 |

**关键发现：**

- Optimized 在 full 122-case dataset 上 Recall@5 达到 98.36%，超过 85% 目标
- Baseline 在 full set 上表现明显弱于 seed set（75.41% vs 90%），说明 20 条 seed 过于简单
- Optimized 的 Recall@1 提升最显著（+20.50pp），说明 top-1 命中率大幅改善
- Failed cases 从 30 降至 2，修复率 93.3%

## 7. 仍失败 Cases 摘要

Optimized 仍失败的 2 个 case：

### full_logistics_us_express_001

- **question**：美国有没有快递加急服务？加急多久能到？
- **expected_doc_ids**：`shipping_us_enquiry_001`
- **retrieved_doc_ids**：`shipping_us_standard_001`, `package_global_lost_001`, `shipping_eu_standard_001`, ...
- **可能原因**：加急服务信息仅在英文文档 `shipping_us_enquiry_001` 中提及（Express shipping, 3-5 business days），但 query 中文"加急"扩展后更匹配 `shipping_us_standard_001` 的中文内容
- **后续优化方向**：增强 express/加急 的跨语言映射精度

### full_logistics_us_warehouse_001

- **question**：你们是从哪里发货的？从仓库到美国要多久？
- **expected_doc_ids**：`shipping_us_enquiry_001`
- **retrieved_doc_ids**：`shipping_us_standard_001`, `exchange_global_process_001`, `return_us_policy_001`, ...
- **可能原因**：仓库/发货 信息在英文文档中有 "overseas warehouse"，但中文 query 的"仓库"更匹配 `shipping_us_standard_001` 的"仓库发出后"表述
- **后续优化方向**：增强 warehouse/仓库 的同义词映射，或在中文知识文档中补充仓库信息

## 8. 简历指标口径提醒

- 最终简历数据应该以 full eval set（122 条）的结果为准，不直接使用 20 seed cases 的 100%
- 简历表述建议："在 122-case 评测集上，Optimized Retriever 相比 Baseline BM25 Recall@5 从 75.4% 提升到 98.4%，MRR 从 0.70 提升到 0.91"
- 注意：这是 Top-K doc hit rate 口径，不是 answer quality 口径
- 后续 answer quality evaluation（M8）完成后才能评估最终回答质量
