from uuid import uuid4
from fastapi import Depends

from app.common.exceptions import (
    CaseNotFoundException,
    SectionNotFoundException,
    DuplicateCaseSectionException,
    CaseSectionNotFoundException,
)
from app.models.case_section import CaseSectionAssociation
from app.repository.case_repository import CaseRepository
from app.repository.section_repository import SectionRepository
from app.repository.act_repository import ActRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.common.queries.case_section_query import CaseSectionQueryOptions
from app.schemas.case_section import (
    CaseSectionCreate,
    CaseSectionResponse,
    CaseSectionSummary,
    CaseSectionListResponse,
    PaginationMeta,
)


class CaseSectionService:
    """
    Service layer handling case section association assignments.
    """

    def __init__(
        self,
        case_repo: CaseRepository = Depends(lambda: CaseRepository),
        section_repo: SectionRepository = Depends(lambda: SectionRepository),
        act_repo: ActRepository = Depends(lambda: ActRepository),
        case_section_repo: CaseSectionRepository = Depends(lambda: CaseSectionRepository),
    ):
        self.case_repo = case_repo
        self.section_repo = section_repo
        self.act_repo = act_repo
        self.case_section_repo = case_section_repo

    # ----------------------------------------------------------
    # Helper to construct detailed CaseSectionSummary
    # ----------------------------------------------------------

    def _build_summary(
        self, association: CaseSectionAssociation
    ) -> CaseSectionSummary:
        """
        Construct a detailed de-serialized CaseSectionSummary by loading Act & Section details.
        """
        section = self.section_repo.get_section_by_id(association.section_id)
        if section is None:
            # Fallback if section was deleted from catalog
            return CaseSectionSummary(
                association_id=association.association_id,
                case_master_id=association.case_master_id,
                section_id=association.section_id,
                remarks=association.remarks,
                created_at=association.created_at,
                section_number="Unknown",
                section_title="Unknown Section",
                act_short_name="Unknown Act",
                act_year=0,
                is_cognizable=True,
                is_bailable=True,
                maximum_punishment=None,
            )

        act = self.act_repo.get_act_by_id(section.act_id)
        act_short_name = act.short_name if act else "Unknown Act"
        act_year = act.year if act else 0

        return CaseSectionSummary(
            association_id=association.association_id,
            case_master_id=association.case_master_id,
            section_id=association.section_id,
            remarks=association.remarks,
            created_at=association.created_at,
            section_number=section.section_number,
            section_title=section.title,
            act_short_name=act_short_name,
            act_year=act_year,
            is_cognizable=section.is_cognizable,
            is_bailable=section.is_bailable,
            maximum_punishment=section.maximum_punishment,
        )

    # ----------------------------------------------------------
    # Link Section to Case
    # ----------------------------------------------------------

    def assign_section(
        self, case_id: str, schema: CaseSectionCreate
    ) -> CaseSectionResponse:
        """
        Assign a legal Section to a Case.
        Validates case, section existence and uniqueness of the link.
        """
        # 1. Validate Case exists
        case = self.case_repo.get_case_by_id(case_id)
        if case is None:
            raise CaseNotFoundException(case_id)

        # 2. Validate Section exists
        section = self.section_repo.get_section_by_id(schema.section_id)
        if section is None:
            raise SectionNotFoundException(schema.section_id)

        # 3. Check for duplicate assignment
        existing = self.case_section_repo.get_association_by_case_and_section(
            case_id, schema.section_id
        )
        if existing is not None:
            raise DuplicateCaseSectionException(schema.section_id, case_id)

        # 4. Generate Association ID
        association_id = f"CSA-{uuid4().hex[:12].upper()}"

        association = CaseSectionAssociation(
            association_id=association_id,
            case_master_id=case_id,
            section_id=schema.section_id,
            remarks=schema.remarks,
        )

        stored = self.case_section_repo.assign_section_to_case(association)
        return CaseSectionResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Remove Section Link
    # ----------------------------------------------------------

    def remove_section(self, case_id: str, association_id: str) -> None:
        """
        Remove/Delete a case-section association.
        """
        # Verify Case exists
        case = self.case_repo.get_case_by_id(case_id)
        if case is None:
            raise CaseNotFoundException(case_id)

        existing = self.case_section_repo.get_association_by_id(association_id)
        if existing is None or existing.case_master_id != case_id:
            raise CaseSectionNotFoundException(association_id)

        self.case_section_repo.remove_section(association_id)

    # ----------------------------------------------------------
    # Search Assigned Sections
    # ----------------------------------------------------------

    def search_case_sections(
        self, options: CaseSectionQueryOptions
    ) -> CaseSectionListResponse:
        """
        Search case section associations.
        """
        records, total = self.case_section_repo.query_case_sections(options)
        summaries = [self._build_summary(r) for r in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return CaseSectionListResponse(items=summaries, pagination=meta)
