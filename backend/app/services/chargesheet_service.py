from uuid import uuid4
from datetime import datetime
from fastapi import Depends

from app.common.exceptions import (
    CaseNotFoundException,
    AccusedNotFoundException,
    EvidenceNotFoundException,
    SectionNotFoundException,
    ChargesheetNotFoundException,
    DuplicateChargesheetNumberException,
)
from app.models.chargesheet import (
    Chargesheet,
    ChargesheetAccused,
    ChargesheetEvidence,
    ChargesheetSection,
)
from app.models.timeline import TimelineEventType
from app.repository.case_repository import CaseRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.section_repository import SectionRepository
from app.repository.chargesheet_repository import ChargesheetRepository
from app.services.timeline_service import TimelineService
from app.common.queries.chargesheet_query import ChargesheetQueryOptions
from app.schemas.chargesheet import (
    ChargesheetCreate,
    ChargesheetUpdate,
    ChargesheetResponse,
    ChargesheetAccusedDetail,
    ChargesheetEvidenceDetail,
    ChargesheetSectionDetail,
    ChargesheetListResponse,
    PaginationMeta,
)


class ChargesheetService:
    """
    Service responsible for Chargesheet management business logic.
    """

    def __init__(
        self,
        case_repo=CaseRepository,
        accused_repo=AccusedRepository,
        evidence_repo=EvidenceRepository,
        section_repo=SectionRepository,
        chargesheet_repo=ChargesheetRepository,
        timeline_service=None,
    ):
        self.case_repo = case_repo
        self.accused_repo = accused_repo
        self.evidence_repo = evidence_repo
        self.section_repo = section_repo
        self.chargesheet_repo = chargesheet_repo
        self.timeline_service = timeline_service or TimelineService()

    def create_chargesheet(
        self, case_master_id: str, schema: ChargesheetCreate
    ) -> ChargesheetResponse:
        """
        File a new chargesheet for a case.
        """
        case = self.case_repo.get_case_by_id(case_master_id)
        if case is None:
            raise CaseNotFoundException(case_master_id)

        # Generate or validate chargesheet number
        if schema.chargesheet_number:
            num = schema.chargesheet_number.strip()
            existing = self.chargesheet_repo.get_chargesheet_by_number(num)
            if existing:
                raise DuplicateChargesheetNumberException(num)
        else:
            num = f"CSN-{datetime.now().year}-{uuid4().hex[:6].upper()}"

        # Validate Accused links
        accused_entities = []
        accused_links = []
        for link in schema.accused_links:
            acc = self.accused_repo.get_accused_by_id(link.accused_id)
            if acc is None:
                raise AccusedNotFoundException(link.accused_id)
            accused_entities.append(acc)

        # Validate Evidence links
        evidence_entities = []
        evidence_links = []
        for link in schema.evidence_links:
            ev = self.evidence_repo.get_evidence_by_id(link.evidence_id)
            if ev is None:
                raise EvidenceNotFoundException(link.evidence_id)
            evidence_entities.append(ev)

        # Validate Section links
        section_entities = []
        section_links = []
        for link in schema.section_links:
            sec = self.section_repo.get_section_by_id(link.section_id)
            if sec is None:
                raise SectionNotFoundException(link.section_id)
            section_entities.append(sec)

        chargesheet_id = f"CS-{uuid4().hex[:12].upper()}"

        chargesheet = Chargesheet(
            chargesheet_id=chargesheet_id,
            case_master_id=case_master_id,
            chargesheet_number=num,
            filing_date=schema.filing_date,
            investigating_officer=schema.investigating_officer.strip(),
            summary=schema.summary.strip(),
            remarks=schema.remarks,
            status=schema.status,
        )

        for link in schema.accused_links:
            accused_links.append(
                ChargesheetAccused(
                    chargesheet_id=chargesheet_id,
                    accused_id=link.accused_id,
                    charges_summary=link.charges_summary,
                )
            )

        for link in schema.evidence_links:
            evidence_links.append(
                ChargesheetEvidence(
                    chargesheet_id=chargesheet_id,
                    evidence_id=link.evidence_id,
                    relevance_notes=link.relevance_notes,
                )
            )

        for link in schema.section_links:
            section_links.append(
                ChargesheetSection(
                    chargesheet_id=chargesheet_id,
                    section_id=link.section_id,
                    offence_details=link.offence_details,
                )
            )

        stored = self.chargesheet_repo.create_chargesheet(
            chargesheet=chargesheet,
            accused_links=accused_links,
            evidence_links=evidence_links,
            section_links=section_links,
        )

        # Trigger Timeline Event
        self.timeline_service.record_event(
            case_master_id=case_master_id,
            event_type=TimelineEventType.CHARGESHEET_FILED,
            title=f"Chargesheet Filed: {num}",
            description=f"Chargesheet '{num}' filed by {schema.investigating_officer} for case {case_master_id}.",
            reference_id=chargesheet_id,
            reference_type="Chargesheet",
        )

        return self._build_response(stored)

    def get_chargesheet(self, chargesheet_id: str) -> ChargesheetResponse:
        """
        Retrieve chargesheet details by ID.
        """
        cs = self.chargesheet_repo.get_chargesheet_by_id(chargesheet_id)
        if cs is None:
            raise ChargesheetNotFoundException(chargesheet_id)
        return self._build_response(cs)

    def update_chargesheet(
        self, chargesheet_id: str, schema: ChargesheetUpdate
    ) -> ChargesheetResponse:
        """
        Update chargesheet details and associations.
        """
        existing = self.chargesheet_repo.get_chargesheet_by_id(chargesheet_id)
        if existing is None:
            raise ChargesheetNotFoundException(chargesheet_id)

        updates = schema.model_dump(exclude_unset=True)

        if "chargesheet_number" in updates and updates["chargesheet_number"]:
            num = updates["chargesheet_number"].strip()
            if num.lower() != existing.chargesheet_number.lower():
                other = self.chargesheet_repo.get_chargesheet_by_number(num)
                if other:
                    raise DuplicateChargesheetNumberException(num)
            updates["chargesheet_number"] = num

        if "investigating_officer" in updates and updates["investigating_officer"]:
            updates["investigating_officer"] = updates["investigating_officer"].strip()
        if "summary" in updates and updates["summary"]:
            updates["summary"] = updates["summary"].strip()

        accused_links = None
        if schema.accused_links is not None:
            accused_links = []
            for link in schema.accused_links:
                acc = self.accused_repo.get_accused_by_id(link.accused_id)
                if acc is None:
                    raise AccusedNotFoundException(link.accused_id)
                accused_links.append(
                    ChargesheetAccused(
                        chargesheet_id=chargesheet_id,
                        accused_id=link.accused_id,
                        charges_summary=link.charges_summary,
                    )
                )

        evidence_links = None
        if schema.evidence_links is not None:
            evidence_links = []
            for link in schema.evidence_links:
                ev = self.evidence_repo.get_evidence_by_id(link.evidence_id)
                if ev is None:
                    raise EvidenceNotFoundException(link.evidence_id)
                evidence_links.append(
                    ChargesheetEvidence(
                        chargesheet_id=chargesheet_id,
                        evidence_id=link.evidence_id,
                        relevance_notes=link.relevance_notes,
                    )
                )

        section_links = None
        if schema.section_links is not None:
            section_links = []
            for link in schema.section_links:
                sec = self.section_repo.get_section_by_id(link.section_id)
                if sec is None:
                    raise SectionNotFoundException(link.section_id)
                section_links.append(
                    ChargesheetSection(
                        chargesheet_id=chargesheet_id,
                        section_id=link.section_id,
                        offence_details=link.offence_details,
                    )
                )

        updated_cs = existing.model_copy(update=updates)
        stored = self.chargesheet_repo.update_chargesheet(
            chargesheet=updated_cs,
            accused_links=accused_links,
            evidence_links=evidence_links,
            section_links=section_links,
        )

        if stored is None:
            raise ChargesheetNotFoundException(chargesheet_id)

        return self._build_response(stored)

    def delete_chargesheet(self, chargesheet_id: str) -> None:
        """
        Delete a chargesheet by ID.
        """
        existing = self.chargesheet_repo.get_chargesheet_by_id(chargesheet_id)
        if existing is None:
            raise ChargesheetNotFoundException(chargesheet_id)

        self.chargesheet_repo.delete_chargesheet(chargesheet_id)

    def search_chargesheets(
        self, options: ChargesheetQueryOptions
    ) -> ChargesheetListResponse:
        """
        Query chargesheets with options.
        """
        records, total = self.chargesheet_repo.query_chargesheets(options)
        items = [self._build_response(cs) for cs in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return ChargesheetListResponse(items=items, pagination=meta)

    def _build_response(self, cs: Chargesheet) -> ChargesheetResponse:
        """
        Helper method to populate association details in ChargesheetResponse.
        """
        res = ChargesheetResponse.model_validate(cs)

        # Populate Accused details
        acc_links = self.chargesheet_repo.get_accused_links(cs.chargesheet_id)
        res.accused = []
        for al in acc_links:
            acc = self.accused_repo.get_accused_by_id(al.accused_id)
            res.accused.append(
                ChargesheetAccusedDetail(
                    accused_id=al.accused_id,
                    accused_name=acc.name if acc else None,
                    charges_summary=al.charges_summary,
                )
            )

        # Populate Evidence details
        ev_links = self.chargesheet_repo.get_evidence_links(cs.chargesheet_id)
        res.evidence = []
        for el in ev_links:
            ev = self.evidence_repo.get_evidence_by_id(el.evidence_id)
            res.evidence.append(
                ChargesheetEvidenceDetail(
                    evidence_id=el.evidence_id,
                    evidence_number=ev.evidence_number if ev else None,
                    title=ev.title if ev else None,
                    relevance_notes=el.relevance_notes,
                )
            )

        # Populate Section details
        sec_links = self.chargesheet_repo.get_section_links(cs.chargesheet_id)
        res.sections = []
        for sl in sec_links:
            sec = self.section_repo.get_section_by_id(sl.section_id)
            res.sections.append(
                ChargesheetSectionDetail(
                    section_id=sl.section_id,
                    section_number=sec.section_number if sec else None,
                    offence_details=sl.offence_details,
                )
            )

        return res
