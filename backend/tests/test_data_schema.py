"""Tests for knowledge base and eval case data schemas."""

import json
import re
from pathlib import Path

import pytest

from app.rag.schemas import EvalCase, KnowledgeDocument

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
KB_FILE = DATA_DIR / "knowledge_base" / "customer_service_seed.jsonl"
EVAL_FILE = DATA_DIR / "eval_cases_seed.jsonl"


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


# ---------------------------------------------------------------------------
# Knowledge Base Tests
# ---------------------------------------------------------------------------


class TestKnowledgeBase:
    """Validate customer_service_seed.jsonl against KnowledgeDocument schema."""

    @pytest.fixture(autouse=True)
    def load_docs(self):
        self.raw = _load_jsonl(KB_FILE)
        self.docs = [KnowledgeDocument(**item) for item in self.raw]

    def test_file_exists(self):
        assert KB_FILE.exists(), f"Knowledge base file not found: {KB_FILE}"

    def test_minimum_doc_count(self):
        assert len(self.docs) >= 12, f"Expected >= 12 docs, got {len(self.docs)}"

    def test_all_docs_valid_schema(self):
        for i, doc in enumerate(self.docs):
            assert doc.doc_id, f"doc {i} has empty doc_id"
            assert doc.content, f"doc {i} has empty content"

    def test_doc_id_unique(self):
        doc_ids = [d.doc_id for d in self.docs]
        duplicates = [id for id in doc_ids if doc_ids.count(id) > 1]
        assert not duplicates, f"Duplicate doc_ids: {set(duplicates)}"

    def test_contains_zh_and_en(self):
        languages = {d.language for d in self.docs}
        assert "zh" in languages, "Missing language 'zh' in knowledge base"
        assert "en" in languages, "Missing language 'en' in knowledge base"

    def test_market_coverage(self):
        markets = {d.market for d in self.docs}
        assert "US" in markets, "Missing market 'US'"
        assert "EU" in markets, "Missing market 'EU'"
        assert "GLOBAL" in markets, "Missing market 'GLOBAL'"

    def test_content_not_too_short(self):
        for doc in self.docs:
            assert len(doc.content) >= 80, (
                f"doc {doc.doc_id} content too short: {len(doc.content)} chars"
            )


# ---------------------------------------------------------------------------
# Eval Cases Tests
# ---------------------------------------------------------------------------


class TestEvalCases:
    """Validate eval_cases_seed.jsonl against EvalCase schema."""

    @pytest.fixture(autouse=True)
    def load_cases(self):
        self.raw = _load_jsonl(EVAL_FILE)
        self.cases = [EvalCase(**item) for item in self.raw]
        # Also load knowledge base doc_ids for cross-reference
        kb_raw = _load_jsonl(KB_FILE)
        self.kb_doc_ids = {item["doc_id"] for item in kb_raw}

    def test_file_exists(self):
        assert EVAL_FILE.exists(), f"Eval cases file not found: {EVAL_FILE}"

    def test_exact_case_count(self):
        assert len(self.cases) == 20, f"Expected 20 eval cases, got {len(self.cases)}"

    def test_all_cases_valid_schema(self):
        for i, case in enumerate(self.cases):
            assert case.case_id, f"case {i} has empty case_id"
            assert case.question, f"case {i} has empty question"
            assert case.expected_doc_ids, f"case {i} has empty expected_doc_ids"
            assert case.expected_keywords, f"case {i} has empty expected_keywords"

    def test_case_id_unique(self):
        case_ids = [c.case_id for c in self.cases]
        duplicates = [id for id in case_ids if case_ids.count(id) > 1]
        assert not duplicates, f"Duplicate case_ids: {set(duplicates)}"

    def test_expected_doc_ids_exist_in_kb(self):
        for case in self.cases:
            for doc_id in case.expected_doc_ids:
                assert doc_id in self.kb_doc_ids, (
                    f"case {case.case_id} references unknown doc_id: {doc_id}"
                )

    def test_contains_zh_and_en(self):
        languages = {c.language for c in self.cases}
        assert "zh" in languages, "Missing language 'zh' in eval cases"
        assert "en" in languages, "Missing language 'en' in eval cases"

    def test_minimum_hard_cases(self):
        hard_cases = [c for c in self.cases if c.difficulty == "hard"]
        assert len(hard_cases) >= 3, (
            f"Expected >= 3 hard cases, got {len(hard_cases)}"
        )

    def test_minimum_en_cases(self):
        en_cases = [c for c in self.cases if c.language == "en"]
        assert len(en_cases) >= 3, (
            f"Expected >= 3 English cases, got {len(en_cases)}"
        )

    def test_en_cases_have_english_questions(self):
        """Check that language=en cases have questions that are not obviously Chinese."""
        chinese_pattern = re.compile(r"[一-鿿]")
        for case in self.cases:
            if case.language == "en":
                chinese_chars = chinese_pattern.findall(case.question)
                # Allow a few Chinese chars (e.g., brand names), but not mostly Chinese
                assert len(chinese_chars) < len(case.question) * 0.3, (
                    f"case {case.case_id} marked as 'en' but question is mostly Chinese: "
                    f"{case.question[:50]}..."
                )
