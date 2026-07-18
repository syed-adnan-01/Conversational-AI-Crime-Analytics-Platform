from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.auth.permissions import require_roles
from app.core.logging import case_logger
from app.core.roles import UserRole
from app.models.user import User
from app.schemas.case import (
    CaseCreate,
    CaseListResponse,
    CaseResponse,
    CaseUpdate,
    SortField,
    SortOrder,
)
from app.services.case_service import CaseService

router = APIRouter()


# ==============================================================
# POST /cases — Register a New Case
# ==============================================================

@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a New Case",
    description=(
        "Register a new FIR / case in the system. "
        "Requires ADMIN, SUPERVISOR, or INVESTIGATOR role. "
        "The system generates the case_master_id, created_at, "
        "and updated_at fields automatically."
    ),
    responses={
        201: {"description": "Case registered successfully."},
        409: {"description": "Duplicate crime number."},
        422: {"description": "Invalid date range or request body."},
    },
)
async def create_case(
    data: CaseCreate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
        )
    ),
) -> CaseResponse:
    """Register a new FIR / case."""

    case_logger.info(
        "Create case request | User=%s | CrimeNo=%s",
        current_user.employee_id,
        data.crime_no,
    )

    created = CaseService.create_case(data)

    return CaseResponse.model_validate(created)


# ==============================================================
# GET /cases/search — Search Cases with Filters
# ==============================================================
# NOTE: This route is defined BEFORE /cases/{case_master_id}
# to prevent FastAPI from matching "search" as a path parameter.
# ==============================================================

@router.get(
    "/search",
    response_model=CaseListResponse,
    summary="Search Cases",
    description=(
        "Search and filter cases with pagination. "
        "All filter parameters are optional. "
        "Requires ADMIN, SUPERVISOR, INVESTIGATOR, or ANALYST role."
    ),
    responses={
        200: {"description": "Paginated list of matching cases."},
    },
)
async def search_cases(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    # Identifiers
    case_no: Optional[str] = Query(
        default=None,
        max_length=50,
        description="Filter by court-assigned case number (exact).",
    ),
    case_number: Optional[str] = Query(
        default=None,
        max_length=50,
        description="Filter by court-assigned case number (alias).",
    ),
    crime_no: Optional[str] = Query(
        default=None,
        max_length=50,
        description="Filter by crime number (exact).",
    ),
    crime_number: Optional[str] = Query(
        default=None,
        max_length=50,
        description="Filter by crime number (alias).",
    ),
    # Date Ranges
    date_from: Optional[datetime] = Query(
        default=None,
        description="Filter cases registered on or after this date (exact).",
    ),
    registered_from_date: Optional[datetime] = Query(
        default=None,
        description="Filter cases registered on or after this date (alias).",
    ),
    date_to: Optional[datetime] = Query(
        default=None,
        description="Filter cases registered on or before this date (exact).",
    ),
    registered_to_date: Optional[datetime] = Query(
        default=None,
        description="Filter cases registered on or before this date (alias).",
    ),
    incident_from_date: Optional[datetime] = Query(
        default=None,
        description="Filter cases with incident starting on or after this date.",
    ),
    incident_to_date: Optional[datetime] = Query(
        default=None,
        description="Filter cases with incident ending on or before this date.",
    ),
    # Classifications
    case_status_id: Optional[int] = Query(
        default=None,
        description="Filter by case lifecycle status ID (exact).",
    ),
    case_status: Optional[int] = Query(
        default=None,
        description="Filter by case lifecycle status ID (alias).",
    ),
    case_category_id: Optional[int] = Query(
        default=None,
        description="Filter by case category ID (exact).",
    ),
    crime_category: Optional[int] = Query(
        default=None,
        description="Filter by case category ID (alias).",
    ),
    gravity_offence_id: Optional[int] = Query(
        default=None,
        description="Filter by gravity of offence ID (exact).",
    ),
    gravity_offence: Optional[int] = Query(
        default=None,
        description="Filter by gravity of offence ID (alias).",
    ),
    crime_major_head_id: Optional[int] = Query(
        default=None,
        description="Filter by major crime head ID (exact).",
    ),
    crime_major_head: Optional[int] = Query(
        default=None,
        description="Filter by major crime head ID (alias).",
    ),
    crime_minor_head_id: Optional[int] = Query(
        default=None,
        description="Filter by minor crime head ID (exact).",
    ),
    crime_minor_head: Optional[int] = Query(
        default=None,
        description="Filter by minor crime head ID (alias).",
    ),
    # Organization
    police_station_id: Optional[int] = Query(
        default=None,
        description="Filter by police station ID (exact).",
    ),
    police_station: Optional[int] = Query(
        default=None,
        description="Filter by police station ID (alias).",
    ),
    police_person_id: Optional[int] = Query(
        default=None,
        description="Filter by investigating officer ID (exact).",
    ),
    police_person: Optional[int] = Query(
        default=None,
        description="Filter by investigating officer ID (alias).",
    ),
    court_id: Optional[int] = Query(
        default=None,
        description="Filter by court ID (exact).",
    ),
    court: Optional[int] = Query(
        default=None,
        description="Filter by court ID (alias).",
    ),
    district: Optional[str] = Query(
        default=None,
        max_length=100,
        description="Filter by district name.",
    ),
    state: Optional[str] = Query(
        default=None,
        max_length=100,
        description="Filter by state name.",
    ),
    # Keyword Search
    brief_facts: Optional[str] = Query(
        default=None,
        description="Case-insensitive keyword search on brief_facts, case_number, or crime_number.",
    ),
    # Sorting
    sort_by: SortField = Query(
        default=SortField.REGISTERED_DATE,
        description="Field to sort results by.",
    ),
    sort_order: SortOrder = Query(
        default=SortOrder.DESC,
        description="Direction of sorting (asc or desc).",
    ),
    # Pagination
    page: int = Query(
        default=1,
        ge=1,
        description="Page number (1-indexed).",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of records per page (max 100).",
    ),
) -> CaseListResponse:
    """Search and filter cases with pagination."""

    return CaseService.search_cases(
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
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )


