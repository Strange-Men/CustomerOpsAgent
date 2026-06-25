"""Tests for the full 120+ eval case dataset (M6)."""

import json
import re
from pathlib import Path

import pytest

from app.rag.schemas import EvalCase

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
KB_FILE = DATA_DIR / "knowledge_base" / "customer_service_seed.jsonl"
FULL_EVAL_FILE = DATA_DIR / "eval_cases_full.jsonl"
SEED_EVAL_FILE = DATA_DIR / "eval_cases_seed.jsonl"


def _load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL file and return a list of dicts."""
    items = []
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON at {path.name} line {line_num}: {e}")
    return items


@pytest.fixture(scope="module")
def full_cases():
    """Load all full eval cases once per module."""
    raw = _load_jsonl(FULL_EVAL_FILE)
    return [EvalCase(**item) for item in raw]


@pytest.fixture(scope="module")
def kb_doc_ids():
    """Load knowledge base doc_ids once per module."""
    raw = _load_jsonl(KB_FILE)
    return {item["doc_id"] for item in raw}


@pytest.fixture(scope="module")
def seed_case_ids():
    """Load seed case_ids once per module."""
    raw = _load_jsonl(SEED_EVAL_FILE)
    return {item["case_id"] for item in raw}


# ---------------------------------------------------------------------------
# 1. test_full_eval_dataset_loads
# ---------------------------------------------------------------------------

class TestFullEvalDatasetLoads:
    """Verify that the full eval dataset loads and validates."""

    def test_full_eval_dataset_loads(self, full_cases):
        """Full dataset loads >= 120 valid EvalCase instances."""
        assert len(full_cases) >= 120, f"Expected >= 120 cases, got {len(full_cases)}"
        for case in full_cases:
            assert isinstance(case, EvalCase)
            assert case.case_id
            assert case.question
            assert len(case.expected_doc_ids) >= 1
            assert len(case.expected_keywords) >= 1


# ---------------------------------------------------------------------------
# 2. test_full_eval_case_ids_unique
# ---------------------------------------------------------------------------

class TestFullEvalCaseIdsUnique:
    """Verify all case_ids are unique."""

    def test_full_eval_case_ids_unique(self, full_cases):
        """No duplicate case_ids in the full dataset."""
        ids = [c.case_id for c in full_cases]
        dupes = [x for x in ids if ids.count(x) > 1]
        assert not dupes, f"Duplicate case_ids: {set(dupes)}"


# ---------------------------------------------------------------------------
# 3. test_full_eval_expected_doc_ids_exist
# ---------------------------------------------------------------------------

class TestFullEvalExpectedDocIdsExist:
    """Verify all expected_doc_ids reference real knowledge base docs."""

    def test_full_eval_expected_doc_ids_exist(self, full_cases, kb_doc_ids):
        """Every expected_doc_id exists in the knowledge base."""
        missing = []
        for case in full_cases:
            for doc_id in case.expected_doc_ids:
                if doc_id not in kb_doc_ids:
                    missing.append((case.case_id, doc_id))
        assert not missing, f"Missing doc_ids: {missing}"


# ---------------------------------------------------------------------------
# 4. test_full_eval_languages_distribution
# ---------------------------------------------------------------------------

class TestFullEvalLanguagesDistribution:
    """Verify language distribution meets requirements."""

    def test_full_eval_languages_distribution(self, full_cases):
        """At least 80 zh and 25 en cases."""
        langs = {c.language for c in full_cases}
        assert "zh" in langs, "Missing language 'zh'"
        assert "en" in langs, "Missing language 'en'"

        en_count = sum(1 for c in full_cases if c.language == "en")
        zh_count = sum(1 for c in full_cases if c.language == "zh")
        assert en_count >= 25, f"Expected >= 25 en cases, got {en_count}"
        assert zh_count >= 80, f"Expected >= 80 zh cases, got {zh_count}"


# ---------------------------------------------------------------------------
# 5. test_full_eval_difficulty_distribution
# ---------------------------------------------------------------------------

class TestFullEvalDifficultyDistribution:
    """Verify difficulty distribution meets requirements."""

    def test_full_eval_difficulty_distribution(self, full_cases):
        """At least 30 hard, 50 medium, 10 easy."""
        diffs = {c.difficulty for c in full_cases}
        assert {"easy", "medium", "hard"}.issubset(diffs), f"Missing difficulties: {diffs}"

        hard = sum(1 for c in full_cases if c.difficulty == "hard")
        medium = sum(1 for c in full_cases if c.difficulty == "medium")
        easy = sum(1 for c in full_cases if c.difficulty == "easy")
        assert hard >= 30, f"Expected >= 30 hard cases, got {hard}"
        assert medium >= 50, f"Expected >= 50 medium cases, got {medium}"
        assert easy >= 10, f"Expected >= 10 easy cases, got {easy}"


# ---------------------------------------------------------------------------
# 6. test_full_eval_category_coverage
# ---------------------------------------------------------------------------

class TestFullEvalCategoryCoverage:
    """Verify all 10 categories are covered with minimum counts."""

    def test_full_eval_category_coverage(self, full_cases):
        """All 10 categories present, each >= 8 cases."""
        required = {
            "logistics", "customs", "return", "refund", "exchange",
            "address", "order", "payment", "package", "coupon",
        }
        cats = {c.category for c in full_cases}
        missing = required - cats
        assert not missing, f"Missing categories: {missing}"

        from collections import Counter
        counts = Counter(c.category for c in full_cases)
        for cat in required:
            assert counts[cat] >= 8, f"Category '{cat}' has only {counts[cat]} cases (need >= 8)"


# ---------------------------------------------------------------------------
# 7. test_full_eval_market_coverage
# ---------------------------------------------------------------------------

class TestFullEvalMarketCoverage:
    """Verify US, EU, GLOBAL markets are all covered."""

    def test_full_eval_market_coverage(self, full_cases):
        """All 3 markets present."""
        markets = {c.market for c in full_cases}
        assert "US" in markets, "Missing market 'US'"
        assert "EU" in markets, "Missing market 'EU'"
        assert "GLOBAL" in markets, "Missing market 'GLOBAL'"


# ---------------------------------------------------------------------------
# 8. test_full_eval_expected_keywords_quality
# ---------------------------------------------------------------------------

class TestFullEvalKeywordsQuality:
    """Verify expected_keywords are specific, not generic."""

    BANNED_GENERIC = {"客服", "处理", "问题", "help", "issue", "order", "support"}

    def test_full_eval_expected_keywords_quality(self, full_cases):
        """Each case has >= 3 keywords, not all generic."""
        for case in full_cases:
            kw = case.expected_keywords
            assert len(kw) >= 3, (
                f"case {case.case_id} has only {len(kw)} keywords: {kw}"
            )
            generic = [k for k in kw if k.lower() in self.BANNED_GENERIC]
            assert len(generic) < len(kw), (
                f"case {case.case_id} has all-generic keywords: {kw}"
            )


# ---------------------------------------------------------------------------
# 9. test_full_eval_english_questions_are_english
# ---------------------------------------------------------------------------

class TestFullEvalEnglishQuestions:
    """Verify language=en cases actually have English questions."""

    def test_full_eval_english_questions_are_english(self, full_cases):
        """language=en questions should not be mostly Chinese."""
        chinese_pattern = re.compile(r"[一-鿿]")
        for case in full_cases:
            if case.language == "en":
                chinese_chars = chinese_pattern.findall(case.question)
                ratio = len(chinese_chars) / max(len(case.question), 1)
                assert ratio < 0.3, (
                    f"case {case.case_id} marked 'en' but question is "
                    f"{ratio:.0%} Chinese: {case.question[:50]}..."
                )


# ---------------------------------------------------------------------------
# 10. test_seed_cases_included_in_full_dataset
# ---------------------------------------------------------------------------

class TestSeedCasesIncluded:
    """Verify seed eval cases are included in the full dataset."""

    def test_seed_cases_included_in_full_dataset(self, full_cases, seed_case_ids):
        """All seed case_ids appear in the full dataset."""
        full_ids = {c.case_id for c in full_cases}
        missing = seed_case_ids - full_ids
        assert not missing, f"Seed cases missing from full dataset: {missing}"


# ---------------------------------------------------------------------------
# 11. test_full_eval_can_run_baseline_and_optimized
# ---------------------------------------------------------------------------

class TestFullEvalCanRunBaselineAndOptimized:
    """Integration test: run baseline and optimized on the full dataset."""

    def test_full_eval_can_run_baseline_and_optimized(self):
        """Both retrievers produce valid metrics on the full dataset."""
        from app.eval.retrieval_eval import load_eval_cases, evaluate_retriever
        from app.rag.retriever import build_default_retriever
        from app.rag.optimized_retriever import build_default_optimized_retriever

        cases = load_eval_cases(FULL_EVAL_FILE)
        assert len(cases) >= 120

        base = evaluate_retriever(build_default_retriever(), cases)
        opt = evaluate_retriever(build_default_optimized_retriever(), cases)

        # Metrics in valid range
        for report in [base, opt]:
            assert 0.0 <= report.recall_at_1 <= 1.0
            assert 0.0 <= report.recall_at_3 <= 1.0
            assert 0.0 <= report.recall_at_5 <= 1.0
            assert 0.0 <= report.mrr <= 1.0

        # Optimized should be competitive
        assert opt.recall_at_5 >= 0.85, (
            f"Optimized Recall@5 {opt.recall_at_5:.4f} < 0.85"
        )
        assert opt.recall_at_5 >= base.recall_at_5, (
            f"Optimized Recall@5 {opt.recall_at_5:.4f} < baseline {base.recall_at_5:.4f}"
        )
        # At least one of MRR or Recall@1 should improve
        assert opt.mrr >= base.mrr or opt.recall_at_1 >= base.recall_at_1, (
            f"Neither MRR ({opt.mrr:.4f} vs {base.mrr:.4f}) nor "
            f"Recall@1 ({opt.recall_at_1:.4f} vs {base.recall_at_1:.4f}) improved"
        )


# ---------------------------------------------------------------------------
# 12. test_full_eval_dataset_does_not_modify_seed
# ---------------------------------------------------------------------------

class TestSeedUnchanged:
    """Verify the seed eval cases file was not modified."""

    def test_full_eval_dataset_does_not_modify_seed(self):
        """Seed file still has exactly 20 cases."""
        raw = _load_jsonl(SEED_EVAL_FILE)
        assert len(raw) == 20, f"Seed file has {len(raw)} cases, expected 20"
