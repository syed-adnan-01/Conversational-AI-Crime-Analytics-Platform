from copy import deepcopy
from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.section import Section
from app.schemas.section import SectionSortField
from app.common.enums import SortOrder
from app.common.queries.section_query import SectionQueryOptions
from app.repository.seed.legal_seed import SEED_SECTIONS


class SectionRepository:
    """
    Repository responsible for Section master data access.
    """

    _sections: list[Section] = []

    # ----------------------------------------------------------
    # Initialization & Seeding
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the repository. Loads default SEED_SECTIONS if empty.
        """
        if cls._sections:
            return

        now = datetime.now()
        for seed in SEED_SECTIONS:
            section = Section(
                section_id=seed["section_id"],
                act_id=seed["act_id"],
                section_number=seed["section_number"],
                title=seed["title"],
                description=seed["description"],
                is_cognizable=seed["is_cognizable"],
                is_bailable=seed["is_bailable"],
                maximum_punishment=seed["maximum_punishment"],
                created_at=now,
                updated_at=now,
            )
            cls._sections.append(section)

        app_logger.info("Section repository initialized with %d seeded sections.", len(cls._sections))

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    @classmethod
    def create_section(cls, section: Section) -> Section:
        """
        Store a new Section master record.
        """
        now = datetime.now()
        stored = section.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )
        cls._sections.append(stored)
        app_logger.info(
            "Section master created | ID=%s | ActID=%s | SecNo=%s",
            stored.section_id,
            stored.act_id,
            stored.section_number,
        )
        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_section_by_id(cls, section_id: str) -> Optional[Section]:
        """
        Retrieve a Section by its ID.
        """
        return next((s for s in cls._sections if s.section_id == section_id), None)

    # ----------------------------------------------------------
    # Retrieve — By Act ID
    # ----------------------------------------------------------

    @classmethod
    def get_sections_by_act(cls, act_id: str) -> list[Section]:
        """
        Retrieve all Sections associated with a specific Act.
        """
        return [s for s in cls._sections if s.act_id == act_id]

    # ----------------------------------------------------------
    # Retrieve — By Section Number within an Act (Unique constraint)
    # ----------------------------------------------------------

    @classmethod
    def get_section_by_number(cls, act_id: str, section_number: str) -> Optional[Section]:
        """
        Retrieve a Section by section number under a specific Act.
        """
        return next(
            (
                s
                for s in cls._sections
                if s.act_id == act_id
                and s.section_number.lower() == section_number.lower()
            ),
            None,
        )

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    @classmethod
    def update_section(cls, section: Section) -> Optional[Section]:
        """
        Replace an existing Section master record.
        """
        section_id = section.section_id
        for index, existing in enumerate(cls._sections):
            if existing.section_id == section_id:
                updated_record = section.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._sections[index] = updated_record
                app_logger.info("Section master updated | ID=%s", section_id)
                return updated_record
        return None

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    @classmethod
    def delete_section(cls, section_id: str) -> bool:
        """
        Delete a Section from the master catalog.
        """
        for index, existing in enumerate(cls._sections):
            if existing.section_id == section_id:
                del cls._sections[index]
                app_logger.info("Section master deleted | ID=%s", section_id)
                return True
        return False

    # ----------------------------------------------------------
    # Query & Search
    # ----------------------------------------------------------

    @classmethod
    def query_sections(
        cls, options: SectionQueryOptions
    ) -> tuple[list[Section], int]:
        """
        Query Sections with sorting, keyword matching, and pagination.
        """
        filtered = list(cls._sections)

        # 1. Filtering & Search
        if options.act_id:
            filtered = [s for s in filtered if s.act_id == options.act_id]

        if options.section_number:
            search_num = options.section_number.lower()
            filtered = [s for s in filtered if search_num in s.section_number.lower()]

        if options.title:
            search_title = options.title.lower()
            filtered = [s for s in filtered if search_title in s.title.lower()]

        if options.is_cognizable is not None:
            filtered = [s for s in filtered if s.is_cognizable == options.is_cognizable]

        if options.is_bailable is not None:
            filtered = [s for s in filtered if s.is_bailable == options.is_bailable]

        total_count = len(filtered)

        # 2. Sorting
        # Natural sorting helper for section numbers (e.g. converting "103" to integer if possible)
        def natural_sort_key(s: Section):
            if options.sort_by == SectionSortField.SECTION_NUMBER:
                # Try to extract leading digits for proper numeric sorting, fallback to string lowercase
                num_str = "".join(c for c in s.section_number if c.isdigit())
                num = int(num_str) if num_str else 0
                return (num, s.section_number.lower())
            elif options.sort_by == SectionSortField.TITLE:
                return s.title.lower()
            elif options.sort_by == SectionSortField.CREATED_DATE:
                return s.created_at or datetime.min
            elif options.sort_by == SectionSortField.UPDATED_DATE:
                return s.updated_at or datetime.min
            return s.created_at or datetime.min

        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=natural_sort_key, reverse=reverse)

        # 3. Pagination
        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
