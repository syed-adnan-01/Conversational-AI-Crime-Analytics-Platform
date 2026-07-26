"""Recommendation engine for investigation actions."""

from __future__ import annotations

from typing import Iterable

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score
from app.ai.investigation.intelligence.investigation_models import (
    CompletenessReport,
    Contradiction,
    EvidenceInsight,
    LegalInsight,
    Recommendation,
    SimilarityResult,
    TimelineInsight,
)


def build_recommendations(
    completeness: CompletenessReport,
    evidence_insights: Iterable[EvidenceInsight],
    timeline_insight: TimelineInsight,
    contradictions: Iterable[Contradiction],
    legal_insight: LegalInsight,
    similar_cases: Iterable[SimilarityResult],
) -> list[Recommendation]:
    recommendations: list[Recommendation] = []
    counter = 1

    evidence_list = list(evidence_insights)
    contradictions_list = list(contradictions)
    similar_list = list(similar_cases)

    if completeness.missing_components:
        recommendations.append(
            Recommendation(
                recommendation_id=f"REC-{counter:03d}",
                priority=1,
                confidence=clamp_score(blend_confidence([1.0, completeness.overall_score / 100.0])),
                reason=f"Address missing investigation components: {', '.join(completeness.missing_components)}.",
                affected_entities=completeness.missing_components,
                required_evidence=completeness.missing_components,
                supporting_citations=completeness.missing_components,
                supporting_facts=[f"Completeness score is {completeness.overall_score:.2f}"],
            )
        )
        counter += 1

    weak_evidence = [item for item in evidence_list if item.weak_evidence or item.chain_of_custody_score < 70]
    if weak_evidence:
        recommendations.append(
            Recommendation(
                recommendation_id=f"REC-{counter:03d}",
                priority=2,
                confidence=clamp_score(blend_confidence([0.9, min(item.confidence for item in weak_evidence)])),
                reason="Strengthen weak evidence and verify chain of custody.",
                affected_entities=[item.evidence_id for item in weak_evidence],
                required_evidence=["chain_of_custody_docs", "corroboration"],
                supporting_citations=[ref for item in weak_evidence for ref in item.evidence_references],
                evidence_references=[ref for item in weak_evidence for ref in item.evidence_references],
                supporting_facts=[fact for item in weak_evidence for fact in item.supporting_facts[:2]],
            )
        )
        counter += 1

    if timeline_insight.missing_events or timeline_insight.large_gaps or timeline_insight.impossible_sequences or timeline_insight.time_conflicts:
        recommendations.append(
            Recommendation(
                recommendation_id=f"REC-{counter:03d}",
                priority=2 if not weak_evidence else 3,
                confidence=clamp_score(blend_confidence([timeline_insight.confidence, 0.85])),
                reason="Reconcile timeline gaps and chronology conflicts.",
                affected_entities=timeline_insight.missing_events + timeline_insight.time_conflicts,
                required_evidence=["timeline_log", "event_audit"],
                supporting_citations=timeline_insight.timeline_references,
                timeline_references=timeline_insight.timeline_references,
                supporting_facts=timeline_insight.supporting_facts + timeline_insight.recommendations,
            )
        )
        counter += 1

    if contradictions_list:
        recommendations.append(
            Recommendation(
                recommendation_id=f"REC-{counter:03d}",
                priority=1 if len(contradictions_list) > 1 else 3,
                confidence=clamp_score(blend_confidence([max(item.confidence for item in contradictions_list), 0.8])),
                reason="Resolve contradictions across witness statements, evidence, and notes.",
                affected_entities=[entity for item in contradictions_list for entity in item.source_entities],
                required_evidence=["statement_reverification", "supplementary_note"],
                supporting_citations=[ref for item in contradictions_list for ref in item.evidence_references + item.timeline_references],
                evidence_references=[ref for item in contradictions_list for ref in item.evidence_references],
                timeline_references=[ref for item in contradictions_list for ref in item.timeline_references],
                supporting_facts=[fact for item in contradictions_list for fact in item.supporting_facts[:2]],
            )
        )
        counter += 1

    if legal_insight.legal_risks:
        recommendations.append(
            Recommendation(
                recommendation_id=f"REC-{counter:03d}",
                priority=2,
                confidence=clamp_score(blend_confidence([legal_insight.confidence, 0.9])),
                reason="Complete legal review and documentation for prosecution readiness.",
                affected_entities=legal_insight.missing_legal_documentation or legal_insight.relevant_sections,
                required_evidence=legal_insight.missing_legal_documentation or legal_insight.relevant_sections,
                supporting_citations=legal_insight.evidence_references + legal_insight.timeline_references,
                evidence_references=legal_insight.evidence_references,
                timeline_references=legal_insight.timeline_references,
                supporting_facts=legal_insight.supporting_facts + legal_insight.legal_risks,
            )
        )
        counter += 1

    if similar_list:
        recommendations.append(
            Recommendation(
                recommendation_id=f"REC-{counter:03d}",
                priority=4,
                confidence=clamp_score(blend_confidence([max(item.confidence for item in similar_list), 0.7])),
                reason="Compare the current matter against similar cases for additional leads.",
                affected_entities=[item.case_id for item in similar_list],
                required_evidence=["case_comparison_notes"],
                supporting_citations=[ref for item in similar_list for ref in item.evidence_references + item.timeline_references],
                evidence_references=[ref for item in similar_list for ref in item.evidence_references],
                timeline_references=[ref for item in similar_list for ref in item.timeline_references],
                supporting_facts=[item.reason for item in similar_list[:3]],
            )
        )

    recommendations.sort(key=lambda item: (item.priority, -item.confidence, item.recommendation_id))
    return recommendations
