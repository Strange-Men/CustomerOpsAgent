"""Tests for optimized retriever."""

from pathlib import Path

from app.rag.optimized_retriever import (
    OptimizedRetriever,
    build_default_optimized_retriever,
    expand_query,
    infer_query_signals,
)
from app.rag.schemas import KnowledgeChunk

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_chunks() -> list[KnowledgeChunk]:
    """Create test chunks with distinct categories and metadata."""
    return [
        KnowledgeChunk(
            chunk_id="customs_doc::chunk_000",
            doc_id="customs_doc",
            title="Customs Clearance Guide",
            category="customs",
            market="GLOBAL",
            language="zh",
            policy_type="customs",
            priority=1,
            source="seed",
            content="跨境包裹清关延迟是常见情况，通常由海关抽检或申报信息不完整导致。清关延迟期间物流状态可能长时间停留在清关中。",
            chunk_index=0,
        ),
        KnowledgeChunk(
            chunk_id="shipping_us::chunk_000",
            doc_id="shipping_us",
            title="US Shipping Timeframes",
            category="logistics",
            market="US",
            language="en",
            policy_type="shipping",
            priority=1,
            source="seed",
            content="Standard shipping to the US takes 7-15 business days from the date of dispatch. Express shipping delivers within 3-5 business days.",
            chunk_index=0,
        ),
        KnowledgeChunk(
            chunk_id="shipping_eu::chunk_000",
            doc_id="shipping_eu",
            title="EU Shipping Timeframes",
            category="logistics",
            market="EU",
            language="zh",
            policy_type="shipping",
            priority=1,
            source="seed",
            content="欧洲标准配送时效为 10-20 个工作日，覆盖德国、法国、意大利、西班牙等主要国家。如遇海关抽检可能延迟。",
            chunk_index=0,
        ),
        KnowledgeChunk(
            chunk_id="refund_doc::chunk_000",
            doc_id="refund_doc",
            title="Refund Policy",
            category="refund",
            market="GLOBAL",
            language="zh",
            policy_type="payment",
            priority=1,
            source="seed",
            content="退款将在退货质检通过后 7-10 个工作日内处理。信用卡退款需 1-2 个账单周期。",
            chunk_index=0,
        ),
        KnowledgeChunk(
            chunk_id="return_doc::chunk_000",
            doc_id="return_doc",
            title="Return Policy",
            category="return",
            market="US",
            language="zh",
            policy_type="return",
            priority=1,
            source="seed",
            content="美国市场支持 30 天无理由退货，自签收之日起计算。退货商品需保持原包装完好。",
            chunk_index=0,
        ),
    ]


# ---------------------------------------------------------------------------
# 1. test_expand_query_adds_cross_lingual_terms
# ---------------------------------------------------------------------------


class TestExpandQueryCrossLingual:
    """Test that expand_query adds cross-lingual synonym terms."""

    def test_expand_query_adds_cross_lingual_terms(self):
        """English 'customs delay' should produce expanded terms including Chinese equivalents."""
        expanded = expand_query("customs delay")
        # Should contain Chinese synonyms for customs
        has_chinese_customs = any(
            term in expanded for term in ["清关", "海关", "关税"]
        )
        # Should contain Chinese synonyms for delay
        has_chinese_delay = any(
            term in expanded for term in ["延迟", "卡住", "处理中"]
        )
        assert has_chinese_customs, f"Expected Chinese customs terms in expanded query, got: {expanded}"
        assert has_chinese_delay, f"Expected Chinese delay terms in expanded query, got: {expanded}"

    def test_expand_query_preserves_original(self):
        """Original query terms should still be present in expanded query."""
        expanded = expand_query("shipping")
        assert "shipping" in expanded

    def test_expand_query_no_match_returns_original(self):
        """Query with no matching terms returns the original."""
        original = "xyzzy foobar"
        expanded = expand_query(original)
        assert expanded == original


# ---------------------------------------------------------------------------
# 2. test_infer_query_signals_customs
# ---------------------------------------------------------------------------


class TestInferQuerySignalsCustoms:
    """Test signal inference for customs-related queries."""

    def test_infer_query_signals_customs(self):
        """'customs clearance delay' should infer customs category and English language."""
        signals = infer_query_signals("customs clearance delay")
        assert "customs" in signals.inferred_categories, (
            f"Expected 'customs' in categories, got {signals.inferred_categories}"
        )
        assert signals.inferred_language == "en"


