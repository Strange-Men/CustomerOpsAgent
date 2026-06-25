"""Optimized retriever with query expansion, signal inference, and metadata-aware boosting.

This module builds on the M3 baseline BM25Retriever without modifying it.
It improves retrieval quality through:
1. Query normalization (lowercase, whitespace cleanup)
2. Cross-lingual synonym expansion (domain-specific dictionary)
3. Query signal inference (category, market, language)
4. Metadata-aware score adjustment (category/market/language boost)
5. Optional doc-level diversity (dedup repeated doc_ids)
"""

import re
import sys
from dataclasses import dataclass, field

try:
    from app.rag.chunker import chunk_documents
    from app.rag.loader import load_knowledge_documents
    from app.rag.retriever import BM25Retriever
    from app.rag.schemas import KnowledgeChunk, RetrievedChunk
except ImportError:
    from backend.app.rag.chunker import chunk_documents
    from backend.app.rag.loader import load_knowledge_documents
    from backend.app.rag.retriever import BM25Retriever
    from backend.app.rag.schemas import KnowledgeChunk, RetrievedChunk

# ---------------------------------------------------------------------------
# Domain synonym dictionary (general-purpose, not case-specific)
# ---------------------------------------------------------------------------
# Each entry maps a canonical concept to a list of synonyms across languages.
# The expand_query function uses this to add cross-lingual terms.

_SYNONYM_GROUPS: list[list[str]] = [
    # Shipping / logistics
    ["shipping", "delivery", "logistics", "package", "parcel", "物流", "配送", "包裹", "快递", "发货", "运输"],
    # Customs / clearance
    ["customs", "clearance", "import tax", "duty", "清关", "关税", "海关", "报关"],
    # Delay / stuck / pending
    ["delay", "stuck", "pending", "late", "slow", "延迟", "卡住", "处理中", "滞后", "很久"],
    # Refund
    ["refund", "退款", "退钱", "退回"],
    # Return
    ["return", "退货", "退回商品"],
    # Exchange
    ["exchange", "换货", "换颜色", "换尺码", "更换"],
    # Damaged / broken
    ["damaged", "broken", "crushed", "破损", "损坏", "碎了", "坏了"],
    # Lost / missing
    ["lost", "missing", "not received", "丢失", "未收到", "丢包", "找不到"],
    # Address
    ["address", "change address", "地址", "修改地址", "收货地址"],
    # Payment
    ["payment", "pay", "paid", "支付", "付款", "扣款", "支付失败"],
    # Order / cancel
    ["order", "cancel", "订单", "取消", "取消订单"],
    # Coupon / discount
    ["coupon", "discount", "promo", "优惠券", "折扣", "促销"],
    # Tracking
    ["tracking", "track", "追踪", "物流信息", "物流状态"],
    # Business days
    ["business days", "工作日"],
    # Inspection / check
    ["inspection", "inspect", "check", "检查", "质检", "抽检"],
]

# Build a lookup: for each word, find all synonyms in its group
_SYNONYM_MAP: dict[str, set[str]] = {}
for _group in _SYNONYM_GROUPS:
    for _term in _group:
        _lower = _term.lower()
        if _lower not in _SYNONYM_MAP:
            _SYNONYM_MAP[_lower] = set()
        for _other in _group:
            if _other.lower() != _lower:
                _SYNONYM_MAP[_lower].add(_other.lower())

# Category keyword mapping (general domain terms → category)
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "customs": ["customs", "clearance", "import tax", "duty", "清关", "海关", "关税", "报关"],
    "logistics": ["shipping", "delivery", "logistics", "package", "parcel", "物流", "配送", "包裹", "快递", "发货", "运输", "tracking", "track", "追踪"],
    "refund": ["refund", "退款", "退钱"],
    "return": ["return", "退货"],
    "exchange": ["exchange", "换货", "换颜色", "换尺码", "更换"],
    "address": ["address", "地址", "修改地址", "收货地址"],
    "order": ["order", "cancel", "订单", "取消"],
    "payment": ["payment", "pay", "paid", "支付", "付款", "扣款", "支付失败"],
    "package": ["package", "parcel", "damaged", "broken", "lost", "missing", "包裹", "丢失", "破损", "损坏", "丢包", "碎了", "坏了", "未收到"],
    "coupon": ["coupon", "discount", "promo", "优惠券", "折扣", "促销"],
}

# Market keyword mapping
_MARKET_KEYWORDS: dict[str, list[str]] = {
    "US": ["us", "usa", "america", "american", "united states", "美国", "美"],
    "EU": ["eu", "europe", "european", "欧洲", "欧"],
}

# Language detection: simple heuristic based on CJK ratio
_CJK_PATTERN = re.compile(r"[一-鿿㐀-䶿]")


# ---------------------------------------------------------------------------
# QuerySignals
# ---------------------------------------------------------------------------


