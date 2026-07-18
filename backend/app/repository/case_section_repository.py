from copy import deepcopy
from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.case_section import CaseSectionAssociation
from app.common.enums import SortOrder
from app.common.queries.case_section_query import CaseSectionQueryOptions


class CaseSectionRepository:
    """
    Repository responsible for Case Section Association data access.
    """

    _associations: list[CaseSectionAssociation] = []

    # ----------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the repository.
        """
        if cls._associations:
            return
        app_logger.info("Case Section Association repository initialized.")

    # ----------------------------------------------------------
    # Assign Section to Case
    # ----------------------------------------------------------

    @classmethod
    def assign_section_to_case(
        cls, association: CaseSectionAssociation
    ) -> CaseSectionAssociation:
        """
        Assign a legal section to a case by storing the association.
        """
        now = datetime.now()
        stored = association.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )
        cls._associations.append(stored)
        app_logger.info(
            "Case section assigned | ID=%s | CaseID=%s | SectionID=%s",
            stored.association_id,
            stored.case_master_id,
            stored.section_id,
        )
        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_association_by_id(
        cls, association_id: str
    ) -> Optional[CaseSectionAssociation]:
        """
        Retrieve an association record by its ID.
        """
        return next(
            (a for a in cls._associations if a.association_id == association_id),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Case & Section (Unique constraint checking)
    # ----------------------------------------------------------

    @classmethod
    def get_association_by_case_and_section(
        cls, case_master_id: str, section_id: str
    ) -> Optional[CaseSectionAssociation]:
        """
        Retrieve an association by case and section.
        """
        return next(
            (
                a
                for a in cls._associations
                if a.case_master_id == case_master_id
                and a.section_id == section_id
            ),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Case ID
    # ----------------------------------------------------------

    @classmethod
    def get_case_sections(cls, case_master_id: str) -> list[CaseSectionAssociation]:
        """
        Retrieve all associations for a specific case.
        """
        return [
            a for a in cls._associations if a.case_master_id == case_master_id
        ]

    # ----------------------------------------------------------
    # Remove Assignment
    # ----------------------------------------------------------

    @classmethod
    def remove_section(cls, association_id: str) -> bool:
        """
        Remove/Delete a case-section link.
        """
        for index, existing in enumerate(cls._associations):
            if existing.association_id == association_id:
                del cls._associations[index]
                app_logger.info("Case section assignment deleted | ID=%s", association_id)
                return True
        return False

    # ----------------------------------------------------------
    # Query & Search
    # ----------------------------------------------------------

    @classmethod
    def query_case_sections(
        cls, options: CaseSectionQueryOptions
    ) -> tuple[list[CaseSectionAssociation], int]:
        """
        Query case section associations.
        """
        filtered = list(cls._associations)

        # 1. Filtering
        if options.case_master_id:
            filtered = [
                a for a in filtered if a.case_master_id == options.case_master_id
            ]

        if options.section_id:
            filtered = [a for a in filtered if a.section_id == options.section_id]

        if options.remarks:
            search_remarks = options.remarks.lower()
            filtered = [
                a
                for a in filtered
                if a.remarks and search_remarks in a.remarks.lower()
            ]

        total_count = len(filtered)

        # 2. Sorting (by creation timestamp)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=lambda a: a.created_at or datetime.min, reverse=reverse)

        # 3. Pagination
        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
