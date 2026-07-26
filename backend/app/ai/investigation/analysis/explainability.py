"""Explainability helpers for investigation outputs."""

from __future__ import annotations

from typing import Iterable

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score, level_from_score
from app.ai.investigation.intelligence.investigation_models import (
    Contradiction,
    EvidenceInsight,
    ReasoningTrace,
    ReasoningTraceStep,
    Recommendation,
    SimilarityResult,
    TimelineInsight,
)


def build_reasoning_trace(
    case_id: str | None,
    evidence_insights: Iterable[EvidenceInsight],
    timeline_insight: TimelineInsight,
    contradictions: Iterable[Contradiction],
    recommendations: Iterable[Recommendation],
    similar_cases: Iterable[SimilarityResult],
) -> ReasoningTrace:
    evidence_list = list(evidence_insights)
    contradiction_list = list(contradictions)
    recommendation_list = list(recommendations)
    similar_list = list(similar_cases)

    steps: list[ReasoningTraceStep] = []
    evidence_refs = [ref for item in evidence_list for ref in item.evidence_references]
    timeline_refs = list(timeline_insight.timeline_references)

    steps.append(
        ReasoningTraceStep(
            step="retrieval",
            detail=f"Grounded the investigation with {len(similar_list)} similar-case matches and repository evidence.",
            references=[item.case_id for item in similar_list],
            confidence=clamp_score(blend_confidence([max((item.confidence for item in similar_list), default=0.0), 0.75])),
        )
    )
    steps.append(
        ReasoningTraceStep(
            step="evidence_analysis",
            detail=f"Analyzed {len(evidence_list)} evidence items for strength and chain-of-custody signals.",
            references=evidence_refs,
            confidence=clamp_score(blend_confidence([max((item.confidence for item in evidence_list), default=0.0), 0.8])),
        )
    )
    steps.append(
        ReasoningTraceStep(
            step="timeline_analysis",
            detail=f"Checked chronology for {len(timeline_insight.missing_events)} missing events and {len(timeline_insight.large_gaps)} large gaps.",
            references=timeline_refs,
            confidence=timeline_insight.confidence,
        )
    )
    steps.append(
        ReasoningTraceStep(
            step="contradiction_detection",
            detail=f"Flagged {len(contradiction_list)} contradictions grounded in the current case data.",
            references=[ref for item in contradiction_list for ref in item.evidence_references + item.timeline_references],
            confidence=clamp_score(blend_confidence([max((item.confidence for item in contradiction_list), default=0.0), 0.75])),
        )
    )
    steps.append(
        ReasoningTraceStep(
            step="recommendations",
            detail=f"Prioritized {len(recommendation_list)} actions based on completeness and legal risk.",
            references=[ref for item in recommendation_list for ref in item.supporting_citations],
            confidence=clamp_score(blend_confidence([max((item.confidence for item in recommendation_list), default=0.0), 0.8])),
        )
    )

    overall_confidence = clamp_score(
        blend_confidence(
            [
                max((item.confidence for item in evidence_list), default=0.0),
                timeline_insight.confidence,
                max((item.confidence for item in contradiction_list), default=0.0),
                max((item.confidence for item in recommendation_list), default=0.0),
                max((item.confidence for item in similar_list), default=0.0),
            ]
        )
    )

    return ReasoningTrace(
        trace_id=f"TRACE-{(case_id or 'QUERY').replace(' ', '_')}",
        case_id=case_id,
        summary="Investigation reasoning grounded in repository data, retrieval results, and deterministic analysis.",
        steps=steps,
        confidence=overall_confidence,
        confidence_level=level_from_score(overall_confidence),
        evidence_references=sorted(set(evidence_refs)),
        timeline_references=sorted(set(timeline_refs)),
    )
