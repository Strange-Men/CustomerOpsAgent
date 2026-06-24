# CustomerOps Agent｜两天 MVP 验收标准

**日期**：2026-06-24
**适用阶段**：M1-M10

---

## 一、简历指标口径说明

### 口径定义

| 表述 | 类型 | 计算方式 | 示例 |
|------|------|---------|------|
| "提升 30%" | 相对提升 | 原值 × (1 + 30%) | 55% × 1.3 = 71.5% |
| "提升 30 个百分点" | 绝对提升 | 原值 + 30pp | 55% + 30pp = 85% |

### 使用规范

- **简历简写**："高频咨询场景回答合格率提升 30%"（可保留，但面试时需说明口径）
- **项目报告 / EVAL_REPORT / 面试口述**："高频咨询场景回答合格率从 55% 提升到 85%，提升 30 个百分点"
- **核心指标**："top-5 知识召回准确率提升至 85%"

### 为什么区分

- "提升 30%" 容易被理解为相对提升（71.5%）
- "提升 30 个百分点" 是绝对提升（85%），更严谨
- 面试时如果被追问，需要能说清楚

---

## 二、必须完成（11 项）

| # | 标准 | 验收命令 |
|---|------|---------|
| 1 | 20 条 seed eval cases 存在，且有 category/market/language/difficulty/expected_doc_ids/expected_keywords | `python -c "import json; cases=json.load(open('backend/data/eval/seed_eval_cases.json')); print(f'{len(cases)} cases')"` |
| 2 | loader + chunker 可将知识库文档切分为 chunks | `python -m pytest backend/tests/test_chunker.py` |
| 3 | baseline BM25 retriever 可返回 top-k chunks | `python -m pytest backend/tests/test_retriever.py` |
| 4 | retrieval evaluation 可计算 Recall@1/3/5, MRR | `python -m pytest backend/tests/test_retrieval_eval.py` |
| 5 | optimized retriever 的 Recall@5 ≥ 85% | `python -m pytest backend/tests/test_retrieval_eval.py -k optimized` |
| 6 | 120+ bad cases 存在，且有分类和优化日志 | `ls backend/data/eval/bad_cases.json` + `ls docs/BAD_CASE_LOG.md` |
| 7 | mock answer generator 可生成带 citations 的回答 | `python -m pytest backend/tests/test_answer_generator.py` |
| 8 | answer evaluation 可按三大维度评估回答质量 | `python -m pytest backend/tests/test_answer_eval.py` |
| 9 | FastAPI 提供 /api/retrieve、/api/answer、/api/eval | `curl localhost:8000/api/health` |
| 10 | pytest 通过 | `conda run -n customerops-agent python -m pytest backend` |
| 11 | ruff check 通过 | `conda run -n customerops-agent python -m ruff check backend` |

### 隐含标准

| # | 标准 | 说明 |
|---|------|------|
| 12 | README 能让面试官 30 秒看懂项目 | M10 更新 |
| 13 | EVAL_REPORT 能展示 baseline vs optimized 对比 | M10 更新 |

---

## 三、可选完成（3 项加分）

| # | 标准 | 条件 |
|---|------|------|
| 1 | 极简 Chat Demo 前端 | M11，仅 M1-M10 全部完成后 |
| 2 | Eval Report 页面 | M11，同上 |
| 3 | embedding adapter stub | M5，接口保留即可 |

---

## 四、不做清单

- ❌ 不做 6 Agent 工单编排
- ❌ 不做登录/权限/多租户
- ❌ 不做真实 LLM 调用（mock-first）
- ❌ 不做向量数据库
- ❌ 不做 Docker 部署
- ❌ 不做复杂前端 Dashboard
- ❌ 不做订单/物流真实 API
- ❌ 不做前端工单系统

---

## 五、验收流程

每个 M 阶段完成后：

1. 运行对应测试命令
2. 确认 ruff check 通过
3. 确认 frontend 仍可 build（`cd frontend && npm run build`）
4. 更新 docs/DEV_STATUS.md
5. 更新 docs/CHANGELOG.md
6. Git commit + tag
