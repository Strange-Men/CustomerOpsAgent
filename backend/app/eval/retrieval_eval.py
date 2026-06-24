"""Retrieval evaluation harness.

Loads eval cases, runs the baseline BM25 retriever, and computes
Recall@1 / Recall@3 / Recall@5 / MRR metrics.
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path

from app.rag.retriever import BM25Retriever, build_default_retriever
from app.rag.schemas import EvalCase, RetrievedChunk


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def get_default_eval_cases_path() -> Path:
    """Return the default path to the seed eval cases JSONL file."""
    return Path(__file__).resolve().parent.parent.parent / "data" / "eval_cases_seed.jsonl"


# ---------------------------------------------------------------------------
# Load eval cases
# ---------------------------------------------------------------------------

def load_eval_cases(path: Path | str | None = None) -> list[EvalCase]:
    """Load and validate eval cases from a JSONL file.

    Args:
        path: Path to the JSONL file. Defaults to the seed eval cases.

    Returns:
        List of validated EvalCase instances.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a JSON line is malformed or fails schema validation.
    """
    if path is None:
        path = get_default_eval_cases_path()
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Eval cases file not found: {path}")

    cases: list[EvalCase] = []
    with open(path, encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_num}: {exc}"
                ) from exc
            try:
                case = EvalCase(**data)
            except Exception as exc:
                raise ValueError(
                    f"Schema validation failed on line {line_num}: {exc}"
                ) from exc
            cases.append(case)
    return cases


# ---------------------------------------------------------------------------
# Unique doc IDs
# ---------------------------------------------------------------------------

def unique_doc_ids_from_results(results: list[RetrievedChunk]) -> list[str]:
    """Extract unique doc_ids from retrieval results, preserving order.

    If the same doc_id appears in multiple chunks, only the first occurrence
    is kept. This prevents a single document with multiple chunks from
    inflating evaluation hit counts.

    Args:
        results: RetrievedChunk list from a retriever search.

    Returns:
        Ordered list of unique doc_ids.
    """
    seen: set[str] = set()
    unique_ids: list[str] = []
    for chunk in results:
        if chunk.doc_id not in seen:
            seen.add(chunk.doc_id)
            unique_ids.append(chunk.doc_id)
    return unique_ids


# ---------------------------------------------------------------------------
# Hit / RR helpers
# ---------------------------------------------------------------------------

def hit_at_k(expected_doc_ids: list[str], retrieved_doc_ids: list[str], k: int) -> bool:
    """Check whether any expected doc_id appears in the top-k retrieved doc_ids.

    Args:
        expected_doc_ids: The ground-truth doc IDs.
        retrieved_doc_ids: Ordered unique doc IDs from retrieval.
        k: Number of top positions to check. Must be > 0.

    Returns:
        True if at least one expected doc_id is found in retrieved_doc_ids[:k].
    """
    if k <= 0:
        return False
    top_k = set(retrieved_doc_ids[:k])
    return any(doc_id in top_k for doc_id in expected_doc_ids)


def reciprocal_rank(expected_doc_ids: list[str], retrieved_doc_ids: list[str]) -> float:
    """Compute the reciprocal rank for a single query.

    Finds the first retrieved doc_id that is in expected_doc_ids and
    returns 1 / rank (rank is 1-based). Returns 0.0 if no hit.

    Args:
        expected_doc_ids: The ground-truth doc IDs.
        retrieved_doc_ids: Ordered unique doc IDs from retrieval.

    Returns:
        Reciprocal rank value (0.0 to 1.0).
    """
    expected_set = set(expected_doc_ids)
    for rank, doc_id in enumerate(retrieved_doc_ids, start=1):
        if doc_id in expected_set:
            return 1.0 / rank
    return 0.0


# ---------------------------------------------------------------------------
# Per-case result
# ---------------------------------------------------------------------------

@dataclass
class CaseResult:
    """Evaluation result for a single eval case."""

    case_id: str
    question: str
    category: str
    market: str
    language: str
    difficulty: str
    expected_doc_ids: list[str]
    retrieved_doc_ids: list[str]
    retrieved_chunk_ids: list[str]
    top_scores: list[float]
    hit_at_1: bool
    hit_at_3: bool
    hit_at_5: bool
    reciprocal_rank: float


# ---------------------------------------------------------------------------
# Aggregate report
# ---------------------------------------------------------------------------

@dataclass
class EvalReport:
    """Aggregate retrieval evaluation report."""

    total_cases: int
    recall_at_1: float
    recall_at_3: float
    recall_at_5: float
    mrr: float
    failed_cases: list[CaseResult]
    per_case_results: list[CaseResult]


# ---------------------------------------------------------------------------
# Evaluate a single case
# ---------------------------------------------------------------------------

def evaluate_case(
    case: EvalCase,
    retriever: BM25Retriever,
    top_k: int = 5,
) -> CaseResult:
    """Evaluate a single eval case against a retriever.

    IMPORTANT: expected_doc_ids are used ONLY for scoring, never passed
    to the retriever. The retriever.search call receives only the question.

    Args:
        case: The eval case to evaluate.
        retriever: A BM25Retriever instance.
        top_k: Number of top results to retrieve.

    Returns:
        CaseResult with all metrics for this case.
    """
    results = retriever.search(case.question, top_k=top_k)

    retrieved_doc_ids = unique_doc_ids_from_results(results)
    retrieved_chunk_ids = [r.chunk_id for r in results]
    top_scores = [r.score for r in results]

    return CaseResult(
        case_id=case.case_id,
        question=case.question,
        category=case.category,
        market=case.market,
        language=case.language,
        difficulty=case.difficulty,
        expected_doc_ids=list(case.expected_doc_ids),
        retrieved_doc_ids=retrieved_doc_ids,
        retrieved_chunk_ids=retrieved_chunk_ids,
        top_scores=top_scores,
        hit_at_1=hit_at_k(case.expected_doc_ids, retrieved_doc_ids, k=1),
        hit_at_3=hit_at_k(case.expected_doc_ids, retrieved_doc_ids, k=3),
        hit_at_5=hit_at_k(case.expected_doc_ids, retrieved_doc_ids, k=5),
        reciprocal_rank=reciprocal_rank(case.expected_doc_ids, retrieved_doc_ids),
    )


# ---------------------------------------------------------------------------
# Evaluate all cases
# ---------------------------------------------------------------------------

def evaluate_retriever(
    retriever: BM25Retriever,
    cases: list[EvalCase],
    top_k: int = 5,
) -> EvalReport:
    """Run evaluation across all cases and compute aggregate metrics.

    Args:
        retriever: A BM25Retriever instance.
        cases: List of eval cases to evaluate.
        top_k: Number of top results to retrieve per case.

    Returns:
        EvalReport with aggregate metrics and per-case results.
    """
    per_case_results = [evaluate_case(case, retriever, top_k) for case in cases]

    total = len(per_case_results)
    if total == 0:
        return EvalReport(
            total_cases=0,
            recall_at_1=0.0,
            recall_at_3=0.0,
            recall_at_5=0.0,
            mrr=0.0,
            failed_cases=[],
            per_case_results=[],
        )

    recall_at_1 = sum(1 for r in per_case_results if r.hit_at_1) / total
    recall_at_3 = sum(1 for r in per_case_results if r.hit_at_3) / total
    recall_at_5 = sum(1 for r in per_case_results if r.hit_at_5) / total
    mrr = sum(r.reciprocal_rank for r in per_case_results) / total
    failed_cases = [r for r in per_case_results if not r.hit_at_5]

    return EvalReport(
        total_cases=total,
        recall_at_1=recall_at_1,
        recall_at_3=recall_at_3,
        recall_at_5=recall_at_5,
        mrr=mrr,
        failed_cases=failed_cases,
        per_case_results=per_case_results,
    )


# ---------------------------------------------------------------------------
# Default evaluation
# ---------------------------------------------------------------------------

def run_default_evaluation() -> EvalReport:
    """Run the default baseline evaluation on seed eval cases.

    Builds the default BM25 retriever, loads seed eval cases,
    and runs full evaluation.

    Returns:
        EvalReport with all metrics.
    """
    retriever = build_default_retriever()
    cases = load_eval_cases()
    return evaluate_retriever(retriever, cases)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 60)
    print("  Retrieval Evaluation — Baseline BM25 Retriever")
    print("=" * 60)
    print()

    report = run_default_evaluation()

    print(f"Total cases:   {report.total_cases}")
    print(f"Recall@1:      {report.recall_at_1:.2%}")
    print(f"Recall@3:      {report.recall_at_3:.2%}")
    print(f"Recall@5:      {report.recall_at_5:.2%}")
    print(f"MRR:           {report.mrr:.4f}")
    print(f"Failed cases:  {len(report.failed_cases)}")
    print()

    if report.failed_cases:
        print("-" * 60)
        print("  Failed Cases (hit_at_5 = False)")
        print("-" * 60)
        for fc in report.failed_cases:
            print(f"  case_id:          {fc.case_id}")
            print(f"  question:         {fc.question}")
            print(f"  expected_doc_ids: {fc.expected_doc_ids}")
            print(f"  retrieved_doc_ids:{fc.retrieved_doc_ids}")
            print()
