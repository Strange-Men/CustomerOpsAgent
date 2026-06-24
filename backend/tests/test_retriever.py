"""Tests for baseline BM25 retriever."""

from pathlib import Path

import pytest

from app.rag.retriever import BM25Retriever, build_default_retriever, tokenize
from app.rag.schemas import KnowledgeChunk

# ---------------------------------------------------------------------------
# Tokenizer Tests
# ---------------------------------------------------------------------------


class TestTokenize:
    """Test the tokenize function for English and Chinese."""

    def test_tokenize_english(self):
        """English sentence produces lowercase word tokens without empties."""
        tokens = tokenize("How long does Shipping take to the US?")
        assert "how" in tokens
        assert "long" in tokens
        assert "shipping" in tokens
        assert "us" in tokens
        # No empty tokens
        assert all(t for t in tokens)

    def test_tokenize_chinese(self):
        """Chinese sentence produces non-empty character-level tokens."""
        tokens = tokenize("清关延迟怎么办")
        assert len(tokens) > 0
        # Each CJK character should be a separate token
        assert "清" in tokens
        assert "关" in tokens
        assert "延" in tokens

    def test_tokenize_mixed(self):
        """Mixed English/Chinese text produces both word and char tokens."""
        tokens = tokenize("订单 order 状态 status")
        assert "订" in tokens
        assert "单" in tokens
        assert "order" in tokens
        assert "status" in tokens

    def test_tokenize_empty_string(self):
        """Empty string produces empty list."""
        assert tokenize("") == []

    def test_tokenize_only_whitespace(self):
        """Whitespace-only string produces empty list."""
        assert tokenize("   ") == []


# ---------------------------------------------------------------------------
# BM25Retriever Tests
# ---------------------------------------------------------------------------


def _make_chunks() -> list[KnowledgeChunk]:
    """Create 3 test chunks with distinct content."""
    return [
        KnowledgeChunk(
            chunk_id="doc-001::chunk_000",
            doc_id="doc-001",
            title="Customs Clearance Guide",
            category="customs",
            market="GLOBAL",
            language="zh",
            policy_type="customs",
            priority=1,
            source="seed",
            content="清关延迟通常由申报信息不完整或海关抽查导致，请确认发票和装箱单是否齐全。",
            chunk_index=0,
        ),
        KnowledgeChunk(
            chunk_id="doc-002::chunk_000",
            doc_id="doc-002",
            title="Shipping Timeframes",
            category="logistics",
            market="US",
            language="en",
            policy_type="shipping",
            priority=1,
            source="seed",
            content="Standard shipping to the US takes 7-15 business days. Express shipping takes 3-5 business days.",
            chunk_index=0,
        ),
        KnowledgeChunk(
            chunk_id="doc-003::chunk_000",
            doc_id="doc-003",
            title="Return Policy",
            category="return",
            market="GLOBAL",
            language="zh",
            policy_type="return",
            priority=2,
            source="seed",
            content="退货需在签收后7天内申请，商品需保持原包装完好，不影响二次销售。",
            chunk_index=0,
        ),
    ]


class TestBM25Retriever:
    """Test BM25Retriever core functionality."""

    def test_retriever_empty_chunks(self):
        """Retriever initialized with empty chunks returns empty results."""
        retriever = BM25Retriever([])
        results = retriever.search("anything")
        assert results == []

    def test_retriever_empty_query(self):
        """Empty or whitespace-only query returns empty results."""
        retriever = BM25Retriever(_make_chunks())
        assert retriever.search("") == []
        assert retriever.search("   ") == []

    def test_retriever_returns_top_k_sorted(self):
        """Results are sorted by score descending and count <= top_k."""
        chunks = _make_chunks()
        retriever = BM25Retriever(chunks)
        results = retriever.search("清关延迟", top_k=3)

        assert len(results) <= 3
        assert len(results) > 0
        # Scores must be in descending order
        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score

    def test_retriever_preserves_metadata(self):
        """RetrievedChunk preserves all metadata fields from KnowledgeChunk."""
        chunks = _make_chunks()
        retriever = BM25Retriever(chunks)
        results = retriever.search("shipping", top_k=5)

        assert len(results) > 0
        r = results[0]
        # All metadata fields must be present and match
        assert r.doc_id == "doc-002"
        assert r.category == "logistics"
        assert r.market == "US"
        assert r.language == "en"
        assert r.policy_type == "shipping"
        assert r.source == "seed"
        assert r.chunk_index == 0

    def test_retriever_search_seed_knowledge_base(self):
        """Searching '清关延迟' on seed KB returns customs-related results."""
        retriever = build_default_retriever()
        results = retriever.search("清关延迟", top_k=5)

        assert len(results) > 0
        # At least one top result should be customs-related
        top_categories = [r.category for r in results[:3]]
        top_contents = [r.content for r in results[:3]]
        has_customs = (
            "customs" in top_categories
            or any("清关" in c or "海关" in c or "customs" in c.lower() for c in top_contents)
        )
        assert has_customs, (
            f"Expected customs-related result in top 3, got categories: {top_categories}"
        )

    def test_retriever_does_not_import_eval_cases(self):
        """retriever.py must not reference eval_cases or expected_doc_ids."""
        source_file = Path(__file__).resolve().parent.parent / "app" / "rag" / "retriever.py"
        content = source_file.read_text(encoding="utf-8")
        assert "eval_cases_seed" not in content, "retriever.py must not import eval_cases"
        assert "expected_doc_ids" not in content, "retriever.py must not use expected_doc_ids"
        assert "expected_keywords" not in content, "retriever.py must not use expected_keywords"

    def test_top_k_limit(self):
        """top_k=3 returns at most 3 results."""
        chunks = _make_chunks()
        retriever = BM25Retriever(chunks)
        results = retriever.search("清关 延迟 退货 物流", top_k=3)
        assert len(results) <= 3

    def test_score_is_non_negative_float(self):
        """All scores are float and >= 0."""
        chunks = _make_chunks()
        retriever = BM25Retriever(chunks)
        results = retriever.search("清关", top_k=5)
        assert len(results) > 0
        for r in results:
            assert isinstance(r.score, float), f"Score must be float, got {type(r.score)}"
            assert r.score >= 0, f"Score must be >= 0, got {r.score}"

    def test_top_k_zero_raises(self):
        """top_k <= 0 raises ValueError."""
        retriever = BM25Retriever(_make_chunks())
        with pytest.raises(ValueError, match="top_k must be > 0"):
            retriever.search("test", top_k=0)
        with pytest.raises(ValueError, match="top_k must be > 0"):
            retriever.search("test", top_k=-1)

    def test_retriever_english_query(self):
        """English query returns relevant English-content chunks."""
        retriever = build_default_retriever()
        results = retriever.search("How long does shipping take to the US?", top_k=5)

        assert len(results) > 0
        # Should find shipping/logistics content
        top_contents = " ".join(r.content for r in results[:3])
        assert "ship" in top_contents.lower() or "logistics" in top_contents.lower() or "deliver" in top_contents.lower()