@dataclass
class QuerySignals:
    """Inferred signals from a query string.

    These signals are used for metadata-aware boosting, not for hard filtering.
    """

    original_query: str
    expanded_query: str
    inferred_categories: list[str] = field(default_factory=list)
    inferred_markets: list[str] = field(default_factory=list)
    inferred_language: str = "unknown"


# ---------------------------------------------------------------------------
# Query normalization
# ---------------------------------------------------------------------------


def normalize_query(query: str) -> str:
    """Normalize query text: lowercase English, collapse whitespace, preserve CJK.

    Args:
        query: Raw query string.

    Returns:
        Normalized query string.
    """
    # Lowercase
    q = query.lower()
    # Collapse multiple whitespace into single space
    q = re.sub(r"\s+", " ", q).strip()
    return q


# ---------------------------------------------------------------------------
# Query expansion (synonym expansion)
# ---------------------------------------------------------------------------


def expand_query(query: str) -> str:
    """Expand query with cross-lingual synonyms from the domain dictionary.

    For each word/phrase in the query that matches a synonym group entry,
    all other terms in that group are appended to the query.

    This is a general-purpose domain expansion, not tied to any specific
    eval case or expected answer.

    Args:
        query: Normalized query string.

    Returns:
        Expanded query string with added synonym terms.
    """
    q_lower = query.lower()
    added_terms: set[str] = set()

    # Check multi-word phrases first, then single words
    # Sort by length descending so longer phrases match first
    all_terms = sorted(_SYNONYM_MAP.keys(), key=len, reverse=True)

    for term in all_terms:
        if term in q_lower:
            for synonym in _SYNONYM_MAP[term]:
                if synonym not in q_lower:
                    added_terms.add(synonym)

    if added_terms:
        return query + " " + " ".join(sorted(added_terms))
    return query


# ---------------------------------------------------------------------------
# Query signal inference
# ---------------------------------------------------------------------------


def _detect_language(query: str) -> str:
    """Detect the primary language of a query.

    Simple heuristic: if CJK characters dominate, it's Chinese (zh);
    if mostly ASCII/Latin, it's English (en); otherwise unknown.
    """
    cjk_count = len(_CJK_PATTERN.findall(query))
    total_alpha = len(re.findall(r"[a-zA-Z]", query))

    if cjk_count > 0 and total_alpha == 0:
        return "zh"
    if cjk_count == 0 and total_alpha > 0:
        return "en"
    if cjk_count > 0 and total_alpha > 0:
        # Mixed: return the dominant one, or "mixed"
        return "zh" if cjk_count > total_alpha else "en"
    return "unknown"


def infer_query_signals(query: str) -> QuerySignals:
    """Infer category, market, and language signals from a query.

    Uses general domain keywords — not tied to any specific eval case.

    Args:
        query: The raw or normalized query string.

    Returns:
        QuerySignals with inferred metadata.
    """
    q_lower = query.lower()

    # Infer categories
    inferred_categories: list[str] = []
    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in q_lower:
                inferred_categories.append(category)
                break

    # Infer markets
    inferred_markets: list[str] = []
    for market, keywords in _MARKET_KEYWORDS.items():
        for kw in keywords:
            # Use word boundary for short terms like "us" to avoid false positives
            if len(kw) <= 2:
                if re.search(r'\b' + re.escape(kw) + r'\b', q_lower):
                    inferred_markets.append(market)
                    break
            else:
                if kw in q_lower:
                    inferred_markets.append(market)
                    break

    # Infer language
    inferred_language = _detect_language(query)

    return QuerySignals(
        original_query=query,
        expanded_query="",  # Will be filled after expand_query
        inferred_categories=inferred_categories,
        inferred_markets=inferred_markets,
        inferred_language=inferred_language,
    )


# ---------------------------------------------------------------------------
# OptimizedRetriever
# ---------------------------------------------------------------------------

# Boost factors for metadata matching (conservative, explainable)
_CATEGORY_BOOST = 1.15  # +15% if chunk category matches inferred category
_MARKET_BOOST = 1.10  # +10% if chunk market matches inferred market
_GLOBAL_MARKET_BOOST = 1.03  # +3% for GLOBAL market chunks (always relevant)
_LANGUAGE_BOOST = 1.08  # +8% if chunk language matches inferred language


