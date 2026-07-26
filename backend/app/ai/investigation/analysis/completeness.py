"""Investigation completeness analysis."""

from __future__ import annotations

from typing import Iterable

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score
from app.ai.investigation.intelligence.investigation_models import CompletenessReport
from app.models.arrest import Arrest
from app.models.chargesheet import Chargesheet
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence, EvidenceCategory, EvidenceType
from app.models.section import Section
from app.models.timeline import TimelineEvent
from app.models.victim import Victim
from app.models.witness import Witness


def _category_score(count: int, target: int) -> float:
    if target <= 0:
        return 1.0 if count > 0 else 0.0
    return min(1.0, count / target)


def analyze_completeness(
    evidence: Iterable[Evidence],
    witnesses: Iterable[Witness],
    timeline_events: Iterable[TimelineEvent],
    arrests: Iterable[Arrest],
    chargesheets: Iterable[Chargesheet],
    court_proceedings: Iterable[CourtProceeding],
    sections: Iterable[Section],
    victims: Iterable[Victim],
) -> CompletenessReport:
    evidence_list = list(evidence)
    witness_list = list(witnesses)
    timeline_list = list(timeline_events)
    arrest_list = list(arrests)
    chargesheet_list = list(chargesheets)
    court_list = list(court_proceedings)
    section_list = list(sections)
    victim_list = list(victims)

    evidence_score = clamp_score(_category_score(len(evidence_list), 4) + (0.1 if evidence_list else 0.0))
    witness_score = clamp_score(_category_score(len(witness_list), 3) + (0.1 if witness_list else 0.0))
    timeline_score = clamp_score(_category_score(len(timeline_list), 4) + (0.1 if timeline_list else 0.0))
    arrests_score = clamp_score(_category_score(len(arrest_list), 1))
    forensics_present = any(
        item.evidence_type in {EvidenceType.FORENSIC_REPORT, EvidenceType.FINGERPRINT, EvidenceType.DNA, EvidenceType.BLOOD_SAMPLE}
        or item.evidence_category == EvidenceCategory.FORENSIC
        for item in evidence_list
    )
    forensics_score = 1.0 if forensics_present else (0.35 if evidence_list else 0.0)
    chargesheet_score = 1.0 if chargesheet_list else 0.0
    legal_review_score = 1.0 if chargesheet_list and section_list else (0.45 if section_list else 0.0)
    documents_score = clamp_score(
        blend_confidence(
            [
                1.0 if evidence_list else 0.0,
                1.0 if chargesheet_list else 0.0,
                1.0 if court_list else 0.0,
                1.0 if victim_list else 0.0,
            ]
        )
    )

    overall_score = round(
        (
            evidence_score * 20
            + witness_score * 15
            + timeline_score * 15
            + arrests_score * 10
            + forensics_score * 15
            + chargesheet_score * 10
            + legal_review_score * 10
            + documents_score * 5
        ),
        2,
    )

    missing_components: list[str] = []
    if not evidence_list:
        missing_components.append("evidence")
    if not witness_list:
        missing_components.append("witnesses")
    if not timeline_list:
        missing_components.append("timeline")
    if not arrest_list:
        missing_components.append("arrests")
    if not forensics_present:
        missing_components.append("forensics")
    if not chargesheet_list:
        missing_components.append("chargesheet")
    if not court_list:
        missing_components.append("legal_review")
    if not section_list:
        missing_components.append("documents")

    return CompletenessReport(
        overall_score=overall_score,
        evidence=round(evidence_score * 100, 2),
        witnesses=round(witness_score * 100, 2),
        timeline=round(timeline_score * 100, 2),
        arrests=round(arrests_score * 100, 2),
        forensics=round(forensics_score * 100, 2),
        chargesheet=round(chargesheet_score * 100, 2),
        legal_review=round(legal_review_score * 100, 2),
        documents=round(documents_score * 100, 2),
        missing_components=sorted(set(missing_components)),
    )
