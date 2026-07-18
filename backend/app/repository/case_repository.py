from copy import deepcopy
from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.core.logging import case_logger
from app.models.case_master import CaseMaster
from app.schemas.case import SortField, SortOrder
from app.common.queries.case_query import CaseQueryOptions


class CaseRepository:
    """
    Repository responsible for case data access operations.

    During development, cases are stored in an in-memory collection.
    The public interface is designed so that this implementation can
    be replaced by CatalystCaseRepository or SQLCaseRepository
    without modifying the Service or API layers.

    Thread Safety:
        The current in-memory implementation uses a class-level list.
        In production, this will be replaced by a database-backed
        store where concurrency is managed by the database engine.
        If the in-memory store is used under concurrent load,
        a threading.Lock should guard all write operations
        (_cases.append, list assignment, list removal).
    """

    # Internal in-memory case store
    _cases: list[CaseMaster] = []

    # ----------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory case store.

        Follows the same idempotency pattern as UserRepository.
        In production, this method would establish a database
        connection pool or verify table existence.
        """

        if cls._cases:
            return

        case_logger.info("Case repository initialized.")

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    @classmethod
    def create_case(cls, case: CaseMaster) -> CaseMaster:
        """
        Store a CaseMaster object in the repository.

        Assigns a system-generated case_master_id and populates
        audit timestamps (created_at, updated_at) before storage.

        Args:
            case: The CaseMaster domain object to store.

        Returns:
            The stored CaseMaster with generated ID and timestamps.

        Future SQL behaviour:
            Will execute an INSERT statement and return the
            row with the database-generated primary key.
        """

        stored = case.model_copy(
            update={
                "case_master_id": f"CM-{uuid4().hex[:12].upper()}",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )

        cls._cases.append(stored)

        case_logger.info(
            "Case stored | ID=%s | CrimeNo=%s",
            stored.case_master_id,
            stored.crime_no,
        )

        return stored

    # ----------------------------------------------------------
    # Retrieve — By ID
    # ----------------------------------------------------------

    @classmethod
    def get_case_by_id(
        cls, case_master_id: str,
    ) -> Optional[CaseMaster]:
        """
        Retrieve a single case by its system-generated ID.

        Args:
            case_master_id: The unique case identifier.

        Returns:
            The matching CaseMaster, or None if not found.

        Future SQL behaviour:
            Will execute SELECT ... WHERE case_master_id = ?
        """

        return next(
            (
                case
                for case in cls._cases
                if case.case_master_id == case_master_id
            ),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Case Number
    # ----------------------------------------------------------

    @classmethod
    def get_case_by_case_number(
        cls, case_no: str,
    ) -> Optional[CaseMaster]:
        """
        Retrieve a single case by its court-assigned case number.

        Args:
            case_no: The court-assigned case number.

        Returns:
            The matching CaseMaster, or None if not found.

        Future SQL behaviour:
            Will execute SELECT ... WHERE case_no = ?
        """

        return next(
            (
                case
                for case in cls._cases
                if case.case_no == case_no
            ),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — By Crime Number
    # ----------------------------------------------------------

    @classmethod
    def get_case_by_crime_number(
        cls, crime_no: str,
    ) -> Optional[CaseMaster]:
        """
        Retrieve a single case by its police-assigned crime number.

        Args:
            crime_no: The official crime number.

        Returns:
            The matching CaseMaster, or None if not found.

        Future SQL behaviour:
            Will execute SELECT ... WHERE crime_no = ?
        """

        return next(
            (
                case
                for case in cls._cases
                if case.crime_no == crime_no
            ),
            None,
        )

    # ----------------------------------------------------------
    # Retrieve — All Cases
    # ----------------------------------------------------------

    @classmethod
    def get_all_cases(cls) -> list[CaseMaster]:
        """
        Retrieve all stored cases.

        Returns:
            A list of all CaseMaster objects in the store.

        Future SQL behaviour:
            Will execute SELECT * with default ordering
            and pagination applied at the service layer.
        """

        return list(cls._cases)

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    @classmethod
    def update_case(cls, case: CaseMaster) -> Optional[CaseMaster]:
        """
        Replace a stored case with the provided object.

        Performs a full replacement — does not merge individual
        fields. The updated_at timestamp is refreshed automatically.

        Args:
            case: The complete CaseMaster object to store.
                  Must contain a valid case_master_id.

        Returns:
            The updated CaseMaster, or None if the ID was not found.

        Future SQL behaviour:
            Will execute UPDATE ... SET ... WHERE case_master_id = ?

        Thread Safety:
            In production, optimistic locking (version column) or
            database-level row locking should be used to prevent
            lost updates under concurrent modification.
        """

        for index, existing in enumerate(cls._cases):
            if existing.case_master_id == case.case_master_id:

                updated = case.model_copy(
                    update={"updated_at": datetime.now()}
                )

                cls._cases[index] = updated

                case_logger.info(
                    "Case updated | ID=%s",
                    updated.case_master_id,
                )

                return updated

        return None

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    @classmethod
    def delete_case(cls, case_master_id: str) -> bool:
        """
        Remove a case from the store by its ID.

        Args:
            case_master_id: The unique case identifier to remove.

        Returns:
            True if the case was found and removed, False otherwise.

        Future SQL behaviour:
            Will execute DELETE ... WHERE case_master_id = ?
            May implement soft-delete (is_deleted flag) instead.
        """

        for index, existing in enumerate(cls._cases):
            if existing.case_master_id == case_master_id:

                cls._cases.pop(index)

                case_logger.info(
                    "Case deleted | ID=%s",
                    case_master_id,
                )

                return True

        return False

    # ----------------------------------------------------------
    # Existence Check
    # ----------------------------------------------------------

    @classmethod
    def case_exists(cls, case_master_id: str) -> bool:
        """
        Check whether a case with the given ID exists.

        Args:
            case_master_id: The unique case identifier.

        Returns:
            True if found, False otherwise.

        Future SQL behaviour:
            Will execute SELECT EXISTS(...) for efficiency.
        """

        return any(
            case.case_master_id == case_master_id
            for case in cls._cases
        )

    # ----------------------------------------------------------
    # Search & Advanced Querying
    # ----------------------------------------------------------

    _SORT_ACCESSORS = {
        SortField.REGISTERED_DATE: lambda c: c.crime_registered_date,
        SortField.INCIDENT_DATE: lambda c: c.incident_from_date or datetime.min,
        SortField.CASE_NUMBER: lambda c: c.case_no or "",
        SortField.CRIME_NUMBER: lambda c: c.crime_no,
        SortField.CREATED_DATE: lambda c: c.created_at or datetime.min,
        SortField.UPDATED_DATE: lambda c: c.updated_at or datetime.min,
    }

    @classmethod
    def query_cases(
        cls,
        options: CaseQueryOptions,
    ) -> tuple[list[CaseMaster], int]:
        """
        Query cases using filtering, keyword search, sorting, and pagination.

        Returns:
            A tuple of (matching CaseMaster objects, total count before pagination).
        """
        results = cls._cases

        # --- Filtering ---
        if options.crime_no is not None:
            results = [c for c in results if c.crime_no == options.crime_no]

        if options.case_no is not None:
            results = [c for c in results if c.case_no == options.case_no]

        if options.date_from is not None:
            results = [c for c in results if c.crime_registered_date >= options.date_from]

        if options.date_to is not None:
            results = [c for c in results if c.crime_registered_date <= options.date_to]

        if options.incident_from_date is not None:
            results = [
                c for c in results
                if c.incident_from_date and c.incident_from_date >= options.incident_from_date
            ]

        if options.incident_to_date is not None:
            results = [
                c for c in results
                if c.incident_to_date and c.incident_to_date <= options.incident_to_date
            ]

        if options.case_status_id is not None:
            results = [c for c in results if c.case_status_id == options.case_status_id]

        if options.case_category_id is not None:
            results = [c for c in results if c.case_category_id == options.case_category_id]

        if options.gravity_offence_id is not None:
            results = [c for c in results if c.gravity_offence_id == options.gravity_offence_id]

        if options.crime_major_head_id is not None:
            results = [c for c in results if c.crime_major_head_id == options.crime_major_head_id]

        if options.crime_minor_head_id is not None:
            results = [c for c in results if c.crime_minor_head_id == options.crime_minor_head_id]

        if options.police_station_id is not None:
            results = [c for c in results if c.police_station_id == options.police_station_id]

        if options.police_person_id is not None:
            results = [c for c in results if c.police_person_id == options.police_person_id]

        if options.court_id is not None:
            results = [c for c in results if c.court_id == options.court_id]

        # Simulate district and state lookup using case-insensitive check on brief_facts
        if options.district is not None:
            dist_kw = options.district.lower()
            results = [c for c in results if c.brief_facts and dist_kw in c.brief_facts.lower()]

        if options.state is not None:
            state_kw = options.state.lower()
            results = [c for c in results if c.brief_facts and state_kw in c.brief_facts.lower()]

        # --- Keyword Search ---
        if options.brief_facts is not None:
            kw = options.brief_facts.lower()
            results = [
                c for c in results
                if (c.brief_facts and kw in c.brief_facts.lower())
                or (c.case_no and kw in c.case_no.lower())
                or (c.crime_no and kw in c.crime_no.lower())
            ]

        # --- Sorting ---
        accessor = cls._SORT_ACCESSORS.get(options.sort_by)
        if accessor:
            reverse = options.sort_order == SortOrder.DESC
            results = sorted(results, key=accessor, reverse=reverse)

        # --- Pagination ---
        total = len(results)
        start = (options.page - 1) * options.page_size
        end = start + options.page_size
        paginated_results = results[start:end]

        return paginated_results, total

    @classmethod
    def search_cases(
        cls,
        crime_no: Optional[str] = None,
        case_no: Optional[str] = None,
        brief_facts: Optional[str] = None,
    ) -> list[CaseMaster]:
        """
        Search cases using basic field matching.

        All parameters are optional. Only non-None parameters
        are applied as filters. Multiple filters use AND logic.

        Args:
            crime_no:    Exact match on crime number.
            case_no:     Exact match on case number.
            brief_facts: Substring match on brief facts (case-insensitive).

        Returns:
            A list of matching CaseMaster objects.

        Future SQL behaviour:
            Will translate filters into a WHERE clause with
            parameterized queries. Full-text search will replace
            the brief_facts substring match.
        """

        results = cls._cases

        if crime_no is not None:
            results = [
                c for c in results
                if c.crime_no == crime_no
            ]

        if case_no is not None:
            results = [
                c for c in results
                if c.case_no == case_no
            ]

        if brief_facts is not None:
            keyword = brief_facts.lower()
            results = [
                c for c in results
                if c.brief_facts
                and keyword in c.brief_facts.lower()
            ]

        return results

    # ----------------------------------------------------------
    # Filter — By Status
    # ----------------------------------------------------------

    @classmethod
    def filter_by_status(
        cls, case_status_id: int,
    ) -> list[CaseMaster]:
        """
        Filter cases by lifecycle status.

        Args:
            case_status_id: The status ID to filter by.

        Returns:
            A list of matching CaseMaster objects.

        Future SQL behaviour:
            Will execute SELECT ... WHERE case_status_id = ?
        """

        return [
            case for case in cls._cases
            if case.case_status_id == case_status_id
        ]

    # ----------------------------------------------------------
    # Filter — By Police Station
    # ----------------------------------------------------------

    @classmethod
    def filter_by_police_station(
        cls, police_station_id: int,
    ) -> list[CaseMaster]:
        """
        Filter cases by registering police station.

        Args:
            police_station_id: The police station ID to filter by.

        Returns:
            A list of matching CaseMaster objects.

        Future SQL behaviour:
            Will execute SELECT ... WHERE police_station_id = ?
        """

        return [
            case for case in cls._cases
            if case.police_station_id == police_station_id
        ]

    # ----------------------------------------------------------
    # Filter — By Date Range
    # ----------------------------------------------------------

    @classmethod
    def filter_by_date_range(
        cls,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> list[CaseMaster]:
        """
        Filter cases by registration date range.

        Either bound may be omitted for an open-ended range.

        Args:
            date_from: Include cases registered on or after this date.
            date_to:   Include cases registered on or before this date.

        Returns:
            A list of matching CaseMaster objects.

        Future SQL behaviour:
            Will execute SELECT ... WHERE crime_registered_date
            BETWEEN ? AND ?
        """

        results = cls._cases

        if date_from is not None:
            results = [
                c for c in results
                if c.crime_registered_date >= date_from
            ]

        if date_to is not None:
            results = [
                c for c in results
                if c.crime_registered_date <= date_to
            ]

        return results

    # ----------------------------------------------------------
    # Filter — By Crime Head
    # ----------------------------------------------------------

    @classmethod
    def filter_by_crime_head(
        cls, crime_major_head_id: int,
    ) -> list[CaseMaster]:
        """
        Filter cases by major crime classification head.

        Args:
            crime_major_head_id: The major crime head ID to filter by.

        Returns:
            A list of matching CaseMaster objects.

        Future SQL behaviour:
            Will execute SELECT ... WHERE crime_major_head_id = ?
        """

        return [
            case for case in cls._cases
            if case.crime_major_head_id == crime_major_head_id
        ]

    # ----------------------------------------------------------
    # Count
    # ----------------------------------------------------------

    @classmethod
    def count(cls) -> int:
        """
        Return the total number of cases in the store.

        Returns:
            Integer count of all stored cases.

        Future SQL behaviour:
            Will execute SELECT COUNT(*) FROM case_master.
        """

        return len(cls._cases)
