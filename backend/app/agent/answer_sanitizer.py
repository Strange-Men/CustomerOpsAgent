"""
CustomerOps Agent - Answer Sanitizer

Post-processing to strip internal system fields from customer-facing answers.
Ensures the answer reads like a natural customer service response,
without leaking doc_id, citation references, or internal metadata.
"""

from __future__ import annotations

import re


# Known internal doc_id patterns (e.g. payment_global_failure_001)
_DOC_ID_PATTERN = re.compile(
    r"[a-z][a-z0-9_]*_[a-z][a-z0-9_]*_\d{3,}",
    re.IGNORECASE,
)

# Patterns that mark the start of an internal citation tail
_CITATION_TAIL_PREFIXES = [
    "证据引用",
    "引用证据",
    "引用：",
    "引用:",
    "参考文档：",
    "参考文档:",
    "参考依据：",
    "参考依据:",
    "文档编号：",
    "文档编号:",
    "doc_id",
    "Doc ID",
    "Doc_ID",
    "【证据】",
    "[证据]",
    "（证据）",
    "(证据)",
    "知识库依据：",
    "知识库依据:",
    "以上信息根据当前知识库",
    "以上信息来源于知识库",
]


def sanitize_customer_answer(answer: str) -> str:
    """
    Strip internal citation tails and doc_id leaks from a customer-facing answer.

    Rules:
    - Remove trailing paragraphs that start with citation keywords
    - Remove parenthesized doc_id lists like (payment_global_failure_001、refund_eu_policy_001)
    - Remove standalone doc_id references at the end of lines
    - Preserve normal business content (amounts, dates, order numbers)
    - Preserve customer service suggestions

    Args:
        answer: Raw answer text from LLM or mock generator

    Returns:
        Cleaned answer text safe for customer-facing display
    """
    if not answer:
        return answer

    text = answer.strip()

    # Step 1: Remove trailing citation paragraphs
    # Split into lines and remove trailing blocks that start with citation keywords
    lines = text.split("\n")
    cutoff = len(lines)

    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        # Check if this line starts with a citation tail prefix
        if any(line.startswith(prefix) for prefix in _CITATION_TAIL_PREFIXES):
            cutoff = i
            continue
        # Check if this line is purely doc_ids in parentheses
        if _is_pure_doc_id_line(line):
            cutoff = i
            continue
        # Once we hit a non-citation line going backwards, stop
        if line and not any(line.startswith(prefix) for prefix in _CITATION_TAIL_PREFIXES):
            break

    if cutoff < len(lines):
        lines = lines[:cutoff]

    text = "\n".join(lines).strip()

    # Step 2: Remove inline parenthesized doc_id lists
    # Match patterns like (payment_global_failure_001、refund_eu_policy_001)
    text = re.sub(
        r"[（(]\s*[a-z][a-z0-9_]*_\d{3,}(?:\s*[、,，]\s*[a-z][a-z0-9_]*_\d{3,})*\s*[）)]",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Step 3: Remove trailing doc_id references on the same line
    # e.g. "建议您重新支付。 payment_global_failure_001"
    text = re.sub(
        r"\s+[a-z][a-z0-9_]*_\d{3,}(?:\s*[、,，]\s*[a-z][a-z0-9_]*_\d{3,})*\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Step 4: Remove "以上信息根据当前知识库（xxx）。" tails
    text = re.sub(
        r"以上信息[根来]据[当前]*知识库[（(][^）)]*[）)]。\s*$",
        "",
        text,
    )
    text = re.sub(
        r"以上信息[根来]据[当前]*知识库。\s*$",
        "",
        text,
    )

    # Step 5: Clean up excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    return text


def _is_pure_doc_id_line(line: str) -> bool:
    """Check if a line is purely doc_ids (possibly in parentheses with separators)."""
    if not line:
        return False
    # Remove parentheses and separators
    cleaned = re.sub(r"[（()）]", "", line)
    cleaned = re.sub(r"[、,，]", " ", cleaned)
    cleaned = cleaned.strip()
    if not cleaned:
        return False
    # Check if all tokens look like doc_ids
    tokens = cleaned.split()
    return all(_DOC_ID_PATTERN.fullmatch(t) for t in tokens) and len(tokens) > 0
