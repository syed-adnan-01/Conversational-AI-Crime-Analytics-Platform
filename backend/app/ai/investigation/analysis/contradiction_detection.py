"""Contradiction detection routines."""

from __future__ import annotations

import re
from typing import Iterable

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score
from app.ai.investigation.analysis.pattern_analysis import normalize_text, shared_terms
from app.ai.investigation.intelligence.investigation_models import Contradiction
from app.models.evidence import Evidence
from app.models.officer import OfficerAssignment
from app.models.timeline import TimelineEvent
from app.models.witness import Witness


_NEGATION_MARKERS = {"not", "never", "denies", "deny", "didn't", "didnt", "no", "without", "none"}


def _contains_negation(text: str | None) -> bool:
    normalized = normalize_text(text)
    return any(marker in normalized.split() for marker in _NEGATION_MARKERS)


def _times_in_text(text: str | None) -> list[str]:
    if not text:
        return []
    matches = re.findall(r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm|hours?|hrs?)?\b", text.lower())
    return [match.strip() for match in matches]


def detect_contradictions(
    witnesses: Iterable[Witness],
    evidence: Iterable[Evidence],
    timeline_events: Iterable[TimelineEvent],
    officer_notes: Iterable[OfficerAssignment],
) -> list[Contradiction]:
    witness_list = list(witnesses)
    evidence_list = list(evidence)
    timeline_list = list(timeline_events)
    officer_list = list(officer_notes)

    contradictions: list[Contradiction] = []
    counter = 1

    for witness in witness_list:
        witness_text = witness.statement or ""
        witness_times = _times_in_text(witness_text)
        for source_id, source_text, source_label in [
            *((item.evidence_id or item.evidence_number, item.description or item.title, "evidence") for item in evidence_list),
            *((item.event_id or item.title, item.description or item.title, "timeline") for item in timeline_list),
            *((item.assignment_id or item.officer_id, item.remarks or "", "officer note") for item in officer_list),
        ]:
            shared = shared_terms(witness_text, source_text)
            if not shared:
                continue
            negation_mismatch = _contains_negation(witness_text) != _contains_negation(source_text)
            time_mismatch = False
            if witness_times and _times_in_text(source_text):
                time_mismatch = witness_times != _times_in_text(source_text)
            if negation_mismatch or time_mismatch:
                confidence = clamp_score(
                    blend_confidence(
                        [
                            0.7 if shared else 0.0,
                            0.8 if negation_mismatch else 0.4,
                            0.85 if time_mismatch else 0.35,
                        ]
                    )
                )
                contradictions.append(
                    Contradiction(
                        contradiction_id=f"CON-{counter:03d}",
                        source_entities=[witness.witness_id or witness.name, source_id],
                        description=f"Witness statement conflicts with {source_label} reference.",
                        confidence=confidence,
                        evidence_references=[item.evidence_id for item in evidence_list if item.evidence_id and item.evidence_id == source_id],
                        timeline_references=[item.event_id for item in timeline_list if item.event_id and item.event_id == source_id],
                        supporting_facts=[
                            f"Shared terms: {', '.join(shared[:4])}",
                            "Negation markers differ between the sources." if negation_mismatch else "Source times differ.",
                        ],
                        severity="HIGH" if confidence >= 0.75 else "MEDIUM",
                    )
                )
                counter += 1

    for evidence_item in evidence_list:
        for event in timeline_list:
            shared = shared_terms(evidence_item.description or evidence_item.title, event.description or event.title)
            if len(shared) < 2:
                continue
            if _contains_negation(evidence_item.description) or _contains_negation(event.description):
                confidence = clamp_score(blend_confidence([0.75, 0.7, 0.8]))
                contradictions.append(
                    Contradiction(
                        contradiction_id=f"CON-{counter:03d}",
                        source_entities=[evidence_item.evidence_id or evidence_item.evidence_number, event.event_id or event.title],
                        description="Evidence description conflicts with timeline entry.",
                        confidence=confidence,
                        evidence_references=[evidence_item.evidence_id or evidence_item.evidence_number],
                        timeline_references=[event.event_id or event.title],
                        supporting_facts=[f"Shared terms: {', '.join(shared[:4])}"],
                        severity="MEDIUM",
                    )
                )
                counter += 1

    unique: dict[str, Contradiction] = {}
    for contradiction in contradictions:
        unique[contradiction.description + "|" + ",".join(contradiction.source_entities)] = contradiction
    return list(unique.values())
