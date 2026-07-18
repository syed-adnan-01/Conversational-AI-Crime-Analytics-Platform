from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.permissions import require_roles
from app.core.logging import app_logger
from app.core.roles import UserRole
from app.models.user import User
from app.common.enums import SortOrder, Gender, IdentificationType
from app.common.queries.accused_query import AccusedQueryOptions
from app.schemas.accused import (
    AccusedCreate,
    AccusedListResponse,
    AccusedResponse,
    AccusedSortField,
    AccusedUpdate,
)
from app.services.accused_service import AccusedService

router = APIRouter()


# ==============================================================
# POST /cases/{case_id}/accused — Register Accused
# ==============================================================

@router.post(
    "/cases/{case_id}/accused",
    response_model=AccusedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a New Accused for a Case",
    description=(
        "Register a new accused linked to the specified case ID. "
        "Requires ADMIN, SUPERVISOR, or INVESTIGATOR role. "
        "Performs format validation for mobile numbers and email, "
        "checks for duplicates, and ensures the referenced CaseMaster exists."
    ),
    responses={
        201: {"description": "Accused registered successfully."},
        404: {"description": "Case not found."},
        409: {"description": "Duplicate accused name/phone in case."},
        422: {"description": "Invalid format or request body."},
    },
)
async def create_accused(
    case_id: str,
    data: AccusedCreate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
        )
    ),
    service: AccusedService = Depends(),
) -> AccusedResponse:
    """Register a new accused."""
    app_logger.info(
        "Create accused request | User=%s | CaseID=%s | Name=%s",
        current_user.employee_id,
        case_id,
        data.name,
    )
    return service.create_accused(case_id, data)


# ==============================================================
# GET /cases/{case_id}/accused — List Case Accused
# ==============================================================

@router.get(
    "/cases/{case_id}/accused",
    response_model=AccusedListResponse,
    summary="List Accused for a Case",
    description=(
        "Retrieve a paginated list of accused summaries linked to a case. "
        "Supports query parameters for filtering, sorting, and pagination. "
        "Requires ADMIN, SUPERVISOR, INVESTIGATOR, or ANALYST role."
    ),
    responses={
        200: {"description": "List of case accused retrieved successfully."},
    },
)
async def list_case_accused(
    case_id: str,
    name: Optional[str] = Query(
        default=None,
        description="Filter by name (case-insensitive keyword matching).",
    ),
    mobile_no: Optional[str] = Query(
        default=None,
        description="Filter by exact mobile number.",
    ),
    email: Optional[str] = Query(
        default=None,
        description="Filter by exact email address.",
    ),
    gender: Optional[Gender] = Query(
        default=None,
        description="Filter by exact gender enum.",
    ),
    age: Optional[int] = Query(
        default=None,
        description="Filter by exact age.",
    ),
    nationality: Optional[str] = Query(
        default=None,
        description="Filter by exact nationality.",
    ),
    occupation: Optional[str] = Query(
        default=None,
        description="Filter by exact occupation.",
    ),
    id_type: Optional[IdentificationType] = Query(
        default=None,
        description="Filter by exact identification type enum.",
    ),
    id_number: Optional[str] = Query(
        default=None,
        description="Filter by exact identification number.",
    ),
    sort_by: AccusedSortField = Query(
        default=AccusedSortField.CREATED_DATE,
        description="Field to sort the result list by.",
    ),
    sort_order: SortOrder = Query(
        default=SortOrder.DESC,
        description="Sorting sequence order: ascending or descending.",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page offset index (1-indexed).",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum records returned per page.",
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: AccusedService = Depends(),
) -> AccusedListResponse:
    """List accused for a case."""
    # Compose flat query parameters into structured AccusedQueryOptions
    options = AccusedQueryOptions(
        case_master_id=case_id,
        name=name,
        mobile_no=mobile_no,
        email=email,
        gender=gender,
        age=age,
        nationality=nationality,
        occupation=occupation,
        id_type=id_type,
        id_number=id_number,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return service.search_accused(options)


# ==============================================================
# GET /accused/{accused_id} — Retrieve Accused Details
# ==============================================================

@router.get(
    "/accused/{accused_id}",
    response_model=AccusedResponse,
    summary="Get Accused Details",
    description=(
        "Retrieve the full detail view of an accused record. "
        "Requires ADMIN, SUPERVISOR, INVESTIGATOR, or ANALYST role."
    ),
    responses={
        200: {"description": "Accused details retrieved successfully."},
        404: {"description": "Accused not found."},
    },
)
async def get_accused(
    accused_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: AccusedService = Depends(),
) -> AccusedResponse:
    """Get accused by ID."""
    return service.get_accused(accused_id)


# ==============================================================
# PUT /accused/{accused_id} — Update Accused
# ==============================================================

@router.put(
    "/accused/{accused_id}",
    response_model=AccusedResponse,
    summary="Update Accused",
    description=(
        "Update details of an existing accused. "
        "Allows full and partial payload edits. "
        "Requires ADMIN, SUPERVISOR, or INVESTIGATOR role."
    ),
    responses={
        200: {"description": "Accused updated successfully."},
        404: {"description": "Accused not found."},
        409: {"description": "Duplicate accused check failed."},
        422: {"description": "Invalid format or request body."},
    },
)
async def update_accused(
    accused_id: str,
    data: AccusedUpdate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
        )
    ),
    service: AccusedService = Depends(),
) -> AccusedResponse:
    """Update accused by ID."""
    app_logger.info(
        "Update accused request | User=%s | ID=%s",
        current_user.employee_id,
        accused_id,
    )
    return service.update_accused(accused_id, data)


# ==============================================================
# DELETE /accused/{accused_id} — Delete Accused
# ==============================================================

@router.delete(
    "/accused/{accused_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Accused",
    description=(
        "Remove an accused record from the system. "
        "Requires ADMIN or SUPERVISOR role."
    ),
    responses={
        204: {"description": "Accused deleted successfully."},
        404: {"description": "Accused not found."},
    },
)
async def delete_accused(
    accused_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
        )
    ),
    service: AccusedService = Depends(),
) -> None:
    """Delete accused by ID."""
    app_logger.info(
        "Delete accused request | User=%s | ID=%s",
        current_user.employee_id,
        accused_id,
    )
    service.delete_accused(accused_id)
