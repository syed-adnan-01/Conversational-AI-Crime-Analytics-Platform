from copy import deepcopy
from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.victim import Victim
from app.schemas.victim import VictimSortField
from app.common.enums import SortOrder
from app.common.queries.victim_query import VictimQueryOptions



class VictimRepository:
    """
    Repository responsible for victim data access operations.

    During development, victims are stored in an in-memory collection.
    The interface decouples Service/API layers from physical storage.
    """

    _victims: list[Victim] = []

    # ----------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory victim store.
        """
        if cls._victims:
            return

        app_logger.info("Victim repository initialized.")

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    @classmethod
    def create_victim(cls, victim: Victim) -> Victim:
        """
        Store a Victim object in the repository.
        Assigns audit timestamps before storage.
        Note: The ID is generated in the Service layer, not here.
        """
        now = datetime.now()
        stored = victim.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._victims.append(stored)

        app_logger.info(
            "Victim stored | ID=%s | CaseMasterID=%s | Name=%s",
            stored.victim_id,
            stored.case_master_id,
            stored.name,
        )

        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_victim_by_id(cls, victim_id: str) -> Optional[Victim]:
        """
        Retrieve a single victim by its ID.
        """
        return next(
            (v for v in cls._victims if v.victim_id == victim_id),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Case Master ID
    # ----------------------------------------------------------

    @classmethod
    def get_victims_by_case_id(cls, case_master_id: str) -> list[Victim]:
        """
        Retrieve all victims associated with a specific case.
        """
        return [v for v in cls._victims if v.case_master_id == case_master_id]

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    @classmethod
    def update_victim(cls, victim: Victim) -> Optional[Victim]:
        """
        Replace a stored victim with the provided object.
        Performs a full replacement, updating updated_at timestamp.
        """
        victim_id = victim.victim_id
        for index, existing in enumerate(cls._victims):
            if existing.victim_id == victim_id:
                updated_record = victim.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._victims[index] = updated_record
                app_logger.info("Victim updated | ID=%s", victim_id)
                return updated_record

        return None

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    @classmethod
    def delete_victim(cls, victim_id: str) -> bool:
        """
        Delete a victim by its ID.
        """
        for index, existing in enumerate(cls._victims):
            if existing.victim_id == victim_id:
                del cls._victims[index]
                app_logger.info("Victim deleted | ID=%s", victim_id)
                return True

        return False

    # ----------------------------------------------------------
    # Query & Search
    # ----------------------------------------------------------

    @classmethod
    def query_victims(
        cls, options: VictimQueryOptions
    ) -> tuple[list[Victim], int]:
        """
        Query victims with filtering, keyword search, sorting, and pagination.
        Returns a tuple of (items_subset, total_count).
        """
        filtered = list(cls._victims)

        # 1. Filtering
        if options.case_master_id:
            filtered = [
                v for v in filtered if v.case_master_id == options.case_master_id
            ]

        if options.gender:
            filtered = [v for v in filtered if v.gender == options.gender]

        if options.age is not None:
            filtered = [v for v in filtered if v.age == options.age]

        if options.nationality:
            filtered = [
                v
                for v in filtered
                if v.nationality and v.nationality.lower() == options.nationality.lower()
            ]

        if options.occupation:
            filtered = [
                v
                for v in filtered
                if v.occupation and v.occupation.lower() == options.occupation.lower()
            ]

        if options.id_type:
            filtered = [v for v in filtered if v.id_type == options.id_type]

        # 2. Case-Insensitive Keyword Searches
        if options.name:
            search_term = options.name.lower()
            filtered = [v for v in filtered if search_term in v.name.lower()]

        if options.mobile_no:
            filtered = [
                v
                for v in filtered
                if v.mobile_no and options.mobile_no in v.mobile_no
            ]

        if options.email:
            search_email = options.email.lower()
            filtered = [
                v
                for v in filtered
                if v.email and search_email in v.email.lower()
            ]

        if options.id_number:
            search_id = options.id_number.lower()
            filtered = [
                v
                for v in filtered
                if v.id_number and search_id in v.id_number.lower()
            ]

        total_count = len(filtered)

        # 3. Sorting
        SORT_FIELDS = {
            VictimSortField.NAME: lambda v: v.name.lower(),
            VictimSortField.AGE: lambda v: v.age or 0,
            VictimSortField.CREATED_DATE: lambda v: v.created_at or datetime.min,
            VictimSortField.UPDATED_DATE: lambda v: v.updated_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda v: v.created_at)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        # 4. Pagination
        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
