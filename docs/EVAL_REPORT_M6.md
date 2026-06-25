# M6 Retrieval Evaluation Report

## 1. 数据集说明

| 数据集 | 文件 | 数量 | 用途 |
|--------|------|------|------|
| Seed Eval Set | `eval_cases_seed.jsonl` | 20 | 早期链路验证 |
| Full Eval Set | `eval_cases_full.jsonl` | 122 | 可信评估 |

## 2. Full Dataset 分布

### Category Distribution

| Category | Count |
|----------|-------|
| logistics | 18 |
| customs | 16 |
| package | 18 |
| return | 10 |
| refund | 10 |
| exchange | 10 |
| address | 10 |
| order | 10 |
| payment | 10 |
| coupon | 10 |
| **Total** | **122** |

### Market Distribution

| Market | Count |
|--------|-------|
| US | 37 |
| EU | 16 |
| GLOBAL | 69 |
| **Total** | **122** |

### Language Distribution

| Language | Count |
|----------|-------|
| zh | 82 |
| en | 40 |
| **Total** | **122** |

### Difficulty Distribution

| Difficulty | Count |
|------------|-------|
| easy | 16 |
| medium | 75 |
| hard | 31 |
| **Total** | **122** |

## 3. Baseline vs Optimized 指标

### Full Eval Set（122 cases）

| 指标 | Baseline | Optimized | 提升 |
|------|----------|-----------|------|
| Recall@1 | 64.75% | 85.25% | +20.50pp |
| Recall@3 | 74.59% | 96.72% | +22.13pp |
| Recall@5 | 75.41% | 98.36% | +22.95pp |
| MRR | 0.6956 | 0.9108 | +0.2152 |
| Failed Cases | 30 | 2 | -28 |

### Seed Eval Set（20 cases，M5 数据）

| 指标 | Baseline | Optimized | 提升 |
|------|----------|-----------|------|
| Recall@1 | 70.00% | 85.00% | +15.00pp |
| Recall@3 | 85.00% | 100.00% | +15.00pp |
| Recall@5 | 90.00% | 100.00% | +10.00pp |
| MRR | 0.7850 | 0.9167 | +0.1317 |
| Failed Cases | 2 | 0 | -2 |

## 4. 结论

1. **Optimized Retriever 在 full dataset 上达到 Recall@5 = 98.36%，超过 85% 目标** ✓
2. **Recall@1 从 64.75% 提升到 85.25%（+20.50pp）**，Top-1 命中率大幅改善 ✓
3. **MRR 从 0.6956 提升到 0.9108（+0.2152）**，排序质量显著提升 ✓
4. **Failed cases 从 30 降至 2**，修复率 93.3% ✓
5. **Baseline 在 full set 上明显弱于 seed set**（Recall@5: 75.41% vs 90%），说明 20 条 seed set 过于简单，full set 更能暴露真实问题

### 简历表述建议

> 在自建 122-case 跨境电商客服评测集上，Optimized Retriever（query expansion + metadata-aware boosting）相比 Baseline BM25，Recall@5 从 75.4% 提升到 98.4%（+23.0pp），MRR 从 0.70 提升到 0.91（+0.21），Top-5 失败用例从 30 降至 2。

## 5. 注意事项

1. **这是自建评测集结果**，非公开 benchmark，不可直接与论文或其他项目对比
2. **指标是 Top-K doc hit rate 口径**：衡量的是"检索结果中是否包含正确文档"，不是"回答是否正确"
3. **Answer quality evaluation 还未完成**：后续 M8 将实现 answer evaluation，评估回答的相关性、完整性、可追溯性
4. **知识库规模较小**（14 篇文档）：在大规模知识库上，BM25 的局限性会更明显，optimized 的优势可能更大也可能需要更多优化
5. **Full set 仍有 2 个 failed cases**：均为物流加急/仓库查询，暴露了跨语言同义词映射的精度瓶颈
