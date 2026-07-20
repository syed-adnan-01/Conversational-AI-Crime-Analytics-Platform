from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.witness import Witness
from app.schemas.witness import WitnessSortField
from app.common.enums import SortOrder
from app.common.queries.witness_query import WitnessQueryOptions


class WitnessRepository:
    """
    Repository responsible for Witness data access operations.
    In-memory collection for development phase.
    """

    _witnesses: list[Witness] = []

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory witness store.
        """
        if cls._witnesses:
            return
        app_logger.info("Witness repository initialized.")

    @classmethod
    def create_witness(cls, witness: Witness) -> Witness:
        """
        Store a Witness object in the repository.
        Assigns audit timestamps before storage.
        """
        now = datetime.now()
        stored = witness.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._witnesses.append(stored)

        app_logger.info(
            "Witness stored | ID=%s | CaseID=%s | Name=%s",
            stored.witness_id,
            stored.case_master_id,
            stored.name,
        )

        return stored

    @classmethod
    def get_witness_by_id(cls, witness_id: str) -> Optional[Witness]:
        """
        Retrieve a single witness by ID.
        """
        return next((w for w in cls._witnesses if w.witness_id == witness_id), None)

    @classmethod
    def get_witnesses_by_case_id(cls, case_master_id: str) -> list[Witness]:
        """
        Retrieve all witnesses associated with a specific case.
        """
        return [w for w in cls._witnesses if w.case_master_id == case_master_id]

    @classmethod
    def update_witness(cls, witness: Witness) -> Optional[Witness]:
        """
        Update a stored witness record.
        """
        witness_id = witness.witness_id
        for index, existing in enumerate(cls._witnesses):
            if existing.witness_id == witness_id:
                updated_record = witness.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._witnesses[index] = updated_record
                app_logger.info("Witness updated | ID=%s", witness_id)
                return updated_record

        return None

    @classmethod
    def delete_witness(cls, witness_id: str) -> bool:
        """
        Delete a witness record by ID.
        """
        for index, existing in enumerate(cls._witnesses):
            if existing.witness_id == witness_id:
                del cls._witnesses[index]
                app_logger.info("Witness deleted | ID=%s", witness_id)
                return True

        return False

    @classmethod
    def query_witnesses(
        cls, options: WitnessQueryOptions
    ) -> tuple[list[Witness], int]:
        """
        Query witnesses with filtering, sorting, and pagination.
        """
        filtered = list(cls._witnesses)

        if options.case_master_id:
            filtered = [w for w in filtered if w.case_master_id == options.case_master_id]

        if options.gender:
            filtered = [w for w in filtered if w.gender == options.gender]

        if options.is_hostile is not None:
            filtered = [w for w in filtered if w.is_hostile == options.is_hostile]

        if options.id_type:
            filtered = [w for w in filtered if w.id_type == options.id_type]

        if options.name:
            search_name = options.name.lower()
            filtered = [w for w in filtered if search_name in w.name.lower()]

        if options.mobile_no:
            search_mobile = options.mobile_no
            filtered = [w for w in filtered if w.mobile_no and search_mobile in w.mobile_no]

        total_count = len(filtered)

        SORT_FIELDS = {
            WitnessSortField.NAME: lambda w: w.name.lower(),
            WitnessSortField.AGE: lambda w: w.age or 0,
            WitnessSortField.STATEMENT_DATE: lambda w: w.statement_date or datetime.min,
            WitnessSortField.CREATED_AT: lambda w: w.created_at or datetime.min,
            WitnessSortField.UPDATED_AT: lambda w: w.updated_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda w: w.created_at or datetime.min)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
