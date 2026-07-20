from datetime import datetime
from typing import Optional, List

from app.core.logging import app_logger
from app.models.chargesheet import (
    Chargesheet,
    ChargesheetAccused,
    ChargesheetEvidence,
    ChargesheetSection,
)
from app.schemas.chargesheet import ChargesheetSortField
from app.common.enums import SortOrder
from app.common.queries.chargesheet_query import ChargesheetQueryOptions


class ChargesheetRepository:
    """
    Repository responsible for Chargesheet data access and its association entities.
    """

    _chargesheets: list[Chargesheet] = []
    _chargesheet_accused: list[ChargesheetAccused] = []
    _chargesheet_evidence: list[ChargesheetEvidence] = []
    _chargesheet_sections: list[ChargesheetSection] = []

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory chargesheet store.
        """
        if cls._chargesheets:
            return
        app_logger.info("Chargesheet repository initialized.")

    @classmethod
    def create_chargesheet(
        cls,
        chargesheet: Chargesheet,
        accused_links: List[ChargesheetAccused] = None,
        evidence_links: List[ChargesheetEvidence] = None,
        section_links: List[ChargesheetSection] = None,
    ) -> Chargesheet:
        """
        Store a Chargesheet object and its association entities.
        """
        now = datetime.now()
        stored = chargesheet.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._chargesheets.append(stored)

        if accused_links:
            for link in accused_links:
                cls._chargesheet_accused.append(
                    link.model_copy(update={"created_at": now})
                )

        if evidence_links:
            for link in evidence_links:
                cls._chargesheet_evidence.append(
                    link.model_copy(update={"created_at": now})
                )

        if section_links:
            for link in section_links:
                cls._chargesheet_sections.append(
                    link.model_copy(update={"created_at": now})
                )

        app_logger.info(
            "Chargesheet stored | ID=%s | Number=%s | CaseID=%s",
            stored.chargesheet_id,
            stored.chargesheet_number,
            stored.case_master_id,
        )

        return stored

    @classmethod
    def get_chargesheet_by_id(cls, chargesheet_id: str) -> Optional[Chargesheet]:
        """
        Retrieve a single chargesheet by ID.
        """
        return next((cs for cs in cls._chargesheets if cs.chargesheet_id == chargesheet_id), None)

    @classmethod
    def get_chargesheet_by_number(cls, chargesheet_number: str) -> Optional[Chargesheet]:
        """
        Retrieve chargesheet by unique chargesheet_number.
        """
        return next(
            (cs for cs in cls._chargesheets if cs.chargesheet_number.lower() == chargesheet_number.lower()),
            None,
        )

    @classmethod
    def get_chargesheets_by_case_id(cls, case_master_id: str) -> list[Chargesheet]:
        """
        Retrieve all chargesheets for a specific case.
        """
        return [cs for cs in cls._chargesheets if cs.case_master_id == case_master_id]

    @classmethod
    def get_accused_links(cls, chargesheet_id: str) -> list[ChargesheetAccused]:
        """
        Get associated accused links for a chargesheet.
        """
        return [ca for ca in cls._chargesheet_accused if ca.chargesheet_id == chargesheet_id]

    @classmethod
    def get_evidence_links(cls, chargesheet_id: str) -> list[ChargesheetEvidence]:
        """
        Get associated evidence links for a chargesheet.
        """
        return [ce for ce in cls._chargesheet_evidence if ce.chargesheet_id == chargesheet_id]

    @classmethod
    def get_section_links(cls, chargesheet_id: str) -> list[ChargesheetSection]:
        """
        Get associated section links for a chargesheet.
        """
        return [cs for cs in cls._chargesheet_sections if cs.chargesheet_id == chargesheet_id]

    @classmethod
    def update_chargesheet(
        cls,
        chargesheet: Chargesheet,
        accused_links: Optional[List[ChargesheetAccused]] = None,
        evidence_links: Optional[List[ChargesheetEvidence]] = None,
        section_links: Optional[List[ChargesheetSection]] = None,
    ) -> Optional[Chargesheet]:
        """
        Update a chargesheet and optionally replace association entities.
        """
        chargesheet_id = chargesheet.chargesheet_id
        for index, existing in enumerate(cls._chargesheets):
            if existing.chargesheet_id == chargesheet_id:
                updated_record = chargesheet.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._chargesheets[index] = updated_record

                now = datetime.now()
                if accused_links is not None:
                    cls._chargesheet_accused = [
                        ca for ca in cls._chargesheet_accused if ca.chargesheet_id != chargesheet_id
                    ] + [link.model_copy(update={"created_at": now}) for link in accused_links]

                if evidence_links is not None:
                    cls._chargesheet_evidence = [
                        ce for ce in cls._chargesheet_evidence if ce.chargesheet_id != chargesheet_id
                    ] + [link.model_copy(update={"created_at": now}) for link in evidence_links]

                if section_links is not None:
                    cls._chargesheet_sections = [
                        cs for cs in cls._chargesheet_sections if cs.chargesheet_id != chargesheet_id
                    ] + [link.model_copy(update={"created_at": now}) for link in section_links]

                app_logger.info("Chargesheet updated | ID=%s", chargesheet_id)
                return updated_record

        return None

    @classmethod
    def delete_chargesheet(cls, chargesheet_id: str) -> bool:
        """
        Delete a chargesheet and its associations.
        """
        for index, existing in enumerate(cls._chargesheets):
            if existing.chargesheet_id == chargesheet_id:
                del cls._chargesheets[index]
                cls._chargesheet_accused = [
                    ca for ca in cls._chargesheet_accused if ca.chargesheet_id != chargesheet_id
                ]
                cls._chargesheet_evidence = [
                    ce for ce in cls._chargesheet_evidence if ce.chargesheet_id != chargesheet_id
                ]
                cls._chargesheet_sections = [
                    cs for cs in cls._chargesheet_sections if cs.chargesheet_id != chargesheet_id
                ]
                app_logger.info("Chargesheet deleted | ID=%s", chargesheet_id)
                return True

        return False

    @classmethod
    def query_chargesheets(
        cls, options: ChargesheetQueryOptions
    ) -> tuple[list[Chargesheet], int]:
        """
        Query chargesheets with options.
        """
        filtered = list(cls._chargesheets)

        if options.case_master_id:
            filtered = [cs for cs in filtered if cs.case_master_id == options.case_master_id]

        if options.status:
            filtered = [cs for cs in filtered if cs.status == options.status]

        if options.chargesheet_number:
            search_num = options.chargesheet_number.lower()
            filtered = [cs for cs in filtered if search_num in cs.chargesheet_number.lower()]

        if options.investigating_officer:
            search_officer = options.investigating_officer.lower()
            filtered = [cs for cs in filtered if search_officer in cs.investigating_officer.lower()]

        if options.summary:
            search_sum = options.summary.lower()
            filtered = [cs for cs in filtered if search_sum in cs.summary.lower()]

        total_count = len(filtered)

        SORT_FIELDS = {
            ChargesheetSortField.FILING_DATE: lambda cs: cs.filing_date or datetime.min,
            ChargesheetSortField.CHARGESHEET_NUMBER: lambda cs: cs.chargesheet_number.lower(),
            ChargesheetSortField.STATUS: lambda cs: cs.status.value,
            ChargesheetSortField.CREATED_AT: lambda cs: cs.created_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda cs: cs.filing_date or datetime.min)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
