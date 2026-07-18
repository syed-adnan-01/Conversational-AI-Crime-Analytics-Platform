from copy import deepcopy
from datetime import datetime
from typing import Optional

from app.core.logging import complainant_logger
from app.models.complainant import Complainant
from app.schemas.complainant import ComplainantSortField, SortOrder
from app.common.queries.complainant_query import ComplainantQueryOptions


class ComplainantRepository:
    """
    Repository responsible for complainant data access operations.

    During development, complainants are stored in an in-memory collection.
    The interface decouples Service/API layers from physical storage.
    """

    _complainants: list[Complainant] = []

    # ----------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory complainant store.
        """
        if cls._complainants:
            return

        complainant_logger.info("Complainant repository initialized.")

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    @classmethod
    def create_complainant(cls, complainant: Complainant) -> Complainant:
        """
        Store a Complainant object in the repository.
        Assigns audit timestamps before storage.
        Note: The ID is generated in the Service layer, not here.
        """
        now = datetime.now()
        stored = complainant.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._complainants.append(stored)

        complainant_logger.info(
            "Complainant stored | ID=%s | CaseMasterID=%s | Name=%s",
            stored.complainant_id,
            stored.case_master_id,
            stored.name,
        )

        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_complainant_by_id(cls, complainant_id: str) -> Optional[Complainant]:
        """
        Retrieve a single complainant by its ID.
        """
        return next(
            (c for c in cls._complainants if c.complainant_id == complainant_id),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Case Master ID
    # ----------------------------------------------------------

    @classmethod
    def get_complainants_by_case_id(cls, case_master_id: str) -> list[Complainant]:
        """
        Retrieve all complainants associated with a specific case.
        """
        return [c for c in cls._complainants if c.case_master_id == case_master_id]

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    @classmethod
    def update_complainant(cls, complainant: Complainant) -> Optional[Complainant]:
        """
        Replace a stored complainant with the provided object.
        Performs a full replacement, updating updated_at timestamp.
        """
        complainant_id = complainant.complainant_id
        for index, existing in enumerate(cls._complainants):
            if existing.complainant_id == complainant_id:
                updated_record = complainant.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._complainants[index] = updated_record
                complainant_logger.info("Complainant updated | ID=%s", complainant_id)
                return updated_record

        return None

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    @classmethod
    def delete_complainant(cls, complainant_id: str) -> bool:
        """
        Delete a complainant by its ID.
        """
        for index, existing in enumerate(cls._complainants):
            if existing.complainant_id == complainant_id:
                del cls._complainants[index]
                complainant_logger.info("Complainant deleted | ID=%s", complainant_id)
                return True

        return False

    # ----------------------------------------------------------
    # Query & Search
    # ----------------------------------------------------------

    @classmethod
    def query_complainants(
        cls, options: ComplainantQueryOptions
    ) -> tuple[list[Complainant], int]:
        """
        Query complainants with filtering, keyword search, sorting, and pagination.
        Returns a tuple of (items_subset, total_count).
        """
        filtered = list(cls._complainants)

        # 1. Filtering
        if options.case_master_id:
            filtered = [
                c for c in filtered if c.case_master_id == options.case_master_id
            ]

        if options.gender:
            filtered = [c for c in filtered if c.gender == options.gender]

        if options.mobile_no:
            filtered = [c for c in filtered if c.mobile_no == options.mobile_no]

        if options.email:
            filtered = [
                c
                for c in filtered
                if c.email and c.email.lower() == options.email.lower()
            ]

        # 2. Case-Insensitive Keyword Search on Name
        if options.name:
            search_term = options.name.lower()
            filtered = [c for c in filtered if search_term in c.name.lower()]

        total_count = len(filtered)

        # 3. Sorting
        SORT_FIELDS = {
            ComplainantSortField.NAME: lambda c: c.name.lower(),
            ComplainantSortField.AGE: lambda c: c.age or 0,
            ComplainantSortField.CREATED_DATE: lambda c: c.created_at or datetime.min,
            ComplainantSortField.UPDATED_DATE: lambda c: c.updated_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda c: c.created_at)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        # 4. Pagination
        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
