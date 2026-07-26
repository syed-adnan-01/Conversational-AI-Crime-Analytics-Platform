"""Evidence analysis routines."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score
from app.ai.investigation.analysis.pattern_analysis import normalize_text, shared_terms, term_overlap_score
from app.ai.investigation.intelligence.investigation_models import EvidenceInsight
from app.models.evidence import CustodyStatus, Evidence, EvidenceCategory, EvidenceStatus, EvidenceType


_STATUS_SCORES = {
    EvidenceStatus.COLLECTED: 0.55,
    EvidenceStatus.SEALED: 0.72,
    EvidenceStatus.UNDER_ANALYSIS: 0.66,
    EvidenceStatus.SUBMITTED: 0.82,
    EvidenceStatus.PRESENTED_IN_COURT: 0.9,
    EvidenceStatus.RETURNED: 0.45,
    EvidenceStatus.DISPOSED: 0.2,
}

_CUSTODY_SCORES = {
    CustodyStatus.IN_CUSTODY: 0.9,
    CustodyStatus.SEALED: 0.95,
    CustodyStatus.RELEASED: 0.45,
    CustodyStatus.DESTROYED: 0.1,
    CustodyStatus.TRANSFERRED: 0.7,
}


def _evidence_signature(evidence: Evidence) -> str:
    return normalize_text(" ".join([evidence.title or "", evidence.description or "", evidence.evidence_number or ""]))


def _categorize_missing(evidence: Evidence, duplicate: bool) -> list[str]:
    missing: list[str] = []
    if not evidence.checksum:
        missing.append("checksum")
    if not evidence.storage_key:
        missing.append("storage_reference")
    if not evidence.mime_type and evidence.evidence_type in {EvidenceType.DIGITAL_DEVICE, EvidenceType.DOCUMENT, EvidenceType.VIDEO, EvidenceType.AUDIO}:
        missing.append("mime_type")
    if evidence.evidence_type in {EvidenceType.FINGERPRINT, EvidenceType.DNA, EvidenceType.BLOOD_SAMPLE, EvidenceType.FORENSIC_REPORT} and evidence.evidence_category != EvidenceCategory.FORENSIC:
        missing.append("forensic_classification")
    if duplicate:
        missing.append("duplicate_review")
    return sorted(set(missing))


def analyze_evidence(case_evidence: Iterable[Evidence]) -> list[EvidenceInsight]:
    evidence_list = list(case_evidence)
    signatures = defaultdict(list)
    for evidence in evidence_list:
        signatures[_evidence_signature(evidence)].append(evidence)

    insights: list[EvidenceInsight] = []
    all_titles = [item.title for item in evidence_list]
    all_descriptions = [item.description for item in evidence_list]

    for evidence in evidence_list:
        signature = _evidence_signature(evidence)
        duplicates = signatures[signature]
        duplicate_detection = len(duplicates) > 1

        status_score = _STATUS_SCORES.get(evidence.status, 0.5)
        custody_score = _CUSTODY_SCORES.get(evidence.custody_status, 0.6)

        type_score = 0.7
        if evidence.evidence_type in {EvidenceType.FORENSIC_REPORT, EvidenceType.DNA, EvidenceType.FINGERPRINT}:
            type_score = 0.92
        elif evidence.evidence_type in {EvidenceType.DIGITAL_DEVICE, EvidenceType.DOCUMENT, EvidenceType.VIDEO, EvidenceType.AUDIO}:
            type_score = 0.8
        elif evidence.evidence_type == EvidenceType.WEAPON:
            type_score = 0.88

        completeness_score = 0.6
        if evidence.checksum:
            completeness_score += 0.15
        if evidence.storage_key:
            completeness_score += 0.1
        if evidence.file_size:
            completeness_score += 0.05

        strength = clamp_score(blend_confidence([status_score, custody_score, type_score, completeness_score])) * 100.0
        importance = clamp_score(
            0.35
            + (0.25 if evidence.accused_id else 0.0)
            + (0.2 if evidence.victim_id else 0.0)
            + (0.15 if evidence.section_id else 0.0)
            + (0.1 if evidence.description else 0.0)
        ) * 100.0

        chain_of_custody = clamp_score(blend_confidence([custody_score, status_score, completeness_score])) * 100.0
        confidence = clamp_score(blend_confidence([status_score, custody_score, type_score, completeness_score]))

        missing_evidence = _categorize_missing(evidence, duplicate_detection)
        weak_evidence: list[str] = []
        if strength < 60:
            weak_evidence.append("low_strength")
        if chain_of_custody < 70:
            weak_evidence.append("weak_chain_of_custody")
        if completeness_score < 0.75:
            weak_evidence.append("incomplete_metadata")

        conflicting_evidence: list[str] = []
        for other in duplicates:
            if other.evidence_id != evidence.evidence_id:
                conflicting_evidence.append(other.evidence_id or other.evidence_number)

        supporting_facts = [
            f"Evidence type is {evidence.evidence_type.value if hasattr(evidence.evidence_type, 'value') else evidence.evidence_type}",
            f"Status is {evidence.status.value if hasattr(evidence.status, 'value') else evidence.status}",
        ]
        if evidence.custody_status:
            supporting_facts.append(f"Custody status is {evidence.custody_status.value if hasattr(evidence.custody_status, 'value') else evidence.custody_status}")

        insights.append(
            EvidenceInsight(
                evidence_id=evidence.evidence_id or evidence.evidence_number,
                title=evidence.title,
                confidence=confidence,
                strength=round(strength, 2),
                importance=round(importance, 2),
                chain_of_custody_score=round(chain_of_custody, 2),
                duplicate_detection=duplicate_detection,
                missing_evidence=missing_evidence,
                weak_evidence=weak_evidence,
                conflicting_evidence=sorted(set(conflicting_evidence)),
                evidence_references=[evidence.evidence_id or evidence.evidence_number],
                timeline_references=[],
                supporting_facts=supporting_facts,
            )
        )

    if evidence_list:
        shared_keywords = sorted(set(shared_terms(all_titles[0], all_descriptions[0])))
        if shared_keywords:
            insights[0].supporting_facts.extend([f"Shared terms: {', '.join(shared_keywords[:5])}"])

    return insights
