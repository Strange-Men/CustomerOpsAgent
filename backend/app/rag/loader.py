"""Load knowledge base documents from JSONL files."""

import json
from pathlib import Path

from app.rag.schemas import KnowledgeDocument


def get_default_knowledge_path() -> Path:
    """Return the default path to the seed knowledge base JSONL file."""
    return Path(__file__).resolve().parent.parent.parent / "data" / "knowledge_base" / "customer_service_seed.jsonl"


def load_jsonl(path: Path | str) -> list[dict]:
    """Load a JSONL file and return a list of raw dicts.

    Args:
        path: Path to a JSONL file.

    Returns:
        List of parsed JSON dicts, one per non-empty line.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a line contains invalid JSON (message includes line number).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Knowledge base file not found: {path}")

    items: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                items.append(json.loads(stripped))
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at {path.name} line {line_num}: {e}") from e
    return items


def load_knowledge_documents(path: Path | str | None = None) -> list[KnowledgeDocument]:
    """Load and validate knowledge documents from a JSONL file.

    Args:
        path: Path to a JSONL file. Defaults to the seed knowledge base.

    Returns:
        List of validated KnowledgeDocument instances.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a line contains invalid JSON (message includes line number).
        pydantic.ValidationError: If a record fails schema validation.
    """
    if path is None:
        path = get_default_knowledge_path()
    raw_items = load_jsonl(path)

    documents: list[KnowledgeDocument] = []
    for i, item in enumerate(raw_items, 1):
        try:
            documents.append(KnowledgeDocument(**item))
        except Exception as e:
            raise ValueError(f"Schema validation failed at line {i}: {e}") from e
    return documents


if __name__ == "__main__":
    docs = load_knowledge_documents()
    print(f"Loaded {len(docs)} documents")

    languages: dict[str, int] = {}
    categories: dict[str, int] = {}
    for doc in docs:
        languages[doc.language] = languages.get(doc.language, 0) + 1
        categories[doc.category] = categories.get(doc.category, 0) + 1

    print(f"Languages: {languages}")
    print(f"Categories: {categories}")
