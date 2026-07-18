from uuid import uuid4
from fastapi import Depends

from app.common.exceptions import ActNotFoundException, SectionNotFoundException, DuplicateSectionException
from app.models.section import Section
from app.repository.act_repository import ActRepository
from app.repository.section_repository import SectionRepository
from app.common.queries.section_query import SectionQueryOptions
from app.schemas.section import (
    SectionCreate,
    SectionResponse,
    SectionSummary,
    SectionListResponse,
    PaginationMeta,
    SectionUpdate,
)


class SectionService:
    """
    Service layer handling legal Section catalog logic.
    """

    def __init__(
        self,
        act_repo: ActRepository = Depends(lambda: ActRepository),
        section_repo: SectionRepository = Depends(lambda: SectionRepository),
    ):
        self.act_repo = act_repo
        self.section_repo = section_repo

    # ----------------------------------------------------------
    # Normalization helper
    # ----------------------------------------------------------

    @staticmethod
    def normalize_section_number(val: str) -> str:
        """
        Normalize section number by stripping whitespace, converting to uppercase,
        and cleaning unnecessary slashes or dots.
        """
        return val.strip().upper().replace("/", "").replace(" ", "")

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    def create_section(self, act_id: str, schema: SectionCreate) -> SectionResponse:
        """
        Create a new Section master record under an Act.
        """
        # 1. Validate parent Act exists
        act = self.act_repo.get_act_by_id(act_id)
        if act is None:
            raise ActNotFoundException(act_id)

        # 2. Normalize section number
        section_number = self.normalize_section_number(schema.section_number)
        title = schema.title.strip()

        # 3. Validate unique constraint on (act_id + section_number)
        existing = self.section_repo.get_section_by_number(act_id, section_number)
        if existing is not None:
            raise DuplicateSectionException(section_number, act_id)

        # 4. Generate Section ID
        section_id = f"SEC-{uuid4().hex[:12].upper()}"

        section = Section(
            section_id=section_id,
            act_id=act_id,
            section_number=section_number,
            title=title,
            description=schema.description,
            is_cognizable=schema.is_cognizable,
            is_bailable=schema.is_bailable,
            maximum_punishment=schema.maximum_punishment,
        )

        stored = self.section_repo.create_section(section)
        return SectionResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Retrieve
    # ----------------------------------------------------------

    def get_section(self, section_id: str) -> SectionResponse:
        """
        Retrieve Section details.
        """
        section = self.section_repo.get_section_by_id(section_id)
        if section is None:
            raise SectionNotFoundException(section_id)
        return SectionResponse.model_validate(section)

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    def update_section(self, section_id: str, schema: SectionUpdate) -> SectionResponse:
        """
        Update a Section master record.
        """
        existing = self.section_repo.get_section_by_id(section_id)
        if existing is None:
            raise SectionNotFoundException(section_id)

        updates = schema.model_dump(exclude_unset=True)

        if "section_number" in updates:
            updated_num = self.normalize_section_number(updates["section_number"])
            if updated_num != existing.section_number:
                # Check duplicate
                other = self.section_repo.get_section_by_number(existing.act_id, updated_num)
                if other is not None and other.section_id != section_id:
                    raise DuplicateSectionException(updated_num, existing.act_id)
                updates["section_number"] = updated_num

        if "title" in updates:
            updates["title"] = updates["title"].strip()

        updated_section = existing.model_copy(update=updates)
        stored = self.section_repo.update_section(updated_section)

        if stored is None:
            raise SectionNotFoundException(section_id)

        return SectionResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    def delete_section(self, section_id: str) -> None:
        """
        Delete a Section from the catalog.
        """
        existing = self.section_repo.get_section_by_id(section_id)
        if existing is None:
            raise SectionNotFoundException(section_id)
        self.section_repo.delete_section(section_id)

    # ----------------------------------------------------------
    # Search
    # ----------------------------------------------------------

    def search_sections(self, options: SectionQueryOptions) -> SectionListResponse:
        """
        Search sections globally or filtered by Act.
        """
        records, total = self.section_repo.query_sections(options)
        summaries = [SectionSummary.model_validate(s) for s in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return SectionListResponse(items=summaries, pagination=meta)
