"""Chunk knowledge documents into smaller retrievable pieces."""

try:
    from app.rag.schemas import KnowledgeChunk, KnowledgeDocument
except ImportError:
    from backend.app.rag.schemas import KnowledgeChunk, KnowledgeDocument


def split_text_by_chars(text: str, max_chars: int = 320, overlap: int = 40) -> list[str]:
    """Split text into overlapping segments by character count.

    Args:
        text: The text to split.
        max_chars: Maximum characters per segment.
        overlap: Number of overlapping characters between consecutive segments.

    Returns:
        List of text segments.

    Raises:
        ValueError: If max_chars <= 0 or overlap >= max_chars.
    """
    if max_chars <= 0:
        raise ValueError(f"max_chars must be > 0, got {max_chars}")
    if overlap >= max_chars:
        raise ValueError(f"overlap ({overlap}) must be < max_chars ({max_chars})")

    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        # Move forward by (max_chars - overlap) to create overlap
        start += max_chars - overlap

    # Remove trailing empty chunk if any
    return [c for c in chunks if c.strip()]


def chunk_document(
    document: KnowledgeDocument,
    max_chars: int = 320,
    overlap: int = 40,
) -> list[KnowledgeChunk]:
    """Split a single KnowledgeDocument into KnowledgeChunks.

    Args:
        document: The document to chunk.
        max_chars: Maximum characters per chunk.
        overlap: Overlapping characters between consecutive chunks.

    Returns:
        List of KnowledgeChunk instances with inherited metadata.
    """
    segments = split_text_by_chars(document.content, max_chars=max_chars, overlap=overlap)

    chunks: list[KnowledgeChunk] = []
    for idx, segment in enumerate(segments):
        chunk_id = f"{document.doc_id}::chunk_{idx:03d}"
        chunks.append(
            KnowledgeChunk(
                chunk_id=chunk_id,
                doc_id=document.doc_id,
                title=document.title,
                category=document.category,
                market=document.market,
                language=document.language,
                policy_type=document.policy_type,
                priority=document.priority,
                source=document.source,
                content=segment,
                chunk_index=idx,
            )
        )
    return chunks


def chunk_documents(
    documents: list[KnowledgeDocument],
    max_chars: int = 320,
    overlap: int = 40,
) -> list[KnowledgeChunk]:
    """Chunk a list of KnowledgeDocuments into KnowledgeChunks.

    Args:
        documents: List of documents to chunk.
        max_chars: Maximum characters per chunk.
        overlap: Overlapping characters between consecutive chunks.

    Returns:
        Flat list of all KnowledgeChunk instances from all documents.
    """
    all_chunks: list[KnowledgeChunk] = []
    for doc in documents:
        all_chunks.extend(chunk_document(doc, max_chars=max_chars, overlap=overlap))
    return all_chunks


if __name__ == "__main__":
    try:
        from app.rag.loader import load_knowledge_documents
    except ImportError:
        from backend.app.rag.loader import load_knowledge_documents

    docs = load_knowledge_documents()
    chunks = chunk_documents(docs)

    total_len = sum(len(c.content) for c in chunks)
    avg_len = total_len / len(chunks) if chunks else 0

    print(f"Documents: {len(docs)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Avg chunk length: {avg_len:.0f} chars")

    languages: dict[str, int] = {}
    categories: dict[str, int] = {}
    for c in chunks:
        languages[c.language] = languages.get(c.language, 0) + 1
        categories[c.category] = categories.get(c.category, 0) + 1

    print(f"Languages: {languages}")
    print(f"Categories: {categories}")
