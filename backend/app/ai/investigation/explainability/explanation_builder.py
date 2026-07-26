"""Build the public reasoning trace from analysis outputs."""

from __future__ import annotations

from app.ai.investigation.analysis.explainability import build_reasoning_trace
from app.ai.investigation.intelligence.investigation_models import (
    Contradiction,
    EvidenceInsight,
    Recommendation,
    ReasoningTrace,
    SimilarityResult,
    TimelineInsight,
)


def build_explanation(
    case_id: str | None,
    evidence_insights: list[EvidenceInsight],
    timeline_insight: TimelineInsight,
    contradictions: list[Contradiction],
    recommendations: list[Recommendation],
    similar_cases: list[SimilarityResult],
) -> ReasoningTrace:
    return build_reasoning_trace(
        case_id=case_id,
        evidence_insights=evidence_insights,
        timeline_insight=timeline_insight,
        contradictions=contradictions,
        recommendations=recommendations,
        similar_cases=similar_cases,
    )
