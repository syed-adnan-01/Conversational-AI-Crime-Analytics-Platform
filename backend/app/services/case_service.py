from datetime import datetime
from typing import Optional

from app.common.exceptions import (
    CaseNotFoundException,
    DuplicateCaseNumberException,
    DuplicateCrimeNumberException,
    InvalidDateRangeException,
)
from app.core.exceptions import CrimeSphereException
from app.core.logging import case_logger
from app.models.case_master import CaseMaster
from app.repository.case_repository import CaseRepository
from app.common.queries.case_query import CaseQueryOptions
from app.schemas.case import (
    CaseCreate,
    CaseListResponse,
    CaseSearchFilters,
    CaseSummary,
    CaseUpdate,
    PaginationMeta,
    SortField,
    SortOrder,
    CaseFilterParams,
    CaseSortParams,
    CasePaginationParams,
)


class CaseService:
    """
    Service responsible for case management business logic.

    Orchestrates validation, data transformation, and repository
    calls. Mirrors the AuthService pattern using @staticmethod.

    Responsibilities:
        • Business validation (dates, duplicates, existence)
        • Schema ↔ Domain model mapping
        • ID and timestamp generation
        • Logging business events
        • Coordinating repository operations

    Does NOT handle:
        • HTTP requests/responses
        • Authentication/authorization
        • Direct data storage
    """

    # ==============================================================
    # CASE NUMBER GENERATION
    # ==============================================================
    # These are placeholder generators. The final Karnataka
    # numbering algorithm will replace the logic inside these
    # methods without changing their signatures or call sites.
    # ==============================================================

    _case_counter: int = 0
    _crime_counter: int = 0

    @staticmethod
    def _generate_case_number() -> str:
        """
        Generate a placeholder case number.

        Format: CS-{YEAR}{SEQUENCE}
        Example: CS-202600001

        Future:
            Will be replaced by jurisdiction-specific
            numbering (e.g., Karnataka FIR format).
        """

        CaseService._case_counter += 1
        year = datetime.now().year

        return f"CS-{year}{CaseService._case_counter:05d}"

    @staticmethod
    def _generate_crime_number() -> str:
        """
        Generate a placeholder crime number.

        Format: CR-{YEAR}{SEQUENCE}
        Example: CR-202600001

        Future:
            Will be replaced by station-specific
            numbering conventions.
        """

        CaseService._crime_counter += 1
        year = datetime.now().year

        return f"CR-{year}{CaseService._crime_counter:05d}"

    # ==============================================================
    # PRIVATE VALIDATORS
    # ==============================================================

    @staticmethod
    def _validate_dates(
        incident_from_date: Optional[datetime],
        incident_to_date: Optional[datetime],
        crime_registered_date: Optional[datetime],
        info_received_ps_date: Optional[datetime],
    ) -> None:
        """
        Validate logical consistency of date fields.

        Rules:
            1. incident_from_date must not be after incident_to_date.
            2. incident dates must not be in the future.
            3. crime_registered_date must not precede incident_from_date.
            4. info_received_ps_date must not precede incident_from_date.

        Raises:
            InvalidDateRangeException if any rule is violated.
        """

        now = datetime.now()

        # Rule 1: Incident window must be logically ordered
        if (
            incident_from_date is not None
            and incident_to_date is not None
            and incident_from_date > incident_to_date
        ):
            raise InvalidDateRangeException(
                "incident_from_date cannot be after incident_to_date."
            )

        # Rule 2: Incident dates must not be in the future
        if incident_from_date is not None and incident_from_date > now:
            raise InvalidDateRangeException(
                "incident_from_date cannot be in the future."
            )

        if incident_to_date is not None and incident_to_date > now:
            raise InvalidDateRangeException(
                "incident_to_date cannot be in the future."
            )

        # Rule 3: Registration cannot precede incident
        if (
            crime_registered_date is not None
            and incident_from_date is not None
            and crime_registered_date < incident_from_date
        ):
            raise InvalidDateRangeException(
                "crime_registered_date cannot be before incident_from_date."
            )

        # Rule 4: Info received cannot precede incident
        if (
            info_received_ps_date is not None
            and incident_from_date is not None
            and info_received_ps_date < incident_from_date
        ):
            raise InvalidDateRangeException(
                "info_received_ps_date cannot be before incident_from_date."
            )

    @staticmethod
    def _validate_no_duplicate_crime_number(crime_no: str) -> None:
        """
        Ensure the crime number does not already exist.

        Raises:
            DuplicateCrimeNumberException if a duplicate is found.
        """

        existing = CaseRepository.get_case_by_crime_number(crime_no)

        if existing is not None:
            case_logger.warning(
                "Duplicate crime number rejected | CrimeNo=%s",
                crime_no,
            )
            raise DuplicateCrimeNumberException(crime_no)

    @staticmethod
    def _validate_no_duplicate_case_number(case_no: str) -> None:
        """
        Ensure the case number does not already exist.

        Raises:
            DuplicateCaseNumberException if a duplicate is found.
        """

        existing = CaseRepository.get_case_by_case_number(case_no)

        if existing is not None:
            case_logger.warning(
                "Duplicate case number rejected | CaseNo=%s",
                case_no,
            )
            raise DuplicateCaseNumberException(case_no)

    @staticmethod
    def _validate_case_exists(case_master_id: str) -> CaseMaster:
        """
        Verify a case exists and return it.

        Args:
            case_master_id: The unique case identifier.

        Returns:
            The existing CaseMaster domain object.

        Raises:
            CaseNotFoundException if no case matches the ID.
        """

        case = CaseRepository.get_case_by_id(case_master_id)

        if case is None:
            raise CaseNotFoundException(case_master_id)

        return case

    # ==============================================================
    # PRIVATE HELPERS
    # ==============================================================

    @staticmethod
    def _prepare_case(data: CaseCreate) -> CaseMaster:
        """
        Transform a CaseCreate schema into a CaseMaster domain model.

        Maps the API contract (schema) to the internal business
        entity (domain model). System-generated fields like
        case_master_id, created_at, and updated_at are left as
        None — the repository assigns them during storage.
        """

        return CaseMaster(
            crime_no=data.crime_no,
            case_no=None,
            crime_registered_date=data.crime_registered_date,
            police_person_id=data.police_person_id,
            police_station_id=data.police_station_id,
            case_category_id=data.case_category_id,
            gravity_offence_id=data.gravity_offence_id,
            crime_major_head_id=data.crime_major_head_id,
            crime_minor_head_id=data.crime_minor_head_id,
            case_status_id=data.case_status_id,
            court_id=data.court_id,
            incident_from_date=data.incident_from_date,
            incident_to_date=data.incident_to_date,
            info_received_ps_date=data.info_received_ps_date,
            latitude=data.latitude,
            longitude=data.longitude,
            brief_facts=data.brief_facts,
        )

    @staticmethod
    def _apply_update(
        existing: CaseMaster,
        updates: CaseUpdate,
    ) -> CaseMaster:
        """
        Merge non-None update fields into the existing case.

        Only fields present in CaseUpdate are considered.
        Immutable fields (crime_no, case_no, police_station_id,
        crime_registered_date, created_at) are preserved from
        the existing record.

        Returns:
            A new CaseMaster with the merged state.
        """

        update_data = updates.model_dump(exclude_unset=True)

        merged = existing.model_copy(update=update_data)

        return merged

    # ==============================================================
    # PUBLIC METHODS
    # ==============================================================

    @staticmethod
    def create_case(data: CaseCreate) -> CaseMaster:
        """
        Register a new case in the system.

        Workflow:
            1. Validate duplicate crime number.
            2. Validate date consistency.
            3. Transform schema → domain model.
            4. Store via repository.
            5. Log and return the created case.

        Args:
            data: CaseCreate schema from the API layer.

        Returns:
            The created CaseMaster with system-generated fields.

        Raises:
            DuplicateCrimeNumberException: If crime_no already exists.
            InvalidDateRangeException: If dates are logically invalid.
        """

        # Business validation
        CaseService._validate_no_duplicate_crime_number(data.crime_no)

        CaseService._validate_dates(
            incident_from_date=data.incident_from_date,
            incident_to_date=data.incident_to_date,
            crime_registered_date=data.crime_registered_date,
            info_received_ps_date=data.info_received_ps_date,
        )

        # Transform schema to domain model
        case = CaseService._prepare_case(data)

        # Persist via repository
        created = CaseRepository.create_case(case)

        # Trigger Timeline Event
        try:
            from app.models.timeline import TimelineEventType
            from app.services.timeline_service import TimelineService
            timeline_svc = TimelineService()
            timeline_svc.record_event(
                case_master_id=created.case_master_id,
                event_type=TimelineEventType.CASE_CREATED,
                title=f"Case Registered: FIR {created.crime_no}",
                description=f"Case '{created.crime_no}' was registered in the system.",
                reference_id=created.case_master_id,
                reference_type="CaseMaster",
            )
        except Exception as e:
            case_logger.warning("Timeline event generation failed: %s", str(e))

        case_logger.info(
            "Case created | ID=%s | CrimeNo=%s",
            created.case_master_id,
            created.crime_no,
        )

        return created

    @staticmethod
    def get_case(case_master_id: str) -> CaseMaster:
        """
        Retrieve a single case by its ID.

        Args:
            case_master_id: The unique case identifier.

        Returns:
            The matching CaseMaster domain object.

        Raises:
            CaseNotFoundException: If no case matches the ID.
        """

        case = CaseService._validate_case_exists(case_master_id)

        case_logger.info(
            "Case retrieved | ID=%s",
            case_master_id,
        )

        return case

    @staticmethod
    def get_all_cases() -> list[CaseMaster]:
        """
        Retrieve all cases from the repository.

        Returns:
            A list of all CaseMaster domain objects.
        """

        return CaseRepository.get_all_cases()

    @staticmethod
    def update_case(
        case_master_id: str,
        data: CaseUpdate,
    ) -> CaseMaster:
        """
        Update an existing case with the provided data.

        Workflow:
            1. Verify the case exists.
            2. Validate date consistency (if dates are being updated).
            3. Merge non-None fields into existing record.
            4. Persist via repository.
            5. Log and return the updated case.

        Args:
            case_master_id: The unique case identifier.
            data: CaseUpdate schema with fields to modify.

        Returns:
            The updated CaseMaster domain object.

        Raises:
            CaseNotFoundException: If no case matches the ID.
            InvalidDateRangeException: If dates are logically invalid.
        """

        # Verify existence
        existing = CaseService._validate_case_exists(case_master_id)

        # Merge update fields
        merged = CaseService._apply_update(existing, data)

        # Validate dates on the merged result
        CaseService._validate_dates(
            incident_from_date=merged.incident_from_date,
            incident_to_date=merged.incident_to_date,
            crime_registered_date=merged.crime_registered_date,
            info_received_ps_date=merged.info_received_ps_date,
        )

        # Persist
        updated = CaseRepository.update_case(merged)

        case_logger.info(
            "Case updated | ID=%s",
            case_master_id,
        )

        return updated

    @staticmethod
    def delete_case(case_master_id: str) -> bool:
        """
        Delete a case from the system.

        Args:
            case_master_id: The unique case identifier.

        Returns:
            True if the case was successfully deleted.

        Raises:
            CaseNotFoundException: If no case matches the ID.
        """

        CaseService._validate_case_exists(case_master_id)

        result = CaseRepository.delete_case(case_master_id)

        case_logger.info(
            "Case deleted | ID=%s",
            case_master_id,
        )

        return result

    @staticmethod
    def search_cases(
        case_no: Optional[str] = None,
        case_number: Optional[str] = None,
        crime_no: Optional[str] = None,
        crime_number: Optional[str] = None,
        date_from: Optional[datetime] = None,
        registered_from_date: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        registered_to_date: Optional[datetime] = None,
        incident_from_date: Optional[datetime] = None,
        incident_to_date: Optional[datetime] = None,
        case_status_id: Optional[int] = None,
        case_status: Optional[int] = None,
        case_category_id: Optional[int] = None,
        crime_category: Optional[int] = None,
        gravity_offence_id: Optional[int] = None,
        gravity_offence: Optional[int] = None,
        crime_major_head_id: Optional[int] = None,
        crime_major_head: Optional[int] = None,
        crime_minor_head_id: Optional[int] = None,
        crime_minor_head: Optional[int] = None,
        police_station_id: Optional[int] = None,
        police_station: Optional[int] = None,
        police_person_id: Optional[int] = None,
        police_person: Optional[int] = None,
        court_id: Optional[int] = None,
        court: Optional[int] = None,
        district: Optional[str] = None,
        state: Optional[str] = None,
        brief_facts: Optional[str] = None,
        sort_by: SortField = SortField.REGISTERED_DATE,
        sort_order: SortOrder = SortOrder.DESC,
        page: int = 1,
        page_size: int = 20,
    ) -> CaseListResponse:
        """
        Search and filter cases with pagination and sorting.

        Validates pagination bounds, sort parameters, and date ranges.
        Normalizes semantic filters and delegates query execution
        to the repository layer.
        """
        filters = CaseSearchFilters(
            filters=CaseFilterParams(
                case_no=case_no,
                case_number=case_number,
                crime_no=crime_no,
                crime_number=crime_number,
                date_from=date_from,
                registered_from_date=registered_from_date,
                date_to=date_to,
                registered_to_date=registered_to_date,
                incident_from_date=incident_from_date,
                incident_to_date=incident_to_date,
                case_status_id=case_status_id,
                case_status=case_status,
                case_category_id=case_category_id,
                crime_category=crime_category,
                gravity_offence_id=gravity_offence_id,
                gravity_offence=gravity_offence,
                crime_major_head_id=crime_major_head_id,
                crime_major_head=crime_major_head,
                crime_minor_head_id=crime_minor_head_id,
                crime_minor_head=crime_minor_head,
                police_station_id=police_station_id,
                police_station=police_station,
                police_person_id=police_person_id,
                police_person=police_person,
                court_id=court_id,
                court=court,
                district=district,
                state=state,
                brief_facts=brief_facts,
            ),
            sort=CaseSortParams(
                sort_by=sort_by,
                sort_order=sort_order,
            ),
            pagination=CasePaginationParams(
                page=page,
                page_size=page_size,
            ),
        )

        page = filters.pagination.page
        page_size = filters.pagination.page_size

        # Validate pagination
        if page < 1:
            raise CrimeSphereException("Page number must be >= 1", 422)
        if page_size < 1 or page_size > 100:
            raise CrimeSphereException("Page size must be between 1 and 100", 422)

        # Resolve date filters
        date_from = filters.filters.date_from or filters.filters.registered_from_date
        date_to = filters.filters.date_to or filters.filters.registered_to_date
        incident_from = filters.filters.incident_from_date
        incident_to = filters.filters.incident_to_date

        # Validate date consistency
        if date_from and date_to and date_from > date_to:
            raise InvalidDateRangeException("Registered 'from' date cannot be after 'to' date")
        if incident_from and incident_to and incident_from > incident_to:
            raise InvalidDateRangeException("Incident 'from' date cannot be after 'to' date")

        # Resolve and map semantic parameter aliases
        case_no = filters.filters.case_no or filters.filters.case_number
        crime_no = filters.filters.crime_no or filters.filters.crime_number

        case_status_id = (
            filters.filters.case_status_id
            if filters.filters.case_status_id is not None
            else filters.filters.case_status
        )
        case_category_id = (
            filters.filters.case_category_id
            if filters.filters.case_category_id is not None
            else filters.filters.crime_category
        )
        gravity_offence_id = (
            filters.filters.gravity_offence_id
            if filters.filters.gravity_offence_id is not None
            else filters.filters.gravity_offence
        )
        crime_major_head_id = (
            filters.filters.crime_major_head_id
            if filters.filters.crime_major_head_id is not None
            else filters.filters.crime_major_head
        )
        crime_minor_head_id = (
            filters.filters.crime_minor_head_id
            if filters.filters.crime_minor_head_id is not None
            else filters.filters.crime_minor_head
        )

        police_station_id = (
            filters.filters.police_station_id
            if filters.filters.police_station_id is not None
            else filters.filters.police_station
        )
        police_person_id = (
            filters.filters.police_person_id
            if filters.filters.police_person_id is not None
            else filters.filters.police_person
        )
        court_id = (
            filters.filters.court_id
            if filters.filters.court_id is not None
            else filters.filters.court
        )

        # Construct typed query options
        options = CaseQueryOptions(
            case_no=case_no,
            crime_no=crime_no,
            date_from=date_from,
            date_to=date_to,
            incident_from_date=incident_from,
            incident_to_date=incident_to,
            case_status_id=case_status_id,
            case_category_id=case_category_id,
            gravity_offence_id=gravity_offence_id,
            crime_major_head_id=crime_major_head_id,
            crime_minor_head_id=crime_minor_head_id,
            police_station_id=police_station_id,
            police_person_id=police_person_id,
            court_id=court_id,
            district=filters.filters.district,
            state=filters.filters.state,
            brief_facts=filters.filters.brief_facts,
            sort_by=filters.sort.sort_by,
            sort_order=filters.sort.sort_order,
            page=page,
            page_size=page_size,
        )

        # Call repository layer
        page_items, total = CaseRepository.query_cases(options)

        # Map to summary responses
        summaries = [
            CaseSummary(
                case_master_id=c.case_master_id,
                crime_no=c.crime_no,
                case_no=c.case_no,
                case_status_id=c.case_status_id,
                crime_registered_date=c.crime_registered_date,
                police_station_id=c.police_station_id,
                crime_major_head_id=c.crime_major_head_id,
                police_person_id=c.police_person_id,
            )
            for c in page_items
        ]

        # Calculate pagination metadata
        pagination = PaginationMeta.calculate(
            total=total,
            page=page,
            page_size=page_size,
        )

        return CaseListResponse(
            items=summaries,
            pagination=pagination,
        )