# ---------------------------------------------------------------------------
# 3. test_infer_query_signals_shipping_us
# ---------------------------------------------------------------------------


class TestInferQuerySignalsShippingUS:
    """Test signal inference for US shipping queries."""

    def test_infer_query_signals_shipping_us(self):
        """'How long does shipping take to the US?' should infer logistics category and US market."""
        signals = infer_query_signals("How long does shipping take to the US?")
        assert "logistics" in signals.inferred_categories, (
            f"Expected 'logistics' in categories, got {signals.inferred_categories}"
        )
        assert "US" in signals.inferred_markets, (
            f"Expected 'US' in markets, got {signals.inferred_markets}"
        )


# ---------------------------------------------------------------------------
# 4. test_optimized_retriever_does_not_import_eval_cases
# ---------------------------------------------------------------------------


class TestAntiCheat:
    """Ensure optimized_retriever.py does not reference eval data."""

    def test_optimized_retriever_does_not_import_eval_cases(self):
        """optimized_retriever.py must not contain eval_cases_seed, expected_doc_ids, expected_keywords, or case_id."""
        source_file = Path(__file__).resolve().parent.parent / "app" / "rag" / "optimized_retriever.py"
        content = source_file.read_text(encoding="utf-8")
        assert "eval_cases_seed" not in content, "optimized_retriever.py must not reference eval_cases_seed"
        assert "expected_doc_ids" not in content, "optimized_retriever.py must not use expected_doc_ids"
        assert "expected_keywords" not in content, "optimized_retriever.py must not use expected_keywords"
        # case_id check: should not appear as a variable or field access
        assert "case_id" not in content, "optimized_retriever.py must not use case_id"


# ---------------------------------------------------------------------------
# 5. test_optimized_retriever_preserves_metadata
# ---------------------------------------------------------------------------


class TestMetadataPreservation:
    """Ensure search results preserve all metadata fields."""

    def test_optimized_retriever_preserves_metadata(self):
        """RetrievedChunk from OptimizedRetriever preserves all metadata fields."""
        chunks = _make_chunks()
        retriever = OptimizedRetriever(chunks)
        results = retriever.search("customs", top_k=5)

        assert len(results) > 0
        r = results[0]
        # All metadata fields must be present
        assert r.doc_id != ""
        assert r.category != ""
        assert r.market != ""
        assert r.language != ""
        assert r.policy_type != ""
        assert r.source != ""
        assert r.chunk_index >= 0
        assert r.chunk_id != ""
        assert r.title != ""


# ---------------------------------------------------------------------------
# 6. test_optimized_search_returns_sorted_scores
# ---------------------------------------------------------------------------


class TestSortedScores:
    """Ensure results are sorted by score descending."""

    def test_optimized_search_returns_sorted_scores(self):
        """Results should be sorted by score in descending order, all scores >= 0."""
        chunks = _make_chunks()
        retriever = OptimizedRetriever(chunks)
        results = retriever.search("shipping delivery", top_k=5)

        assert len(results) > 0
        for r in results:
            assert isinstance(r.score, float), f"Score must be float, got {type(r.score)}"
            assert r.score >= 0, f"Score must be >= 0, got {r.score}"

        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score, (
                f"Scores not sorted: results[{i}].score={results[i].score} < results[{i+1}].score={results[i+1].score}"
            )


# ---------------------------------------------------------------------------
# 7. test_optimized_search_empty_query
# ---------------------------------------------------------------------------


class TestEmptyQuery:
    """Ensure empty queries return empty results."""

    def test_optimized_search_empty_query(self):
        """Empty or whitespace-only query returns empty list."""
        chunks = _make_chunks()
        retriever = OptimizedRetriever(chunks)
        assert retriever.search("") == []
        assert retriever.search("   ") == []


# ---------------------------------------------------------------------------
# 8. test_optimized_search_top_k_limit
# ---------------------------------------------------------------------------


