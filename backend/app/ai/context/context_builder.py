"""
============================================================
AI Context Builder
============================================================

Module  : AI Context Builder
Purpose : Aggregates all investigation domain entities for a given case
          into a unified InvestigationContext object without mutating
          underlying repositories.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Optional

from app.ai.context.context_models import (
    ContextMetadata,
    ContextSummary,
    InvestigationContext,
)
from app.ai.context.exceptions import AIContextBuildException
from app.ai.context.plugins.base import ContextPlugin
from app.common.exceptions import CaseNotFoundException
from app.common.queries.officer_query import OfficerAssignmentQueryOptions
from app.models.accused import Accused
from app.models.arrest import Arrest
from app.models.case_master import CaseMaster
from app.models.chargesheet import Chargesheet
from app.models.complainant import Complainant
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence
from app.models.officer import OfficerAssignment
from app.models.section import Section
from app.models.timeline import TimelineEvent
from app.models.victim import Victim
from app.models.witness import Witness
from app.repository.accused_repository import AccusedRepository
from app.repository.arrest_repository import ArrestRepository
from app.repository.case_repository import CaseRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.repository.chargesheet_repository import ChargesheetRepository
from app.repository.complainant_repository import ComplainantRepository
from app.repository.court_proceeding_repository import CourtProceedingRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.officer_repository import OfficerRepository
from app.repository.section_repository import SectionRepository
from app.repository.timeline_repository import TimelineRepository
from app.repository.victim_repository import VictimRepository
from app.repository.witness_repository import WitnessRepository


class AIContextBuilder:
    """
    Builder responsible for retrieving and assembling all investigation components
    for a case into an AI-ready InvestigationContext.
    """

    _plugins: list[ContextPlugin] = []

    @classmethod
    def register_plugin(cls, plugin: ContextPlugin) -> None:
        """Register a ContextPlugin for context enrichment."""
        if plugin not in cls._plugins:
            cls._plugins.append(plugin)

    @classmethod
    def clear_plugins(cls) -> None:
        """Clear all registered plugins."""
        cls._plugins.clear()

    # ----------------------------------------------------------
    # Private Modular Loaders
    # ----------------------------------------------------------

    @classmethod
    def _load_case(cls, case_id: str) -> CaseMaster:
        """Load central CaseMaster entity or raise 404 if missing."""
        CaseRepository.initialize()
        case = CaseRepository.get_case_by_id(case_id)
        if case is None:
            raise CaseNotFoundException(case_id)
        return case

    @classmethod
    def _load_complainant(cls, case_id: str) -> Optional[Complainant]:
        """Load primary complainant for case."""
        ComplainantRepository.initialize()
        complainants = ComplainantRepository.get_complainants_by_case_id(case_id)
        return complainants[0] if complainants else None

    @classmethod
    def _load_victims(cls, case_id: str) -> list[Victim]:
        """Load victims linked to case."""
        VictimRepository.initialize()
        return VictimRepository.get_victims_by_case_id(case_id)

    @classmethod
    def _load_accused(cls, case_id: str) -> list[Accused]:
        """Load accused persons linked to case."""
        AccusedRepository.initialize()
        return AccusedRepository.get_accused_by_case_id(case_id)

    @classmethod
    def _load_witnesses(cls, case_id: str) -> list[Witness]:
        """Load witnesses linked to case."""
        WitnessRepository.initialize()
        return WitnessRepository.get_witnesses_by_case_id(case_id)

    @classmethod
    def _load_sections(cls, case_id: str) -> list[Section]:
        """Load law sections linked to case via case-section associations."""
        CaseSectionRepository.initialize()
        SectionRepository.initialize()
        associations = CaseSectionRepository.get_case_sections(case_id)
        sections: list[Section] = []
        for assoc in associations:
            sec = SectionRepository.get_section_by_id(assoc.section_id)
            if sec:
                sections.append(sec)
        return sections

    @classmethod
    def _load_evidence(cls, case_id: str) -> list[Evidence]:
        """Load evidence records linked to case."""
        EvidenceRepository.initialize()
        return EvidenceRepository.get_case_evidence(case_id)

    @classmethod
    def _load_arrests(cls, case_id: str) -> list[Arrest]:
        """Load arrest records linked to case."""
        ArrestRepository.initialize()
        return ArrestRepository.get_arrests_by_case_id(case_id)

    @classmethod
    def _load_chargesheets(cls, case_id: str) -> list[Chargesheet]:
        """Load chargesheets linked to case."""
        ChargesheetRepository.initialize()
        return ChargesheetRepository.get_chargesheets_by_case_id(case_id)

    @classmethod
    def _load_court_proceedings(cls, case_id: str) -> list[CourtProceeding]:
        """Load court proceedings linked to case."""
        CourtProceedingRepository.initialize()
        return CourtProceedingRepository.get_proceedings_by_case_id(case_id)

    @classmethod
    def _load_officer_assignments(cls, case_id: str) -> list[OfficerAssignment]:
        """Load officer assignments linked to case."""
        OfficerRepository.initialize()
        opts = OfficerAssignmentQueryOptions(case_master_id=case_id, page_size=100)
        records, _ = OfficerRepository.query_assignments(opts)
        return records

    @classmethod
    def _load_timeline(cls, case_id: str) -> list[TimelineEvent]:
        """Load investigation timeline events linked to case."""
        TimelineRepository.initialize()
        return TimelineRepository.get_case_timeline(case_id)

    # ----------------------------------------------------------
    # Helper Computations
    # ----------------------------------------------------------

    @classmethod
    def _evaluate_ai_readiness(
        cls,
        case: CaseMaster,
        complainant: Optional[Complainant],
        victims: list[Victim],
        accused: list[Accused],
        sections: list[Section],
        evidence: list[Evidence],
        timeline: list[TimelineEvent],
    ) -> tuple[bool, list[str]]:
        """Evaluate whether case has sufficient context for AI readiness."""
        reasons: list[str] = []

        if not sections:
            reasons.append("No legal sections assigned to case.")
        if not complainant and not victims:
            reasons.append("No complainant or victim records linked.")
        if not timeline and not evidence:
            reasons.append("No timeline events or evidence items recorded.")

        is_ready = len(reasons) == 0
        if is_ready:
            reasons.append("Case has complete foundational context ready for AI analysis.")

        return is_ready, reasons

    @classmethod
    def _compute_context_hash(
        cls,
        case_id: str,
        case: CaseMaster,
        complainant: Optional[Complainant],
        victims: list[Victim],
        accused: list[Accused],
        witnesses: list[Witness],
        sections: list[Section],
        evidence: list[Evidence],
        arrests: list[Arrest],
        chargesheets: list[Chargesheet],
        court_proceedings: list[CourtProceeding],
        officer_assignments: list[OfficerAssignment],
        timeline_events: list[TimelineEvent],
    ) -> str:
        """Generate SHA-256 fingerprint over core domain entities."""
        payload = {
            "case_id": case_id,
            "crime_no": case.crime_no,
            "case_no": case.case_no,
            "complainant_id": complainant.complainant_id if complainant else None,
            "victim_ids": sorted([v.victim_id for v in victims if v.victim_id]),
            "accused_ids": sorted([a.accused_id for a in accused if a.accused_id]),
            "witness_ids": sorted([w.witness_id for w in witnesses if w.witness_id]),
            "section_ids": sorted([s.section_id for s in sections if s.section_id]),
            "evidence_ids": sorted([e.evidence_id for e in evidence if e.evidence_id]),
            "arrest_ids": sorted([a.arrest_id for a in arrests if a.arrest_id]),
            "chargesheet_ids": sorted([c.chargesheet_id for c in chargesheets if c.chargesheet_id]),
            "proceeding_ids": sorted([p.proceeding_id for p in court_proceedings if p.proceeding_id]),
            "assignment_ids": sorted([o.assignment_id for o in officer_assignments if o.assignment_id]),
            "timeline_ids": sorted([t.event_id for t in timeline_events if t.event_id]),
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def _resolve_lead_officer(cls, assignments: list[OfficerAssignment]) -> Optional[str]:
        """Resolve lead officer name/badge from assignments."""
        if not assignments:
            return None
        # Prefer active lead officer assignment if present
        lead_assign = next(
            (a for a in assignments if a.is_active and getattr(a.role, "value", str(a.role)).upper() in ("LEAD", "IO")),
            assignments[0],
        )
        officer = OfficerRepository.get_officer_by_id(lead_assign.officer_id)
        if officer:
            return f"{officer.name} ({officer.badge_number})"
        return f"Officer ID: {lead_assign.officer_id}"

    # ----------------------------------------------------------
    # Main Orchestrator
    # ----------------------------------------------------------

    @classmethod
    def build_context(cls, case_id: str) -> InvestigationContext:
        """
        Build and assemble complete InvestigationContext for a given case_id.
        """
        start_time = time.perf_counter()

        try:
            # 1. Load domain entities via modular loaders
            case = cls._load_case(case_id)
            complainant = cls._load_complainant(case_id)
            victims = cls._load_victims(case_id)
            accused = cls._load_accused(case_id)
            witnesses = cls._load_witnesses(case_id)
            sections = cls._load_sections(case_id)
            evidence = cls._load_evidence(case_id)
            arrests = cls._load_arrests(case_id)
            chargesheets = cls._load_chargesheets(case_id)
            court_proceedings = cls._load_court_proceedings(case_id)
            officer_assignments = cls._load_officer_assignments(case_id)
            timeline_events = cls._load_timeline(case_id)

            # 2. Evaluate AI readiness and compute hash fingerprint
            is_ready, readiness_reasons = cls._evaluate_ai_readiness(
                case, complainant, victims, accused, sections, evidence, timeline_events
            )
            context_hash = cls._compute_context_hash(
                case_id,
                case,
                complainant,
                victims,
                accused,
                witnesses,
                sections,
                evidence,
                arrests,
                chargesheets,
                court_proceedings,
                officer_assignments,
                timeline_events,
            )

            # 3. Entity counts and total entity summation
            entity_counts = {
                "complainant": 1 if complainant else 0,
                "victims": len(victims),
                "accused": len(accused),
                "witnesses": len(witnesses),
                "sections": len(sections),
                "evidence": len(evidence),
                "arrests": len(arrests),
                "chargesheets": len(chargesheets),
                "court_proceedings": len(court_proceedings),
                "officer_assignments": len(officer_assignments),
                "timeline_events": len(timeline_events),
            }
            total_entities = sum(entity_counts.values())

            # 4. Measure execution duration
            end_time = time.perf_counter()
            build_duration_ms = round((end_time - start_time) * 1000, 2)

            # 5. Build Metadata and Summary
            metadata = ContextMetadata(
                generated_at=datetime.now(),
                case_id=case_id,
                context_version="1.0.0",
                build_duration_ms=build_duration_ms,
                context_hash=context_hash,
                is_ai_ready=is_ready,
                ai_readiness_reasons=readiness_reasons,
                total_entities=total_entities,
                entity_counts=entity_counts,
            )

            lead_officer = cls._resolve_lead_officer(officer_assignments)
            summary = ContextSummary(
                case_title=f"FIR No. {case.crime_no}",
                status=getattr(case, "status", "REGISTERED"),
                registered_date=case.crime_registered_date,
                lead_officer=lead_officer,
                total_accused=len(accused),
                total_victims=len(victims),
                total_evidence=len(evidence),
                total_sections=len(sections),
                is_ai_ready=is_ready,
            )

            # 6. Construct unified InvestigationContext
            context = InvestigationContext(
                case=case,
                complainant=complainant,
                victims=victims,
                accused=accused,
                witnesses=witnesses,
                sections=sections,
                evidence=evidence,
                arrests=arrests,
                chargesheets=chargesheets,
                court_proceedings=court_proceedings,
                officer_assignments=officer_assignments,
                timeline_events=timeline_events,
                summary=summary,
                metadata=metadata,
            )

            # 7. Execute registered plugins for context enrichment
            for plugin in cls._plugins:
                plugin.enrich(context)

            return context

        except CaseNotFoundException:
            raise
        except Exception as exc:
            raise AIContextBuildException(case_id=case_id, reason=str(exc)) from exc
