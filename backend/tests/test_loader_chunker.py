"""Tests for knowledge loader and chunker."""

from pathlib import Path

import pytest

from app.rag.chunker import chunk_document, chunk_documents, split_text_by_chars
from app.rag.loader import load_knowledge_documents, load_jsonl
from app.rag.schemas import KnowledgeDocument

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
KB_FILE = DATA_DIR / "knowledge_base" / "customer_service_seed.jsonl"


# ---------------------------------------------------------------------------
# Loader Tests
# ---------------------------------------------------------------------------


class TestLoader:
    """Test JSONL loading and KnowledgeDocument validation."""

    def test_load_knowledge_documents_from_seed(self):
        """Seed knowledge base loads and produces >= 12 KnowledgeDocuments."""
        docs = load_knowledge_documents(KB_FILE)
        assert len(docs) >= 12, f"Expected >= 12 docs, got {len(docs)}"
        for doc in docs:
            assert isinstance(doc, KnowledgeDocument)

    def test_loader_preserves_metadata(self):
        """Loaded docs retain doc_id, category, market, language, policy_type, source."""
        docs = load_knowledge_documents(KB_FILE)
        doc = docs[0]
        assert doc.doc_id
        assert doc.category
        assert doc.market
        assert doc.language in ("zh", "en")
        assert doc.policy_type
        assert doc.source

    def test_loader_reports_bad_json_line(self, tmp_path):
        """Loader raises ValueError with line info on malformed JSON."""
        bad_file = tmp_path / "bad.jsonl"
        bad_file.write_text('{"doc_id": "ok"}\nNOT JSON\n{"doc_id": "ok2"}\n', encoding="utf-8")

        with pytest.raises(ValueError, match="line 2"):
            load_jsonl(bad_file)

    def test_loader_file_not_found(self, tmp_path):
        """Loader raises FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            load_knowledge_documents(tmp_path / "nonexistent.jsonl")


# ---------------------------------------------------------------------------
# Chunker Tests
# ---------------------------------------------------------------------------


def _make_short_doc() -> KnowledgeDocument:
    """Create a short test document."""
    return KnowledgeDocument(
        doc_id="test-short-001",
        title="Short Test",
        category="logistics",
        market="US",
        language="en",
        policy_type="shipping",
        priority=1,
        source="test",
        content="This is a short document for testing.",
    )


def _make_long_doc(length: int = 500) -> KnowledgeDocument:
    """Create a long test document with specified content length."""
    return KnowledgeDocument(
        doc_id="test-long-001",
        title="Long Test",
        category="customs",
        market="EU",
        language="zh",
        policy_type="customs",
        priority=2,
        source="test",
        content="A" * length,
    )


class TestChunker:
    """Test text splitting and document chunking."""

    def test_chunk_single_short_document(self):
        """A short document produces exactly 1 chunk with matching metadata."""
        doc = _make_short_doc()
        chunks = chunk_document(doc, max_chars=320, overlap=40)

        assert len(chunks) == 1
        c = chunks[0]
        assert c.doc_id == doc.doc_id
        assert c.title == doc.title
        assert c.category == doc.category
        assert c.market == doc.market
        assert c.language == doc.language
        assert c.policy_type == doc.policy_type
        assert c.source == doc.source
        assert c.content == doc.content
        assert c.chunk_index == 0

    def test_chunk_long_document_with_overlap(self):
        """A long document produces multiple chunks with stable IDs and overlap."""
        doc = _make_long_doc(500)
        chunks = chunk_document(doc, max_chars=100, overlap=20)

        assert len(chunks) > 1, f"Expected multiple chunks, got {len(chunks)}"
        # chunk_id stability
        assert chunks[0].chunk_id == "test-long-001::chunk_000"
        assert chunks[1].chunk_id == "test-long-001::chunk_001"
        # chunk_index starts at 0
        for i, c in enumerate(chunks):
            assert c.chunk_index == i
            assert c.content  # non-empty

    def test_chunk_documents_from_seed(self):
        """Chunking seed docs produces >= docs count chunks, all IDs unique."""
        docs = load_knowledge_documents(KB_FILE)
        chunks = chunk_documents(docs)

        assert len(chunks) >= len(docs), (
            f"Expected >= {len(docs)} chunks, got {len(chunks)}"
        )
        # All chunk_ids unique
        chunk_ids = [c.chunk_id for c in chunks]
        assert len(chunk_ids) == len(set(chunk_ids)), "Duplicate chunk_ids found"
        # All content non-empty
        for c in chunks:
            assert c.content, f"Empty content in chunk {c.chunk_id}"

    def test_invalid_chunk_config(self):
        """Invalid max_chars or overlap raises ValueError."""
        doc = _make_short_doc()
        with pytest.raises(ValueError, match="max_chars must be > 0"):
            chunk_document(doc, max_chars=0, overlap=10)
        with pytest.raises(ValueError, match="max_chars must be > 0"):
            chunk_document(doc, max_chars=-1, overlap=10)
        with pytest.raises(ValueError, match="overlap.*must be < max_chars"):
            chunk_document(doc, max_chars=100, overlap=100)
        with pytest.raises(ValueError, match="overlap.*must be < max_chars"):
            chunk_document(doc, max_chars=100, overlap=150)

    def test_chunk_preserves_language_and_market(self):
        """Language and market metadata survive chunking."""
        docs = load_knowledge_documents(KB_FILE)
        chunks = chunk_documents(docs)

        for c in chunks:
            assert c.language in ("zh", "en"), f"Bad language in chunk {c.chunk_id}"
            assert c.market in ("US", "EU", "GLOBAL"), f"Bad market in chunk {c.chunk_id}"

    def test_split_text_by_chars_short_text(self):
        """Text shorter than max_chars returns a single segment."""
        segments = split_text_by_chars("hello", max_chars=100, overlap=10)
        assert segments == ["hello"]

    def test_split_text_by_chars_generates_overlap(self):
        """Overlapping segments share characters at the boundary."""
        text = "ABCDEFGHIJ"  # 10 chars
        segments = split_text_by_chars(text, max_chars=4, overlap=2)
        # First: ABCD, second: CDEF, third: EFGH, fourth: GHIJ, fifth: IJ
        assert len(segments) >= 2
        # Check overlap: last 2 of segment[0] == first 2 of segment[1]
        assert segments[0][-2:] == segments[1][:2]
