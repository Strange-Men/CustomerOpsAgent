"""Baseline BM25 retriever for knowledge chunks."""

import math
import re
import sys
from collections import Counter

from app.rag.chunker import chunk_documents
from app.rag.loader import load_knowledge_documents
from app.rag.schemas import KnowledgeChunk, RetrievedChunk

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

# Regex: match English/number words OR individual CJK characters
_TOKEN_PATTERN = re.compile(
    r"[a-z0-9]+|[一-鿿㐀-䶿豈-﫿]"
)


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase English words and CJK character tokens.

    English words are lowercased and split on non-alphanumeric boundaries.
    CJK characters are returned individually (char-level tokenization).
    Empty tokens are filtered out.

    Args:
        text: Input text to tokenize.

    Returns:
        List of non-empty tokens.
    """
    return _TOKEN_PATTERN.findall(text.lower())


# ---------------------------------------------------------------------------
# BM25 Retriever
# ---------------------------------------------------------------------------

_K1 = 1.5
_B = 0.75


class BM25Retriever:
    """Baseline BM25 keyword retriever over KnowledgeChunks.

    Implements the standard BM25 scoring function:
        score(D, Q) = Σ IDF(qi) * (f(qi,D) * (k1+1)) / (f(qi,D) + k1 * (1 - b + b * |D|/avgdl))

    Attributes:
        chunks: The original KnowledgeChunk list.
        k1: Term frequency saturation parameter (default 1.5).
        b: Document length normalization parameter (default 0.75).
    """

    def __init__(
        self,
        chunks: list[KnowledgeChunk],
        k1: float = _K1,
        b: float = _B,
    ) -> None:
        """Initialize the BM25 index from a list of chunks.

        Args:
            chunks: KnowledgeChunk instances to index.
            k1: Term frequency saturation parameter.
            b: Document length normalization parameter.
        """
        self.chunks = chunks
        self.k1 = k1
        self.b = b

        # Pre-compute per-chunk token counts and lengths
        self._doc_tokens: list[Counter] = []
        self._doc_lengths: list[int] = []
        for chunk in chunks:
            tokens = tokenize(chunk.content)
            self._doc_tokens.append(Counter(tokens))
            self._doc_lengths.append(len(tokens))

        # Corpus statistics
        self._num_docs = len(chunks)
        self._avgdl = (
            sum(self._doc_lengths) / self._num_docs if self._num_docs > 0 else 0.0
        )

        # Document frequency: how many chunks contain each token
        self._df: Counter = Counter()
        for token_set in (set(tc.keys()) for tc in self._doc_tokens):
            for token in token_set:
                self._df[token] += 1

    def _idf(self, token: str) -> float:
        """Compute IDF weight for a token.

        Uses the standard BM25 IDF formula:
            IDF(q) = log((N - n(q) + 0.5) / (n(q) + 0.5) + 1)
        """
        n = self._df.get(token, 0)
        return math.log((self._num_docs - n + 0.5) / (n + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Search for the top-k most relevant chunks.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return. Must be > 0.

        Returns:
            List of RetrievedChunk sorted by score descending.

        Raises:
            ValueError: If top_k <= 0.
        """
        if top_k <= 0:
            raise ValueError(f"top_k must be > 0, got {top_k}")

        query = query.strip()
        if not query or self._num_docs == 0:
            return []

        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        # Score every chunk
        scored: list[tuple[int, float]] = []
        for doc_idx in range(self._num_docs):
            score = self._score_document(doc_idx, query_tokens)
            if score > 0:
                scored.append((doc_idx, score))

        # Sort by score descending, then by chunk_id for stability
        scored.sort(key=lambda x: (-x[1], self.chunks[x[0]].chunk_id))

        # Build RetrievedChunk results
        results: list[RetrievedChunk] = []
        for doc_idx, score in scored[:top_k]:
            chunk = self.chunks[doc_idx]
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    title=chunk.title,
                    category=chunk.category,
                    market=chunk.market,
                    language=chunk.language,
                    policy_type=chunk.policy_type,
                    priority=chunk.priority,
                    source=chunk.source,
                    content=chunk.content,
                    chunk_index=chunk.chunk_index,
                    score=round(score, 6),
                )
            )
        return results

    def _score_document(self, doc_idx: int, query_tokens: list[str]) -> float:
        """Compute the BM25 score for a single document against query tokens."""
        doc_tf = self._doc_tokens[doc_idx]
        doc_len = self._doc_lengths[doc_idx]

        score = 0.0
        for qt in query_tokens:
            tf = doc_tf.get(qt, 0)
            if tf == 0:
                continue
            idf = self._idf(qt)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self._avgdl)
            score += idf * numerator / denominator
        return score


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def build_default_retriever() -> BM25Retriever:
    """Build a BM25Retriever from the default seed knowledge base.

    Loads documents via the M2 loader, chunks them via the M2 chunker,
    and returns a ready-to-use BM25Retriever.

    Returns:
        BM25Retriever indexed on the seed knowledge base chunks.
    """
    docs = load_knowledge_documents()
    chunks = chunk_documents(docs)
    return BM25Retriever(chunks)


# ---------------------------------------------------------------------------
# CLI Smoke Test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    query = sys.argv[1] if len(sys.argv) > 1 else "清关延迟怎么办"
    top_k = 5

    retriever = build_default_retriever()
    results = retriever.search(query, top_k=top_k)

    print(f"Query: {query}")
    print(f"Top-K: {top_k}")
    print(f"Chunks indexed: {len(retriever.chunks)}")
    print(f"Results returned: {len(results)}")
    print()

    for i, r in enumerate(results, 1):
        preview = r.content[:80].replace("\n", " ")
        if len(r.content) > 80:
            preview += "..."
        print(f"  [{i}] score={r.score:.4f}  chunk_id={r.chunk_id}")
        print(f"      doc_id={r.doc_id}  category={r.category}  market={r.market}")
        print(f"      language={r.language}  title={r.title}")
        print(f"      content: {preview}")
        print()
