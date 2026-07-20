from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.arrest import Arrest, ArrestStatus
from app.schemas.arrest import ArrestSortField
from app.common.enums import SortOrder
from app.common.queries.arrest_query import ArrestQueryOptions


class ArrestRepository:
    """
    Repository responsible for Arrest data access operations.
    """

    _arrests: list[Arrest] = []

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory arrest store.
        """
        if cls._arrests:
            return
        app_logger.info("Arrest repository initialized.")

    @classmethod
    def create_arrest(cls, arrest: Arrest) -> Arrest:
        """
        Store an Arrest object in the repository.
        """
        now = datetime.now()
        stored = arrest.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._arrests.append(stored)

        app_logger.info(
            "Arrest stored | ID=%s | CaseID=%s | AccusedID=%s",
            stored.arrest_id,
            stored.case_master_id,
            stored.accused_id,
        )

        return stored

    @classmethod
    def get_arrest_by_id(cls, arrest_id: str) -> Optional[Arrest]:
        """
        Retrieve a single arrest by ID.
        """
        return next((a for a in cls._arrests if a.arrest_id == arrest_id), None)

    @classmethod
    def get_arrests_by_case_id(cls, case_master_id: str) -> list[Arrest]:
        """
        Retrieve all arrests associated with a specific case.
        """
        return [a for a in cls._arrests if a.case_master_id == case_master_id]

    @classmethod
    def get_arrests_by_accused_id(cls, accused_id: str) -> list[Arrest]:
        """
        Retrieve all arrests for a specific accused.
        """
        return [a for a in cls._arrests if a.accused_id == accused_id]

    @classmethod
    def update_arrest(cls, arrest: Arrest) -> Optional[Arrest]:
        """
        Update a stored arrest record.
        """
        arrest_id = arrest.arrest_id
        for index, existing in enumerate(cls._arrests):
            if existing.arrest_id == arrest_id:
                updated_record = arrest.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._arrests[index] = updated_record
                app_logger.info("Arrest updated | ID=%s", arrest_id)
                return updated_record

        return None

    @classmethod
    def delete_arrest(cls, arrest_id: str) -> bool:
        """
        Delete an arrest record by ID.
        """
        for index, existing in enumerate(cls._arrests):
            if existing.arrest_id == arrest_id:
                del cls._arrests[index]
                app_logger.info("Arrest deleted | ID=%s", arrest_id)
                return True

        return False

    @classmethod
    def query_arrests(
        cls, options: ArrestQueryOptions
    ) -> tuple[list[Arrest], int]:
        """
        Query arrests with filtering, sorting, and pagination.
        """
        filtered = list(cls._arrests)

        if options.case_master_id:
            filtered = [a for a in filtered if a.case_master_id == options.case_master_id]

        if options.accused_id:
            filtered = [a for a in filtered if a.accused_id == options.accused_id]

        if options.status:
            filtered = [a for a in filtered if a.status == options.status]

        if options.arresting_officer:
            search_officer = options.arresting_officer.lower()
            filtered = [a for a in filtered if search_officer in a.arresting_officer.lower()]

        if options.arrest_location:
            search_loc = options.arrest_location.lower()
            filtered = [a for a in filtered if search_loc in a.arrest_location.lower()]

        total_count = len(filtered)

        SORT_FIELDS = {
            ArrestSortField.ARREST_DATE: lambda a: a.arrest_date or datetime.min,
            ArrestSortField.STATUS: lambda a: a.status.value,
            ArrestSortField.CREATED_AT: lambda a: a.created_at or datetime.min,
            ArrestSortField.UPDATED_AT: lambda a: a.updated_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda a: a.arrest_date or datetime.min)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
