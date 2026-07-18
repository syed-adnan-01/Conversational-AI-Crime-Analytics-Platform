from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.evidence import Evidence
from app.schemas.evidence import EvidenceSortField
from app.common.enums import SortOrder
from app.common.queries.evidence_query import EvidenceQueryOptions


class EvidenceRepository:
    """
    Repository responsible for evidence data access operations.

    During development, evidence is stored in an in-memory collection.
    The interface decouples Service/API layers from physical storage.
    """

    _evidence_list: list[Evidence] = []

    # ----------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory evidence store.
        """
        if cls._evidence_list:
            return

        app_logger.info("Evidence repository initialized.")

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    @classmethod
    def create_evidence(cls, evidence: Evidence) -> Evidence:
        """
        Store an Evidence object in the repository.
        Assigns audit timestamps before storage.
        """
        now = datetime.now()
        stored = evidence.model_copy(
            update={
                "created_at": now,
                "updated_at": now,
            }
        )

        cls._evidence_list.append(stored)

        app_logger.info(
            "Evidence stored | ID=%s | CaseMasterID=%s | EvidenceNo=%s",
            stored.evidence_id,
            stored.case_master_id,
            stored.evidence_number,
        )

        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_evidence_by_id(cls, evidence_id: str) -> Optional[Evidence]:
        """
        Retrieve a single evidence record by its ID.
        """
        return next(
            (e for e in cls._evidence_list if e.evidence_id == evidence_id),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Case Master ID
    # ----------------------------------------------------------

    @classmethod
    def get_case_evidence(cls, case_master_id: str) -> list[Evidence]:
        """
        Retrieve all evidence associated with a specific case directly.
        """
        return [e for e in cls._evidence_list if e.case_master_id == case_master_id]

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    @classmethod
    def update_evidence(cls, evidence: Evidence) -> Optional[Evidence]:
        """
        Replace a stored evidence record with the provided object.
        Performs a full replacement, updating updated_at timestamp.
        """
        evidence_id = evidence.evidence_id
        for index, existing in enumerate(cls._evidence_list):
            if existing.evidence_id == evidence_id:
                updated_record = evidence.model_copy(
                    update={"updated_at": datetime.now()}
                )
                cls._evidence_list[index] = updated_record
                app_logger.info("Evidence updated | ID=%s", evidence_id)
                return updated_record

        return None

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    @classmethod
    def delete_evidence(cls, evidence_id: str) -> bool:
        """
        Delete an evidence record by its ID.
        """
        for index, existing in enumerate(cls._evidence_list):
            if existing.evidence_id == evidence_id:
                del cls._evidence_list[index]
                app_logger.info("Evidence deleted | ID=%s", evidence_id)
                return True

        return False

    # ----------------------------------------------------------
    # Query & Search
    # ----------------------------------------------------------

    @classmethod
    def query_evidence(
        cls, options: EvidenceQueryOptions
    ) -> tuple[list[Evidence], int]:
        """
        Query evidence with filtering, keyword search, sorting, and pagination.
        Returns a tuple of (items_subset, total_count).
        """
        filtered = list(cls._evidence_list)

        # 1. Exact Field Filtering
        if options.case_master_id:
            filtered = [
                e for e in filtered if e.case_master_id == options.case_master_id
            ]

        if options.evidence_type:
            filtered = [e for e in filtered if e.evidence_type == options.evidence_type]

        if options.evidence_category:
            filtered = [e for e in filtered if e.evidence_category == options.evidence_category]

        if options.status:
            filtered = [e for e in filtered if e.status == options.status]

        if options.custody_status:
            filtered = [e for e in filtered if e.custody_status == options.custody_status]

        if options.victim_id:
            filtered = [e for e in filtered if e.victim_id == options.victim_id]

        if options.accused_id:
            filtered = [e for e in filtered if e.accused_id == options.accused_id]

        if options.section_id:
            filtered = [e for e in filtered if e.section_id == options.section_id]

        # 2. Case-Insensitive Keyword / Sub-string Searches
        if options.evidence_number:
            search_num = options.evidence_number.lower()
            filtered = [
                e for e in filtered if search_num in e.evidence_number.lower()
            ]

        if options.title:
            search_title = options.title.lower()
            filtered = [
                e for e in filtered if search_title in e.title.lower()
            ]

        if options.description:
            search_desc = options.description.lower()
            filtered = [
                e for e in filtered if search_desc in e.description.lower()
            ]

        if options.collected_by:
            search_by = options.collected_by.lower()
            filtered = [
                e for e in filtered if search_by in e.collected_by.lower()
            ]

        total_count = len(filtered)

        # 3. Sorting (Whitelist based)
        SORT_FIELDS = {
            EvidenceSortField.EVIDENCE_NUMBER: lambda e: e.evidence_number.lower(),
            EvidenceSortField.TITLE: lambda e: e.title.lower(),
            EvidenceSortField.TYPE: lambda e: e.evidence_type.value,
            EvidenceSortField.STATUS: lambda e: e.status.value,
            EvidenceSortField.COLLECTION_DATE: lambda e: e.collection_date or datetime.min,
            EvidenceSortField.CREATED_DATE: lambda e: e.created_at or datetime.min,
            EvidenceSortField.UPDATED_DATE: lambda e: e.updated_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda e: e.created_at)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        # 4. Pagination
        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