class TestTopKLimit:
    """Ensure top_k limits the number of results."""

    def test_optimized_search_top_k_limit(self):
        """top_k=3 returns at most 3 results."""
        chunks = _make_chunks()
        retriever = OptimizedRetriever(chunks)
        results = retriever.search("shipping customs refund return damaged", top_k=3)
        assert len(results) <= 3


# ---------------------------------------------------------------------------
# 9. test_build_default_optimized_retriever
# ---------------------------------------------------------------------------


class TestBuildDefault:
    """Test the factory function."""

    def test_build_default_optimized_retriever(self):
        """build_default_optimized_retriever creates a working retriever."""
        retriever = build_default_optimized_retriever()
        assert isinstance(retriever, OptimizedRetriever)
        assert len(retriever.chunks) > 0

        results = retriever.search("customs delay", top_k=5)
        assert len(results) > 0


# ---------------------------------------------------------------------------
# 10. test_optimized_evaluation_not_worse_than_baseline_on_seed
# ---------------------------------------------------------------------------


class TestEvaluationComparison:
    """Compare optimized vs baseline on seed eval cases."""

    def test_optimized_evaluation_not_worse_than_baseline_on_seed(self):
        """Optimized retriever should not be worse than baseline on Recall@5 and MRR/Recall@1."""
        from app.eval.retrieval_eval import evaluate_retriever, load_eval_cases
        from app.rag.retriever import build_default_retriever

        cases = load_eval_cases()
        baseline = build_default_retriever()
        optimized = build_default_optimized_retriever()

        base_report = evaluate_retriever(baseline, cases)
        opt_report = evaluate_retriever(optimized, cases)

        # Recall@5 should not degrade
        assert opt_report.recall_at_5 >= base_report.recall_at_5, (
            f"Recall@5 degraded: baseline={base_report.recall_at_5:.4f}, "
            f"optimized={opt_report.recall_at_5:.4f}"
        )

        # At least one of MRR or Recall@1 should not degrade
        mrr_ok = opt_report.mrr >= base_report.mrr
        r1_ok = opt_report.recall_at_1 >= base_report.recall_at_1
        assert mrr_ok or r1_ok, (
            f"Both MRR and Recall@1 degraded: "
            f"baseline MRR={base_report.mrr:.4f}, optimized MRR={opt_report.mrr:.4f}; "
            f"baseline R@1={base_report.recall_at_1:.4f}, optimized R@1={opt_report.recall_at_1:.4f}"
        )


# ---------------------------------------------------------------------------
# 11. test_optimized_fixes_or_improves_known_failed_cases_without_hardcoding
# ---------------------------------------------------------------------------


class TestKnownFailedCasesImproved:
    """Test that common English customs/shipping queries return relevant results."""

    def test_customs_english_delay_returns_customs_content(self):
        """English customs delay query should surface customs-related results in top-k."""
        retriever = build_default_optimized_retriever()
        # This is a general query, not a copy of any eval case
        results = retriever.search("My package has been stuck in customs for 10 days", top_k=5)

        assert len(results) > 0
        top_categories = [r.category for r in results[:3]]
        top_contents = " ".join(r.content for r in results[:3]).lower()

        has_customs = (
            "customs" in top_categories
            or "清关" in top_contents
            or "海关" in top_contents
            or "customs" in top_contents
            or "clearance" in top_contents
        )
        assert has_customs, (
            f"Expected customs-related result in top 3 for English customs query, "
            f"got categories: {top_categories}"
        )

    def test_shipping_customs_compound_query_returns_relevant_results(self):
        """English shipping+customs compound query should surface logistics or customs results."""
        retriever = build_default_optimized_retriever()
        # General compound query about EU shipping with customs
        results = retriever.search(
            "I'm in the EU and my order has been in transit for 3 weeks. The tracking says it's in customs.",
            top_k=5,
        )

        assert len(results) > 0
        top_categories = [r.category for r in results[:5]]
        top_contents = " ".join(r.content for r in results[:5]).lower()

        has_relevant = (
            "logistics" in top_categories
            or "customs" in top_categories
            or "清关" in top_contents
            or "海关" in top_contents
            or "customs" in top_contents
            or "shipping" in top_contents
            or "物流" in top_contents
            or "配送" in top_contents
        )
        assert has_relevant, (
            f"Expected logistics/customs result for EU shipping+customs query, "
            f"got categories: {top_categories}"
        )
