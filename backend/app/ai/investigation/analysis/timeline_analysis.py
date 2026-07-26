"""Timeline analysis routines."""

from __future__ import annotations

from typing import Iterable

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score
from app.ai.investigation.intelligence.investigation_models import TimelineInsight
from app.models.arrest import Arrest
from app.models.chargesheet import Chargesheet
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence
from app.models.timeline import TimelineEvent, TimelineEventType
from app.models.witness import Witness


_EXPECTED_EVENT_MAP = {
    "evidence": TimelineEventType.EVIDENCE_COLLECTED,
    "witness": TimelineEventType.WITNESS_ADDED,
    "arrest": TimelineEventType.ARREST_MADE,
    "chargesheet": TimelineEventType.CHARGESHEET_FILED,
    "court": TimelineEventType.COURT_HEARING,
}

_ORDER = [
    TimelineEventType.CASE_CREATED,
    TimelineEventType.COMPLAINANT_ADDED,
    TimelineEventType.VICTIM_ADDED,
    TimelineEventType.ACCUSED_ADDED,
    TimelineEventType.WITNESS_ADDED,
    TimelineEventType.SECTION_ASSIGNED,
    TimelineEventType.EVIDENCE_COLLECTED,
    TimelineEventType.ARREST_MADE,
    TimelineEventType.CHARGESHEET_FILED,
    TimelineEventType.COURT_HEARING,
    TimelineEventType.COURT_ORDER,
    TimelineEventType.CASE_CLOSED,
]


def _event_rank(event_type: TimelineEventType | str) -> int:
    value = event_type.value if hasattr(event_type, "value") else str(event_type)
    for index, expected in enumerate(_ORDER):
        if expected.value == value:
            return index
    return len(_ORDER)


def analyze_timeline(
    timeline_events: Iterable[TimelineEvent],
    evidence: Iterable[Evidence],
    witnesses: Iterable[Witness],
    arrests: Iterable[Arrest],
    chargesheets: Iterable[Chargesheet],
    court_proceedings: Iterable[CourtProceeding],
) -> TimelineInsight:
    events = sorted(list(timeline_events), key=lambda event: event.event_time)
    evidence_list = list(evidence)
    witness_list = list(witnesses)
    arrest_list = list(arrests)
    chargesheet_list = list(chargesheets)
    court_list = list(court_proceedings)

    present_types = {event.event_type for event in events}
    missing_events: list[str] = []
    for collection_name, event_type in _EXPECTED_EVENT_MAP.items():
        expected_presence = {
            "evidence": bool(evidence_list),
            "witness": bool(witness_list),
            "arrest": bool(arrest_list),
            "chargesheet": bool(chargesheet_list),
            "court": bool(court_list),
        }[collection_name]
        if expected_presence and event_type not in present_types:
            missing_events.append(event_type.value)

    large_gaps: list[str] = []
    impossible_sequences: list[str] = []
    time_conflicts: list[str] = []
    chronological_inconsistencies: list[str] = []

    for previous, current in zip(events, events[1:]):
        gap_hours = abs((current.event_time - previous.event_time).total_seconds()) / 3600.0
        if gap_hours >= 6:
            large_gaps.append(
                f"{previous.title} -> {current.title} gap of {gap_hours:.1f} hours"
            )
        if current.event_time < previous.event_time:
            time_conflicts.append(
                f"{current.title} occurs before {previous.title}"
            )
        if _event_rank(current.event_type) < _event_rank(previous.event_type):
            impossible_sequences.append(
                f"{current.event_type.value} appears before {previous.event_type.value}"
            )
        if current.event_time == previous.event_time and current.event_type != previous.event_type:
            chronological_inconsistencies.append(
                f"{previous.title} and {current.title} share the same timestamp"
            )

    recommendations: list[str] = []
    if missing_events:
        recommendations.append("Add or reconcile the missing timeline events.")
    if large_gaps:
        recommendations.append("Document the activities covering the observed time gaps.")
    if impossible_sequences:
        recommendations.append("Verify the event ordering against case records.")
    if time_conflicts:
        recommendations.append("Correct timestamp conflicts in the timeline log.")
    if not recommendations and events:
        recommendations.append("Timeline appears complete and chronologically stable.")

    confidence = clamp_score(
        blend_confidence(
            [
                1.0 if not missing_events else max(0.2, 1.0 - (len(missing_events) * 0.2)),
                1.0 if not large_gaps else max(0.2, 1.0 - (len(large_gaps) * 0.15)),
                1.0 if not impossible_sequences else max(0.2, 1.0 - (len(impossible_sequences) * 0.2)),
                1.0 if not time_conflicts else max(0.2, 1.0 - (len(time_conflicts) * 0.2)),
            ]
        )
    )

    evidence_refs = [event.reference_id for event in events if event.reference_id]
    timeline_refs = [event.event_id for event in events if event.event_id]

    return TimelineInsight(
        missing_events=sorted(set(missing_events)),
        large_gaps=sorted(set(large_gaps)),
        impossible_sequences=sorted(set(impossible_sequences)),
        time_conflicts=sorted(set(time_conflicts)),
        chronological_inconsistencies=sorted(set(chronological_inconsistencies)),
        recommendations=sorted(set(recommendations)),
        confidence=confidence,
        evidence_references=sorted(set(evidence_refs)),
        timeline_references=sorted(set(timeline_refs)),
        supporting_facts=[f"Timeline event count: {len(events)}"],
    )
