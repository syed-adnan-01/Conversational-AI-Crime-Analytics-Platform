"""Legal analysis routines."""

from __future__ import annotations

from collections import OrderedDict
from typing import Iterable

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score, level_from_score
from app.ai.investigation.analysis.pattern_analysis import compact_phrases
from app.ai.investigation.intelligence.investigation_models import LegalInsight
from app.models.arrest import Arrest
from app.models.chargesheet import Chargesheet
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence
from app.models.section import Section
from app.repository.act_repository import ActRepository


def analyze_legal(
    sections: Iterable[Section],
    evidence: Iterable[Evidence],
    arrests: Iterable[Arrest],
    chargesheets: Iterable[Chargesheet],
    court_proceedings: Iterable[CourtProceeding],
) -> LegalInsight:
    section_list = list(sections)
    evidence_list = list(evidence)
    arrest_list = list(arrests)
    chargesheet_list = list(chargesheets)
    court_list = list(court_proceedings)

    act_ids = list(OrderedDict.fromkeys(section.act_id for section in section_list if section.act_id))
    acts: list[str] = []
    for act_id in act_ids:
        act = ActRepository.get_act_by_id(act_id)
        if act:
            acts.append(f"{act.short_name} ({act.name})")
        else:
            acts.append(act_id)

    relevant_sections = []
    for section in section_list:
        label = f"{section.section_number} - {section.title}"
        relevant_sections.append(label)

    precedents_placeholder = [
        f"Research comparable precedents for {section.section_number}" for section in section_list[:3]
    ] or ["Comparable precedent research required"]

    legal_risks: list[str] = []
    missing_docs: list[str] = []
    if not chargesheet_list:
        legal_risks.append("Chargesheet not filed yet")
        missing_docs.append("chargesheet")
    if not court_list:
        legal_risks.append("No court proceeding record found")
        missing_docs.append("court_proceedings")
    if not section_list:
        legal_risks.append("No statutory section mapping available")
        missing_docs.append("sections")
    if not evidence_list:
        legal_risks.append("Evidence support is thin for legal filing")
        missing_docs.append("evidence")
    if not arrest_list:
        legal_risks.append("No arrest record linked to the case")

    confidence = clamp_score(
        blend_confidence(
            [
                1.0 if section_list else 0.2,
                1.0 if evidence_list else 0.35,
                1.0 if chargesheet_list else 0.25,
                1.0 if court_list else 0.35,
            ]
        )
    )

    supporting_facts = compact_phrases([section.title for section in section_list] + [evidence.title for evidence in evidence_list])

    return LegalInsight(
        relevant_acts=acts,
        relevant_sections=relevant_sections,
        precedents_placeholder=precedents_placeholder,
        legal_risks=sorted(set(legal_risks)),
        missing_legal_documentation=sorted(set(missing_docs)),
        evidence_references=[item.evidence_id or item.evidence_number for item in evidence_list if item.evidence_id or item.evidence_number],
        timeline_references=[],
        supporting_facts=supporting_facts,
        confidence=confidence,
        confidence_level=level_from_score(confidence),
    )
