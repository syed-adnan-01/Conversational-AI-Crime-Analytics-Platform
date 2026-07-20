from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.court_proceeding import CourtProceeding
from app.schemas.court_proceeding import CourtProceedingSortField
from app.common.enums import SortOrder
from app.common.queries.court_proceeding_query import CourtProceedingQueryOptions


class CourtProceedingRepository:
    """
    Repository responsible for Court Proceeding data access operations.
    """

    _proceedings: list[CourtProceeding] = []

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory court proceeding store.
        """
        if cls._proceedings:
            return
        app_logger.info("Court proceeding repository initialized.")

    @classmethod
    def create_proceeding(cls, proceeding: CourtProceeding) -> CourtProceeding:
        """
        Store a CourtProceeding object in the repository.
        """
        now = datetime.now()
        stored = proceeding.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._proceedings.append(stored)

        app_logger.info(
            "Court proceeding stored | ID=%s | CaseID=%s | Stage=%s",
            stored.proceeding_id,
            stored.case_master_id,
            stored.stage,
        )

        return stored

    @classmethod
    def get_proceeding_by_id(cls, proceeding_id: str) -> Optional[CourtProceeding]:
        """
        Retrieve a single court proceeding by ID.
        """
        return next((cp for cp in cls._proceedings if cp.proceeding_id == proceeding_id), None)

    @classmethod
    def get_proceedings_by_case_id(cls, case_master_id: str) -> list[CourtProceeding]:
        """
        Retrieve all court proceedings associated with a specific case.
        """
        return [cp for cp in cls._proceedings if cp.case_master_id == case_master_id]

    @classmethod
    def update_proceeding(cls, proceeding: CourtProceeding) -> Optional[CourtProceeding]:
        """
        Update a stored court proceeding record.
        """
        proceeding_id = proceeding.proceeding_id
        for index, existing in enumerate(cls._proceedings):
            if existing.proceeding_id == proceeding_id:
                updated_record = proceeding.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._proceedings[index] = updated_record
                app_logger.info("Court proceeding updated | ID=%s", proceeding_id)
                return updated_record

        return None

    @classmethod
    def delete_proceeding(cls, proceeding_id: str) -> bool:
        """
        Delete a court proceeding record by ID.
        """
        for index, existing in enumerate(cls._proceedings):
            if existing.proceeding_id == proceeding_id:
                del cls._proceedings[index]
                app_logger.info("Court proceeding deleted | ID=%s", proceeding_id)
                return True

        return False

    @classmethod
    def query_proceedings(
        cls, options: CourtProceedingQueryOptions
    ) -> tuple[list[CourtProceeding], int]:
        """
        Query court proceedings with filtering, sorting, and pagination.
        """
        filtered = list(cls._proceedings)

        if options.case_master_id:
            filtered = [cp for cp in filtered if cp.case_master_id == options.case_master_id]

        if options.stage:
            filtered = [cp for cp in filtered if cp.stage == options.stage]

        if options.court_name:
            search_court = options.court_name.lower()
            filtered = [cp for cp in filtered if search_court in cp.court_name.lower()]

        if options.judge_name:
            search_judge = options.judge_name.lower()
            filtered = [cp for cp in filtered if search_judge in cp.judge_name.lower()]

        total_count = len(filtered)

        SORT_FIELDS = {
            CourtProceedingSortField.HEARING_DATE: lambda cp: cp.hearing_date or datetime.min,
            CourtProceedingSortField.STAGE: lambda cp: cp.stage.value,
            CourtProceedingSortField.NEXT_HEARING_DATE: lambda cp: cp.next_hearing_date or datetime.min,
            CourtProceedingSortField.CREATED_AT: lambda cp: cp.created_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda cp: cp.hearing_date or datetime.min)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
