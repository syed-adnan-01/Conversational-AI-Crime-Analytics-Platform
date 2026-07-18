from copy import deepcopy
from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.accused import Accused
from app.schemas.accused import AccusedSortField
from app.common.enums import SortOrder
from app.common.queries.accused_query import AccusedQueryOptions


class AccusedRepository:
    """
    Repository responsible for accused data access operations.

    During development, accused are stored in an in-memory collection.
    The interface decouples Service/API layers from physical storage.
    """

    _accused: list[Accused] = []

    # ----------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory accused store.
        """
        if cls._accused:
            return

        app_logger.info("Accused repository initialized.")

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    @classmethod
    def create_accused(cls, accused: Accused) -> Accused:
        """
        Store an Accused object in the repository.
        Assigns audit timestamps before storage.
        Note: The ID is generated in the Service layer, not here.
        """
        now = datetime.now()
        stored = accused.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._accused.append(stored)

        app_logger.info(
            "Accused stored | ID=%s | CaseMasterID=%s | Name=%s",
            stored.accused_id,
            stored.case_master_id,
            stored.name,
        )

        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_accused_by_id(cls, accused_id: str) -> Optional[Accused]:
        """
        Retrieve a single accused by its ID.
        """
        return next(
            (a for a in cls._accused if a.accused_id == accused_id),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Case Master ID
    # ----------------------------------------------------------

    @classmethod
    def get_accused_by_case_id(cls, case_master_id: str) -> list[Accused]:
        """
        Retrieve all accused associated with a specific case.
        """
        return [a for a in cls._accused if a.case_master_id == case_master_id]

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    @classmethod
    def update_accused(cls, accused: Accused) -> Optional[Accused]:
        """
        Replace a stored accused with the provided object.
        Performs a full replacement, updating updated_at timestamp.
        """
        accused_id = accused.accused_id
        for index, existing in enumerate(cls._accused):
            if existing.accused_id == accused_id:
                updated_record = accused.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._accused[index] = updated_record
                app_logger.info("Accused updated | ID=%s", accused_id)
                return updated_record

        return None

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    @classmethod
    def delete_accused(cls, accused_id: str) -> bool:
        """
        Delete an accused by its ID.
        """
        for index, existing in enumerate(cls._accused):
            if existing.accused_id == accused_id:
                del cls._accused[index]
                app_logger.info("Accused deleted | ID=%s", accused_id)
                return True

        return False

    # ----------------------------------------------------------
    # Query & Search
    # ----------------------------------------------------------

    @classmethod
    def query_accused(
        cls, options: AccusedQueryOptions
    ) -> tuple[list[Accused], int]:
        """
        Query accused with filtering, keyword search, sorting, and pagination.
        Returns a tuple of (items_subset, total_count).
        """
        filtered = list(cls._accused)

        # 1. Filtering
        if options.case_master_id:
            filtered = [
                a for a in filtered if a.case_master_id == options.case_master_id
            ]

        if options.gender:
            filtered = [a for a in filtered if a.gender == options.gender]

        if options.age is not None:
            filtered = [a for a in filtered if a.age == options.age]

        if options.nationality:
            filtered = [
                a
                for a in filtered
                if a.nationality and a.nationality.lower() == options.nationality.lower()
            ]

        if options.occupation:
            filtered = [
                a
                for a in filtered
                if a.occupation and a.occupation.lower() == options.occupation.lower()
            ]

        if options.id_type:
            filtered = [a for a in filtered if a.id_type == options.id_type]

        # 2. Case-Insensitive Keyword Searches
        if options.name:
            search_term = options.name.lower()
            filtered = [a for a in filtered if search_term in a.name.lower()]

        if options.mobile_no:
            filtered = [
                a
                for a in filtered
                if a.mobile_no and options.mobile_no in a.mobile_no
            ]

        if options.email:
            search_email = options.email.lower()
            filtered = [
                a
                for a in filtered
                if a.email and search_email in a.email.lower()
            ]

        if options.id_number:
            search_id = options.id_number.lower()
            filtered = [
                a
                for a in filtered
                if a.id_number and search_id in a.id_number.lower()
            ]

        total_count = len(filtered)

        # 3. Sorting
        SORT_FIELDS = {
            AccusedSortField.NAME: lambda a: a.name.lower(),
            AccusedSortField.AGE: lambda a: a.age or 0,
            AccusedSortField.CREATED_DATE: lambda a: a.created_at or datetime.min,
            AccusedSortField.UPDATED_DATE: lambda a: a.updated_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda a: a.created_at)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        # 4. Pagination
        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
