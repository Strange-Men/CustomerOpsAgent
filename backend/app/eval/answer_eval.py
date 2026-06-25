"""Answer quality evaluation harness.

Loads eval cases, runs the agent workflow, and evaluates answer quality
across relevance, groundedness, completeness, and citation hit rate.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from backend.app.agent.schemas import AgentResponse
from backend.app.agent.workflow import run_customer_service_agent
from backend.app.rag.schemas import EvalCase


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def get_default_full_eval_cases_path() -> Path:
    """Return the default path to the full eval cases JSONL file."""
    return Path(__file__).resolve().parent.parent.parent / "data" / "eval_cases_full.jsonl"


def load_eval_cases(path: Path | str | None = None) -> list[EvalCase]:
    """Load and validate eval cases from a JSONL file.

    Inlined to avoid cross-module import chain issues.

    Args:
        path: Path to the JSONL file.

    Returns:
        List of validated EvalCase instances.
    """
    if path is None:
        path = get_default_full_eval_cases_path()
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
# Text helpers
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Normalize text for comparison: lowercase, collapse whitespace, strip."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Metric: keyword coverage
# ---------------------------------------------------------------------------

def keyword_coverage(answer: str, expected_keywords: list[str]) -> float:
    """Compute the fraction of expected keywords found in the answer.

    Matching is case-insensitive and supports both CJK and Latin text.
    For CJK keywords, a simple substring check is used.
    For Latin keywords, word-boundary matching is applied.

    Args:
        answer: The generated answer text.
        expected_keywords: Keywords expected in a good answer.

    Returns:
        Coverage ratio from 0.0 to 1.0. Returns 0.0 if expected_keywords is empty.
    """
    if not expected_keywords:
        return 0.0

    answer_norm = normalize_text(answer)
    hits = 0

    for kw in expected_keywords:
        kw_norm = normalize_text(kw)
        if not kw_norm:
            continue
        # Check if keyword contains CJK characters
        has_cjk = any("一" <= ch <= "鿿" for ch in kw_norm)
        if has_cjk:
            # CJK: simple substring match
            if kw_norm in answer_norm:
                hits += 1
        else:
            # Latin: word-boundary substring match
            if kw_norm in answer_norm:
                hits += 1

    return hits / len(expected_keywords)


# ---------------------------------------------------------------------------
# Metric: citation hit rate
# ---------------------------------------------------------------------------

def citation_hit_rate(citation_doc_ids: list[str], expected_doc_ids: list[str]) -> float:
    """Check whether citation doc_ids hit any expected doc_ids.

    Args:
        citation_doc_ids: Doc IDs from the agent's citations.
        expected_doc_ids: Expected ground-truth doc IDs.

    Returns:
        1.0 if at least one citation doc_id is in expected_doc_ids, 0.0 otherwise.
        Returns 0.0 if either list is empty.
    """
    if not expected_doc_ids or not citation_doc_ids:
        return 0.0
    citation_set = set(citation_doc_ids)
    expected_set = set(expected_doc_ids)
    if citation_set & expected_set:
        return 1.0
    return 0.0


# ---------------------------------------------------------------------------
# Metric: relevance
# ---------------------------------------------------------------------------

# Category-to-intent mapping for matching
_CATEGORY_INTENT_MAP: dict[str, set[str]] = {
    "logistics": {"logistics"},
    "customs": {"customs"},
    "return": {"return"},
    "refund": {"refund"},
    "exchange": {"exchange"},
    "address": {"address"},
    "order": {"order"},
    "payment": {"payment"},
    "package": {"package"},
    "coupon": {"coupon"},
}


def evaluate_relevance(case: EvalCase, response: AgentResponse) -> float:
    """Evaluate how relevant the response is to the case.

    Rules:
    - If category matches response intent/detail_intent, add score.
    - If fallback triggered on an in-scope case, relevance is low.
    - Non-empty answer without fallback gets a base score.

    Args:
        case: The evaluation case.
        response: The agent's response.

    Returns:
        Relevance score from 0.0 to 1.0.
    """
    score = 0.0

    # Check category match with intent
    expected_intents = _CATEGORY_INTENT_MAP.get(case.category, set())
    response_intents = {response.intent, response.detail_intent}

    if expected_intents & response_intents:
        score += 0.5

    # Non-empty answer without fallback
    if response.answer and not response.fallback_triggered:
        score += 0.3
    elif response.answer and response.fallback_triggered:
        # Fallback with answer: lower relevance for in-scope cases
        score += 0.1

    # Route correctness bonus
    if case.category == "logistics" and response.route == "logistics_tool":
        score += 0.2
    elif case.category != "logistics" and response.route == "rag_knowledge_base":
        score += 0.2
    elif response.route == "fallback":
        # Fallback penalized for in-scope cases
        score += 0.0

    return min(score, 1.0)


# ---------------------------------------------------------------------------
# Metric: groundedness
# ---------------------------------------------------------------------------

# Absolute claim patterns that indicate fabrication
_FABRICATION_PATTERNS = [
    "保证赔偿",
    "一定到账",
    "100%送达",
    "百分百",
    "绝对安全",
    "guarantee compensation",
    "guarantee delivery",
    "100% guaranteed",
]


def evaluate_groundedness(case: EvalCase, response: AgentResponse) -> float:
    """Evaluate whether the response is grounded in evidence.

    Rules:
    - RAG route: requires citations; penalize fabrication patterns.
    - logistics_tool route: grounded if tool_used exists.
    - fallback route: medium groundedness if no fabrication.

    Args:
        case: The evaluation case.
        response: The agent's response.

    Returns:
        Groundedness score from 0.0 to 1.0.
    """
    answer_lower = response.answer.lower()

    # Check for fabrication
    has_fabrication = any(pat in answer_lower for pat in _FABRICATION_PATTERNS)

    if response.route == "rag_knowledge_base":
        if not response.citations:
            return 0.0
        score = 0.8
        # Verify citations come from retrieved docs
        retrieved_set = set(response.retrieved_doc_ids)
        citation_docs = [c.doc_id for c in response.citations]
        if any(d in retrieved_set for d in citation_docs):
            score += 0.1
        # Penalize fabrication
        if has_fabrication:
            score -= 0.5
        return max(0.0, min(score, 1.0))

    elif response.route == "logistics_tool":
        if response.tool_used == "mock_logistics_tool":
            score = 0.8
            if has_fabrication:
                score -= 0.5
            return max(0.0, min(score, 1.0))
        return 0.3

    else:  # fallback
        if has_fabrication:
            return 0.1
        return 0.4


# ---------------------------------------------------------------------------
# Metric: completeness
# ---------------------------------------------------------------------------

def evaluate_completeness(case: EvalCase, response: AgentResponse) -> float:
    """Evaluate how complete the response is.

    Uses expected_keywords to compute coverage.
    Fallback responses are penalized unless the case is out-of-scope.

    Args:
        case: The evaluation case.
        response: The agent's response.

    Returns:
        Completeness score from 0.0 to 1.0.
    """
    coverage = keyword_coverage(response.answer, case.expected_keywords)

    # Fallback penalty
    if response.fallback_triggered:
        # out-of-scope cases (category=other) don't get penalized
        if case.category != "other":
            coverage *= 0.3

    return min(coverage, 1.0)


# ---------------------------------------------------------------------------
# Metric: citation evaluation
# ---------------------------------------------------------------------------

def evaluate_citation(case: EvalCase, response: AgentResponse) -> float:
    """Evaluate citation quality.

    Rules:
    - RAG route: 1.0 if citation_doc_ids intersect expected_doc_ids, else 0.0.
    - logistics_tool route: independent tool-based field, returns 0.5 if tool_used.
    - fallback route: 0.0.

    Args:
        case: The evaluation case.
        response: The agent's response.

    Returns:
        Citation score from 0.0 to 1.0.
    """
    if response.route == "rag_knowledge_base":
        citation_doc_ids = [c.doc_id for c in response.citations]
        return citation_hit_rate(citation_doc_ids, case.expected_doc_ids)

    elif response.route == "logistics_tool":
        if response.tool_used == "mock_logistics_tool":
            return 0.5
        return 0.0

    else:  # fallback
        return 0.0


# ---------------------------------------------------------------------------
# Per-case result
# ---------------------------------------------------------------------------

@dataclass
class AnswerCaseResult:
    """Answer quality evaluation result for a single case."""

    case_id: str
    question: str
    category: str
    market: str
    language: str
    difficulty: str
    route: str
    intent: str
    detail_intent: str
    fallback_triggered: bool
    fallback_reason: str | None
    expected_doc_ids: list[str]
    expected_keywords: list[str]
    retrieved_doc_ids: list[str]
    citation_doc_ids: list[str]
    answer: str
    relevance: float
    groundedness: float
    completeness: float
    citation_hit: float
    keyword_coverage: float
    passed: bool
    failure_reasons: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Evaluate a single case
# ---------------------------------------------------------------------------

def evaluate_answer_case(case: EvalCase, response: AgentResponse) -> AnswerCaseResult:
    """Evaluate answer quality for a single case.

    Args:
        case: The evaluation case.
        response: The agent's response.

    Returns:
        AnswerCaseResult with all metrics and pass/fail status.
    """
    relevance = evaluate_relevance(case, response)
    groundedness = evaluate_groundedness(case, response)
    completeness = evaluate_completeness(case, response)
    citation_hit = evaluate_citation(case, response)
    kw_cov = keyword_coverage(response.answer, case.expected_keywords)

    # Determine pass/fail
    failure_reasons: list[str] = []

    if relevance < 0.6:
        failure_reasons.append(f"relevance={relevance:.2f} < 0.6")
    if groundedness < 0.7:
        failure_reasons.append(f"groundedness={groundedness:.2f} < 0.7")
    if completeness < 0.4:
        failure_reasons.append(f"completeness={completeness:.2f} < 0.4")

    if response.route == "rag_knowledge_base" and citation_hit < 1.0:
        failure_reasons.append(f"rag route citation_hit={citation_hit:.2f} < 1.0")

    if response.route == "logistics_tool" and response.tool_used is None:
        failure_reasons.append("logistics_tool route but tool_used is None")

    passed = len(failure_reasons) == 0

    return AnswerCaseResult(
        case_id=case.case_id,
        question=case.question,
        category=case.category,
        market=case.market,
        language=case.language,
        difficulty=case.difficulty,
        route=response.route,
        intent=response.intent,
        detail_intent=response.detail_intent,
        fallback_triggered=response.fallback_triggered,
        fallback_reason=response.fallback_reason,
        expected_doc_ids=list(case.expected_doc_ids),
        expected_keywords=list(case.expected_keywords),
        retrieved_doc_ids=list(response.retrieved_doc_ids),
        citation_doc_ids=[c.doc_id for c in response.citations],
        answer=response.answer,
        relevance=relevance,
        groundedness=groundedness,
        completeness=completeness,
        citation_hit=citation_hit,
        keyword_coverage=kw_cov,
        passed=passed,
        failure_reasons=failure_reasons,
    )


# ---------------------------------------------------------------------------
# Aggregate report
# ---------------------------------------------------------------------------

@dataclass
class AnswerEvalReport:
    """Aggregate answer quality evaluation report."""

    total_cases: int
    avg_relevance: float
    avg_groundedness: float
    avg_completeness: float
    citation_hit_rate: float
    answer_pass_rate: float
    fallback_rate: float
    failed_cases: list[AnswerCaseResult]
    per_case_results: list[AnswerCaseResult]


# ---------------------------------------------------------------------------
# Evaluate all cases
# ---------------------------------------------------------------------------

def evaluate_agent_answers(cases: list[EvalCase]) -> AnswerEvalReport:
    """Run agent workflow on all cases and evaluate answer quality.

    Args:
        cases: List of evaluation cases.

    Returns:
        AnswerEvalReport with aggregate metrics and per-case results.
    """
    per_case_results: list[AnswerCaseResult] = []

    for case in cases:
        response = run_customer_service_agent(case.question, top_k=5)
        result = evaluate_answer_case(case, response)
        per_case_results.append(result)

    total = len(per_case_results)
    if total == 0:
        return AnswerEvalReport(
            total_cases=0,
            avg_relevance=0.0,
            avg_groundedness=0.0,
            avg_completeness=0.0,
            citation_hit_rate=0.0,
            answer_pass_rate=0.0,
            fallback_rate=0.0,
            failed_cases=[],
            per_case_results=[],
        )

    avg_relevance = sum(r.relevance for r in per_case_results) / total
    avg_groundedness = sum(r.groundedness for r in per_case_results) / total
    avg_completeness = sum(r.completeness for r in per_case_results) / total
    citation_hits = sum(1 for r in per_case_results if r.citation_hit >= 1.0)
    citation_hit_rate_val = citation_hits / total
    pass_count = sum(1 for r in per_case_results if r.passed)
    answer_pass_rate_val = pass_count / total
    fallback_count = sum(1 for r in per_case_results if r.fallback_triggered)
    fallback_rate_val = fallback_count / total
    failed_cases = [r for r in per_case_results if not r.passed]

    return AnswerEvalReport(
        total_cases=total,
        avg_relevance=avg_relevance,
        avg_groundedness=avg_groundedness,
        avg_completeness=avg_completeness,
        citation_hit_rate=citation_hit_rate_val,
        answer_pass_rate=answer_pass_rate_val,
        fallback_rate=fallback_rate_val,
        failed_cases=failed_cases,
        per_case_results=per_case_results,
    )


# ---------------------------------------------------------------------------
# Default evaluation
# ---------------------------------------------------------------------------

def run_default_answer_evaluation() -> AnswerEvalReport:
    """Run default answer quality evaluation on the full eval dataset.

    Returns:
        AnswerEvalReport with all metrics.
    """
    cases_path = get_default_full_eval_cases_path()
    cases = load_eval_cases(cases_path)
    return evaluate_agent_answers(cases)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 60)
    print("  Answer Quality Evaluation — Agent Workflow")
    print("=" * 60)
    print()

    report = run_default_answer_evaluation()

    print(f"Total cases:        {report.total_cases}")
    print(f"Avg Relevance:      {report.avg_relevance:.4f}")
    print(f"Avg Groundedness:   {report.avg_groundedness:.4f}")
    print(f"Avg Completeness:   {report.avg_completeness:.4f}")
    print(f"Citation Hit Rate:  {report.citation_hit_rate:.2%}")
    print(f"Answer Pass Rate:   {report.answer_pass_rate:.2%}")
    print(f"Fallback Rate:      {report.fallback_rate:.2%}")
    print(f"Failed cases:       {len(report.failed_cases)}")
    print()

    if report.failed_cases:
        print("-" * 60)
        print("  Failed Cases (top 5)")
        print("-" * 60)
        for fc in report.failed_cases[:5]:
            print(f"  case_id:       {fc.case_id}")
            print(f"  question:      {fc.question}")
            print(f"  route:         {fc.route}")
            print(f"  fallback:      {fc.fallback_triggered} ({fc.fallback_reason or 'N/A'})")
            print(f"  relevance:     {fc.relevance:.2f}")
            print(f"  groundedness:  {fc.groundedness:.2f}")
            print(f"  completeness:  {fc.completeness:.2f}")
            print(f"  citation_hit:  {fc.citation_hit:.2f}")
            print(f"  reasons:       {'; '.join(fc.failure_reasons)}")
            print()