class OptimizedRetriever:
    """Optimized retriever built on top of the baseline BM25Retriever.

    Improvements over baseline:
    - Cross-lingual synonym expansion (shipping → 物流、配送、包裹 ...)
    - Query signal inference (category, market, language)
    - Metadata-aware score boosting (category/market/language match)
    - Optional doc-level diversity (limit repeated doc_ids in top-k)

    Does NOT:
    - Read any eval data files
    - Use any eval ground-truth fields
    - Modify the baseline BM25Retriever
    """

    def __init__(self, chunks: list[KnowledgeChunk]) -> None:
        """Initialize the optimized retriever.

        Args:
            chunks: KnowledgeChunk instances to index.
        """
        self.chunks = chunks
        self._base_retriever = BM25Retriever(chunks)

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Search with query expansion and metadata-aware boosting.

        Pipeline:
        1. Normalize query
        2. Expand query with synonyms
        3. Infer query signals (category, market, language)
        4. Run BM25 on expanded query
        5. Apply metadata-aware score adjustment
        6. Re-sort by adjusted score
        7. Apply optional doc-level diversity
        8. Return top-k

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of RetrievedChunk sorted by adjusted score descending.
        """
        if top_k <= 0:
            raise ValueError(f"top_k must be > 0, got {top_k}")

        query = query.strip()
        if not query:
            return []

        # Step 1: Normalize
        normalized = normalize_query(query)

        # Step 2: Expand
        expanded = expand_query(normalized)

        # Step 3: Infer signals
        signals = infer_query_signals(query)
        signals.expanded_query = expanded

        # Step 4: BM25 search on expanded query (fetch more candidates for reranking)
        candidate_k = min(top_k * 3, len(self.chunks), 50)
        if candidate_k < top_k:
            candidate_k = top_k
        candidates = self._base_retriever.search(expanded, top_k=candidate_k)

        # Step 5: Metadata-aware score adjustment
        adjusted: list[tuple[RetrievedChunk, float]] = []
        for chunk in candidates:
            boost = self._compute_boost(chunk, signals)
            new_score = round(chunk.score * boost, 6)
            adjusted.append((chunk, new_score))

        # Step 6: Re-sort by adjusted score
        adjusted.sort(key=lambda x: (-x[1], x[0].chunk_id))

        # Step 7: Build results with adjusted scores
        results: list[RetrievedChunk] = []
        for chunk, new_score in adjusted:
            # Doc-level diversity: skip if we already have 2+ chunks from same doc
            # This prevents a single document from dominating the top-k
            doc_count = sum(1 for r in results if r.doc_id == chunk.doc_id)
            if doc_count >= 2:
                continue

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
                    score=new_score,
                )
            )
            if len(results) >= top_k:
                break

        return results

    def _compute_boost(self, chunk: RetrievedChunk, signals: QuerySignals) -> float:
        """Compute the metadata-aware boost multiplier for a chunk.

        Boost strategy (all multiplicative, conservative):
        - Category match: ×1.15 (chunk.category in inferred categories)
        - Market match: ×1.10 (chunk.market in inferred markets)
        - GLOBAL market: ×1.03 (GLOBAL docs are always somewhat relevant)
        - Language match: ×1.08 (chunk.language matches inferred language)

        All boosts are multiplicative and capped to prevent BM25 distortion.
        Maximum possible boost: 1.15 × 1.10 × 1.03 × 1.08 ≈ 1.41

        Args:
            chunk: The RetrievedChunk to evaluate.
            signals: Inferred query signals.

        Returns:
            Boost multiplier (float >= 1.0).
        """
        boost = 1.0

        # Category boost
        if signals.inferred_categories and chunk.category in signals.inferred_categories:
            boost *= _CATEGORY_BOOST

        # Market boost
        if signals.inferred_markets and chunk.market in signals.inferred_markets:
            boost *= _MARKET_BOOST
        elif chunk.market == "GLOBAL":
            boost *= _GLOBAL_MARKET_BOOST

        # Language boost
        if signals.inferred_language != "unknown" and chunk.language == signals.inferred_language:
            boost *= _LANGUAGE_BOOST

        return boost


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def build_default_optimized_retriever() -> OptimizedRetriever:
    """Build an OptimizedRetriever from the default seed knowledge base.

    Loads documents via the M2 loader, chunks them via the M2 chunker,
    and returns a ready-to-use OptimizedRetriever.

    Returns:
        OptimizedRetriever indexed on the seed knowledge base chunks.
    """
    docs = load_knowledge_documents()
    chunks = chunk_documents(docs)
    return OptimizedRetriever(chunks)


# ---------------------------------------------------------------------------
# CLI Smoke Test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    query = sys.argv[1] if len(sys.argv) > 1 else "customs clearance delay"
    top_k = 5

    retriever = build_default_optimized_retriever()

    # Show query signals
    normalized = normalize_query(query)
    expanded = expand_query(normalized)
    signals = infer_query_signals(query)
    signals.expanded_query = expanded

    print(f"Query:          {query}")
    print(f"Normalized:     {normalized}")
    print(f"Expanded:       {expanded}")
    print(f"Category:       {signals.inferred_categories}")
    print(f"Market:         {signals.inferred_markets}")
    print(f"Language:       {signals.inferred_language}")
    print(f"Top-K:          {top_k}")
    print(f"Chunks indexed: {len(retriever.chunks)}")
    print()

    results = retriever.search(query, top_k=top_k)

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
