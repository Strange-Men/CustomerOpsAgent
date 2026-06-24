"""Tests for retrieval evaluation harness."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.eval.retrieval_eval import (
    CaseResult,
    evaluate_case,
    evaluate_retriever,
    hit_at_k,
    load_eval_cases,
    reciprocal_rank,
    run_default_evaluation,
    unique_doc_ids_from_results,
)
from app.rag.schemas import EvalCase, RetrievedChunk


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_retrieved_chunk(doc_id: str, chunk_id: str | None = None, score: float = 1.0) -> RetrievedChunk:
    """Create a minimal RetrievedChunk for testing."""
    return RetrievedChunk(
        chunk_id=chunk_id or f"{doc_id}::chunk_000",
        doc_id=doc_id,
        title="Test Title",
        category="logistics",
        market="GLOBAL",
        language="zh",
        policy_type="shipping",
        priority=1,
        source="test",
        content="Test content for evaluation.",
        chunk_index=0,
        score=score,
    )


def _make_eval_case(case_id: str, expected_doc_ids: list[str]) -> EvalCase:
    """Create a minimal EvalCase for testing."""
    return EvalCase(
        case_id=case_id,
        question=f"Test question for {case_id}",
        category="logistics",
        market="GLOBAL",
        language="zh",
        difficulty="easy",
        expected_doc_ids=expected_doc_ids,
        expected_keywords=["keyword1"],
    )


def _make_fake_retriever(results_map: dict[str, list[RetrievedChunk]]):
    """Create a fake BM25Retriever with canned search results.

    Args:
        results_map: Mapping from query string to list of RetrievedChunk.
    """
    retriever = MagicMock()
    retriever.search = MagicMock(
        side_effect=lambda query, top_k=5: results_map.get(query, [])[:top_k]
    )
    return retriever


# ---------------------------------------------------------------------------
# 1. test_load_eval_cases_from_seed
# ---------------------------------------------------------------------------

class TestLoadEvalCasesFromSeed:
    """Verify that the seed eval cases file loads correctly."""

    def test_load_eval_cases_from_seed(self):
        """Seed file loads 20 EvalCase instances with non-empty expected_doc_ids."""
        cases = load_eval_cases()
        assert len(cases) == 20
        for case in cases:
            assert isinstance(case, EvalCase)
            assert len(case.expected_doc_ids) >= 1


# ---------------------------------------------------------------------------
# 2. test_unique_doc_ids_from_results_deduplicates_preserving_order
# ---------------------------------------------------------------------------

class TestUniqueDocIdsFromResults:
    """Test doc_id deduplication logic."""

    def test_unique_doc_ids_from_results_deduplicates_preserving_order(self):
        """Same doc_id appearing multiple times keeps only the first occurrence."""
        results = [
            _make_retrieved_chunk("doc_a", "doc_a::chunk_000"),
            _make_retrieved_chunk("doc_b", "doc_b::chunk_000"),
            _make_retrieved_chunk("doc_a", "doc_a::chunk_001"),
            _make_retrieved_chunk("doc_c", "doc_c::chunk_000"),
            _make_retrieved_chunk("doc_b", "doc_b::chunk_001"),
        ]
        unique = unique_doc_ids_from_results(results)
        assert unique == ["doc_a", "doc_b", "doc_c"]

    def test_unique_doc_ids_empty_results(self):
        """Empty results returns empty list."""
        assert unique_doc_ids_from_results([]) == []


# ---------------------------------------------------------------------------
# 3. test_hit_at_k
# ---------------------------------------------------------------------------

class TestHitAtK:
    """Test the hit_at_k metric function."""

    def test_hit_at_k(self):
        """hit_at_k correctly identifies hits at different k values."""
        expected = ["doc_b"]
        retrieved = ["doc_a", "doc_b", "doc_c"]

        assert hit_at_k(expected, retrieved, k=1) is False
        assert hit_at_k(expected, retrieved, k=2) is True
        assert hit_at_k(expected, retrieved, k=3) is True

    def test_hit_at_k_zero(self):
        """k=0 always returns False."""
        assert hit_at_k(["doc_a"], ["doc_a"], k=0) is False

    def test_hit_at_k_negative(self):
        """Negative k returns False."""
        assert hit_at_k(["doc_a"], ["doc_a"], k=-1) is False

    def test_hit_at_k_multiple_expected(self):
        """Multiple expected docs — hit if any is found."""
        expected = ["doc_x", "doc_y"]
        retrieved = ["doc_a", "doc_y", "doc_b"]
        assert hit_at_k(expected, retrieved, k=1) is False
        assert hit_at_k(expected, retrieved, k=2) is True


# ---------------------------------------------------------------------------
# 4. test_reciprocal_rank
# ---------------------------------------------------------------------------

class TestReciprocalRank:
    """Test the reciprocal_rank metric function."""

    def test_rr_first_rank(self):
        """First position hit returns 1.0."""
        assert reciprocal_rank(["doc_a"], ["doc_a", "doc_b"]) == 1.0

    def test_rr_second_rank(self):
        """Second position hit returns 0.5."""
        assert reciprocal_rank(["doc_b"], ["doc_a", "doc_b", "doc_c"]) == 0.5

    def test_rr_no_hit(self):
        """No hit returns 0.0."""
        assert reciprocal_rank(["doc_x"], ["doc_a", "doc_b"]) == 0.0

    def test_rr_multiple_expected(self):
        """First match among multiple expected docs determines rank."""
        assert reciprocal_rank(["doc_x", "doc_b"], ["doc_a", "doc_b"]) == 0.5


# ---------------------------------------------------------------------------
# 5. test_evaluate_case_does_not_pass_expected_docs_to_search
# ---------------------------------------------------------------------------

class TestEvaluateCaseAntiCheat:
    """Ensure expected_doc_ids are never passed to retriever.search."""

    def test_evaluate_case_does_not_pass_expected_docs_to_search(self):
        """evaluate_case calls search with only query and top_k, no expected docs."""
        results = [_make_retrieved_chunk("doc_a")]
        retriever = MagicMock()
        retriever.search = MagicMock(return_value=results)

        case = _make_eval_case("case_001", ["doc_a"])
        evaluate_case(case, retriever, top_k=5)

        retriever.search.assert_called_once_with(case.question, top_k=5)
        call_args = retriever.search.call_args
        # Ensure no extra positional or keyword args for expected_doc_ids
        assert call_args == ((case.question,), {"top_k": 5})


# ---------------------------------------------------------------------------
# 6. test_evaluate_case_returns_required_fields
# ---------------------------------------------------------------------------

class TestEvaluateCaseFields:
    """Verify evaluate_case output contains all required fields."""

    def test_evaluate_case_returns_required_fields(self):
        """CaseResult from evaluate_case has all expected fields."""
        results = [
            _make_retrieved_chunk("doc_x", "doc_x::chunk_000", score=2.5),
            _make_retrieved_chunk("doc_y", "doc_y::chunk_000", score=1.8),
        ]
        retriever = _make_fake_retriever({"Test question for case_001": results})

        case = _make_eval_case("case_001", ["doc_y"])
        result = evaluate_case(case, retriever, top_k=5)

        assert isinstance(result, CaseResult)
        assert result.case_id == "case_001"
        assert result.expected_doc_ids == ["doc_y"]
        assert "doc_x" in result.retrieved_doc_ids
        assert "doc_y" in result.retrieved_doc_ids
        assert result.hit_at_5 is True
        assert result.reciprocal_rank == 0.5
        assert len(result.retrieved_chunk_ids) == 2
        assert len(result.top_scores) == 2


# ---------------------------------------------------------------------------
# 7. test_evaluate_retriever_aggregate_metrics
# ---------------------------------------------------------------------------

class TestEvaluateRetrieverAggregate:
    """Verify aggregate metrics computation."""

    def test_evaluate_retriever_aggregate_metrics(self):
        """Aggregate recall and MRR are computed correctly."""
        case1 = _make_eval_case("case_1", ["doc_a"])
        case2 = _make_eval_case("case_2", ["doc_b"])
        case3 = _make_eval_case("case_3", ["doc_c"])

        results1 = [_make_retrieved_chunk("doc_a")]  # hit@1
        results2 = [_make_retrieved_chunk("doc_x"), _make_retrieved_chunk("doc_b")]  # hit@2, not hit@1
        results3 = [_make_retrieved_chunk("doc_x"), _make_retrieved_chunk("doc_y"), _make_retrieved_chunk("doc_z")]  # miss

        retriever = _make_fake_retriever({
            "Test question for case_1": results1,
            "Test question for case_2": results2,
            "Test question for case_3": results3,
        })

        report = evaluate_retriever(retriever, [case1, case2, case3], top_k=5)

        assert report.total_cases == 3
        # case1: hit@1, case2: miss@1, case3: miss@1
        assert report.recall_at_1 == pytest.approx(1 / 3)
        # case1: hit@3, case2: hit@3, case3: miss@3
        assert report.recall_at_3 == pytest.approx(2 / 3)
        # case1: hit@5, case2: hit@5, case3: miss@5
        assert report.recall_at_5 == pytest.approx(2 / 3)
        # MRR: (1.0 + 0.5 + 0.0) / 3
        assert report.mrr == pytest.approx(1.5 / 3)
        assert len(report.failed_cases) == 1
        assert report.failed_cases[0].case_id == "case_3"


# ---------------------------------------------------------------------------
# 8. test_run_default_evaluation_seed_cases
# ---------------------------------------------------------------------------

class TestRunDefaultEvaluation:
    """Integration test: run the full default evaluation."""

    def test_run_default_evaluation_seed_cases(self):
        """Default evaluation on seed cases produces valid metrics."""
        report = run_default_evaluation()

        assert report.total_cases == 20
        assert 0.0 <= report.recall_at_1 <= 1.0
        assert 0.0 <= report.recall_at_3 <= 1.0
        assert 0.0 <= report.recall_at_5 <= 1.0
        assert 0.0 <= report.mrr <= 1.0
        assert len(report.per_case_results) == 20


# ---------------------------------------------------------------------------
# 9. test_retrieval_eval_does_not_modify_retriever
# ---------------------------------------------------------------------------

class TestRetrieverNotModified:
    """Ensure M4 did not leak eval info into retriever.py."""

    def test_retrieval_eval_does_not_modify_retriever(self):
        """retriever.py must not contain eval_cases_seed, expected_doc_ids, or expected_keywords."""
        source_file = Path(__file__).resolve().parent.parent / "app" / "rag" / "retriever.py"
        content = source_file.read_text(encoding="utf-8")
        assert "eval_cases_seed" not in content
        assert "expected_doc_ids" not in content
        assert "expected_keywords" not in content


# ---------------------------------------------------------------------------
# 10. test_load_eval_cases_reports_bad_json_line
# ---------------------------------------------------------------------------

class TestLoadEvalCasesBadJson:
    """Verify error reporting for malformed JSONL."""

    def test_load_eval_cases_reports_bad_json_line(self, tmp_path):
        """Bad JSON line raises ValueError with line number."""
        content = (
            '{"case_id": "good", "question": "q", "category": "c", '
            '"market": "M", "language": "zh", "difficulty": "easy", '
            '"expected_doc_ids": ["d1"], "expected_keywords": ["k1"]}\n'
            "this is not json\n"
            '{"case_id": "good2", "question": "q2", "category": "c2", '
            '"market": "M2", "language": "en", "difficulty": "hard", '
            '"expected_doc_ids": ["d2"], "expected_keywords": ["k2"]}\n'
        )
        bad_file = tmp_path / "bad.jsonl"
        bad_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="line 2"):
            load_eval_cases(bad_file)

    def test_load_eval_cases_reports_schema_error(self, tmp_path):
        """Schema validation failure raises ValueError with line number."""
        content = '{"case_id": "missing_fields"}\n'
        bad_file = tmp_path / "bad_schema.jsonl"
        bad_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="line 1"):
            load_eval_cases(bad_file)
