"""Case similarity analysis using the existing retrieval engine."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from sqlalchemy import select

from app.ai.investigation.analysis.confidence import blend_confidence, level_from_score
from app.ai.investigation.analysis.pattern_analysis import compact_phrases, term_overlap_score, tokenize
from app.ai.investigation.intelligence.investigation_models import SimilarityResult
from app.ai.retrieval.retrieval_models import RetrievalFilter, SearchQuery
from app.ai.retrieval.retrieval_service import RetrievalService
from app.database.session import SessionLocal
from app.database.orm.case_master import CaseMasterORM
from app.database.mappers.case_mapper import CaseMapper
from app.models.accused import Accused
from app.models.arrest import Arrest
from app.models.case_master import CaseMaster
from app.models.case_section import CaseSectionAssociation
from app.models.chargesheet import Chargesheet
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence
from app.models.section import Section
from app.models.timeline import TimelineEvent
from app.models.victim import Victim
from app.models.witness import Witness
from app.repository.accused_repository import AccusedRepository
from app.repository.arrest_repository import ArrestRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.repository.case_repository import CaseRepository
from app.repository.chargesheet_repository import ChargesheetRepository
from app.repository.court_proceeding_repository import CourtProceedingRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.section_repository import SectionRepository
from app.repository.timeline_repository import TimelineRepository
from app.repository.victim_repository import VictimRepository
from app.repository.witness_repository import WitnessRepository


class _CaseBundle:
    def __init__(
        self,
        case: CaseMaster,
        accused: list[Accused],
        arrests: list[Arrest],
        chargesheets: list[Chargesheet],
        court_proceedings: list[CourtProceeding],
        evidence: list[Evidence],
        sections: list[Section],
        timeline_events: list[TimelineEvent],
        victims: list[Victim],
        witnesses: list[Witness],
    ) -> None:
        self.case = case
        self.accused = accused
        self.arrests = arrests
        self.chargesheets = chargesheets
        self.court_proceedings = court_proceedings
        self.evidence = evidence
        self.sections = sections
        self.timeline_events = timeline_events
        self.victims = victims
        self.witnesses = witnesses


def _load_all_cases() -> list[CaseMaster]:
    db = SessionLocal()
    try:
        stmt = select(CaseMasterORM)
        return [CaseMapper.to_domain(row) for row in db.scalars(stmt).all()]
    finally:
        db.close()


def _load_case_bundle(case_id: str) -> _CaseBundle | None:
    case = CaseRepository.get_case_by_id(case_id)
    if not case:
        return None

    accused = AccusedRepository.get_accused_by_case_id(case.case_master_id)
    arrests = ArrestRepository.get_arrests_by_case_id(case.case_master_id)
    chargesheets = ChargesheetRepository.get_chargesheets_by_case_id(case.case_master_id)
    court_proceedings = CourtProceedingRepository.get_proceedings_by_case_id(case.case_master_id)
    evidence = EvidenceRepository.get_case_evidence(case.case_master_id)
    timeline_events = TimelineRepository.get_case_timeline(case.case_master_id)
    victims = VictimRepository.get_victims_by_case_id(case.case_master_id)
    witnesses = WitnessRepository.get_witnesses_by_case_id(case.case_master_id)
    associations = CaseSectionRepository.get_case_sections(case.case_master_id)

    sections: list[Section] = []
    for association in associations:
        section = SectionRepository.get_section_by_id(association.section_id)
        if section:
            sections.append(section)

    return _CaseBundle(case, accused, arrests, chargesheets, court_proceedings, evidence, sections, timeline_events, victims, witnesses)


def _case_text(bundle: _CaseBundle) -> str:
    parts: list[str] = [
        bundle.case.crime_no,
        bundle.case.case_no or "",
        bundle.case.brief_facts or "",
    ]
    parts.extend(item.title for item in bundle.evidence)
    parts.extend(item.description for item in bundle.evidence)
    parts.extend(item.name for item in bundle.accused)
    parts.extend(item.name for item in bundle.victims)
    parts.extend(item.name for item in bundle.witnesses)
    parts.extend(item.title for item in bundle.timeline_events)
    parts.extend(item.description for item in bundle.timeline_events)
    parts.extend(item.section_number for item in bundle.sections)
    return " ".join(part for part in parts if part)


def _shared_entities(bundle: _CaseBundle, target: _CaseBundle | None, query_tokens: set[str]) -> tuple[list[str], list[str], list[str], list[str]]:
    shared_evidence: list[str] = []
    shared_accused: list[str] = []
    shared_sections: list[str] = []
    shared_mo: list[str] = []
    if target:
        target_text = _case_text(target)
        for evidence in bundle.evidence:
            if term_overlap_score(evidence.title + " " + evidence.description, target_text) >= 0.25:
                shared_evidence.append(evidence.evidence_id or evidence.evidence_number)
        for accused in bundle.accused:
            if term_overlap_score(accused.name, target_text) >= 0.3:
                shared_accused.append(accused.accused_id or accused.name)
        for section in bundle.sections:
            section_text = section.title + " " + (section.description or "")
            if term_overlap_score(section_text, target_text) >= 0.2:
                shared_sections.append(section.section_id or section.section_number)
        for evidence in bundle.evidence:
            if term_overlap_score(evidence.description or evidence.title, target_text) >= 0.2:
                shared_mo.append(evidence.title)
    else:
        for evidence in bundle.evidence:
            if set(tokenize(evidence.title + " " + evidence.description)) & query_tokens:
                shared_evidence.append(evidence.evidence_id or evidence.evidence_number)
                shared_mo.append(evidence.title)
        for accused in bundle.accused:
            if set(tokenize(accused.name)) & query_tokens:
                shared_accused.append(accused.accused_id or accused.name)
        for section in bundle.sections:
            if set(tokenize(section.title + " " + (section.description or ""))) & query_tokens:
                shared_sections.append(section.section_id or section.section_number)

    return sorted(set(shared_evidence)), sorted(set(shared_accused)), sorted(set(shared_sections)), sorted(set(shared_mo))


def analyze_case_similarity(request_case_id: str | None, query: str | None, top_k: int = 5) -> list[SimilarityResult]:
    target_bundle = _load_case_bundle(request_case_id) if request_case_id else None
    query_text = query or (target_bundle and _case_text(target_bundle)) or ""
    query_tokens = set(tokenize(query_text))

    retrieval_query = SearchQuery(
        query=query_text,
        top_k=max(top_k * 3, 10),
        min_similarity=0.0,
        filters=RetrievalFilter(case_id=None),
    )
    retrieval_result = RetrievalService.retrieve(retrieval_query)
    retrieval_scores: dict[str, list[float]] = defaultdict(list)
    for chunk in retrieval_result.chunks:
        retrieval_scores[chunk.case_id].append(chunk.similarity_score or 0.0)

    all_cases = _load_all_cases()
    results: list[SimilarityResult] = []
    target_case_id = request_case_id or (target_bundle.case.case_master_id if target_bundle else None)

    for candidate_case in all_cases:
        if target_case_id and candidate_case.case_master_id == target_case_id:
            continue
        candidate_bundle = _load_case_bundle(candidate_case.case_master_id)
        if not candidate_bundle:
            continue

        candidate_text = _case_text(candidate_bundle)
        text_score = term_overlap_score(query_text, candidate_text)
        if target_bundle:
            target_text = _case_text(target_bundle)
            text_score = max(text_score, term_overlap_score(target_text, candidate_text))

        candidate_scores = retrieval_scores.get(candidate_case.case_master_id, [])
        retrieval_score = sum(candidate_scores) / max(1, len(candidate_scores))
        evidence, accused, sections, mo = _shared_entities(candidate_bundle, target_bundle, query_tokens)
        shared_signal = blend_confidence(
            [
                1.0 if evidence else 0.0,
                1.0 if accused else 0.0,
                1.0 if sections else 0.0,
                1.0 if mo else 0.0,
                text_score,
                retrieval_score,
            ]
        )

        if shared_signal <= 0.0:
            continue

        results.append(
            SimilarityResult(
                case_id=candidate_case.case_master_id,
                case_no=candidate_case.case_no,
                similarity_score=round(shared_signal * 100.0, 2),
                shared_evidence=evidence,
                shared_accused=accused,
                shared_sections=sections,
                shared_mo=mo,
                evidence_references=evidence,
                timeline_references=[event.event_id for event in candidate_bundle.timeline_events if event.event_id],
                reason="Shared case facts, evidence, and statutory context detected.",
                confidence=shared_signal,
                confidence_level=level_from_score(shared_signal),
            )
        )

    results.sort(key=lambda item: (-item.similarity_score, item.case_id))
    return results[:top_k]