# ==============================================================
# GET /cases — List All Cases (Paginated)
# ==============================================================

@router.get(
    "/",
    response_model=CaseListResponse,
    summary="List All Cases",
    description=(
        "Retrieve a paginated list of all cases. "
        "Requires ADMIN, SUPERVISOR, INVESTIGATOR, or ANALYST role."
    ),
    responses={
        200: {"description": "Paginated list of cases."},
    },
)
async def list_cases(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number (1-indexed).",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of records per page (max 100).",
    ),
) -> CaseListResponse:
    """Retrieve a paginated list of all cases."""

    return CaseService.search_cases(
        page=page,
        page_size=page_size,
    )


# ==============================================================
# GET /cases/{case_master_id} — Get Single Case
# ==============================================================

@router.get(
    "/{case_master_id}",
    response_model=CaseResponse,
    summary="Get Case by ID",
    description=(
        "Retrieve a single case by its system-generated ID. "
        "Requires ADMIN, SUPERVISOR, INVESTIGATOR, or ANALYST role."
    ),
    responses={
        200: {"description": "Case details returned successfully."},
        404: {"description": "Case not found."},
    },
)
async def get_case(
    case_master_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
) -> CaseResponse:
    """Retrieve a single case by ID."""

    case = CaseService.get_case(case_master_id)

    return CaseResponse.model_validate(case)


# ==============================================================
# PUT /cases/{case_master_id} — Update Case
# ==============================================================

@router.put(
    "/{case_master_id}",
    response_model=CaseResponse,
    summary="Update Case",
    description=(
        "Update an existing case. Only provided fields are modified. "
        "Immutable fields (crime_no, case_no, police_station_id, "
        "crime_registered_date) cannot be changed. "
        "Requires ADMIN, SUPERVISOR, or INVESTIGATOR role."
    ),
    responses={
        200: {"description": "Case updated successfully."},
        404: {"description": "Case not found."},
        422: {"description": "Invalid date range or request body."},
    },
)
async def update_case(
    case_master_id: str,
    data: CaseUpdate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
        )
    ),
) -> CaseResponse:
    """Update an existing case."""

    case_logger.info(
        "Update case request | User=%s | ID=%s",
        current_user.employee_id,
        case_master_id,
    )

    updated = CaseService.update_case(case_master_id, data)

    return CaseResponse.model_validate(updated)


# ==============================================================
# DELETE /cases/{case_master_id} — Delete Case
# ==============================================================

@router.delete(
    "/{case_master_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Case",
    description=(
        "Delete a case from the system. "
        "This action is restricted to ADMIN and SUPERVISOR roles."
    ),
    responses={
        204: {"description": "Case deleted successfully."},
        404: {"description": "Case not found."},
    },
)
async def delete_case(
    case_master_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
        )
    ),
) -> None:
    """Delete a case."""

    case_logger.info(
        "Delete case request | User=%s | ID=%s",
        current_user.employee_id,
        case_master_id,
    )

    CaseService.delete_case(case_master_id)
