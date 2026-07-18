from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.permissions import require_roles
from app.core.logging import complainant_logger
from app.core.roles import UserRole
from app.models.user import User
from app.common.enums import SortOrder, Gender
from app.common.queries.complainant_query import ComplainantQueryOptions
from app.schemas.complainant import (
    ComplainantCreate,
    ComplainantListResponse,
    ComplainantResponse,
    ComplainantSortField,
    ComplainantUpdate,
)
from app.services.complainant_service import ComplainantService

router = APIRouter()


# ==============================================================
# POST /cases/{case_id}/complainants — Register Complainant
# ==============================================================

@router.post(
    "/cases/{case_id}/complainants",
    response_model=ComplainantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a New Complainant for a Case",
    description=(
        "Register a new complainant linked to the specified case ID. "
        "Requires ADMIN, SUPERVISOR, or INVESTIGATOR role. "
        "Performs format validation for mobile numbers and email, "
        "checks for duplicates, and ensures the referenced CaseMaster exists."
    ),
    responses={
        201: {"description": "Complainant registered successfully."},
        404: {"description": "Case not found."},
        409: {"description": "Duplicate complainant name/phone in case."},
        422: {"description": "Invalid format or request body."},
    },
)
async def create_complainant(
    case_id: str,
    data: ComplainantCreate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
        )
    ),
    service: ComplainantService = Depends(),
) -> ComplainantResponse:
    """Register a new complainant."""
    complainant_logger.info(
        "Create complainant request | User=%s | CaseID=%s | Name=%s",
        current_user.employee_id,
        case_id,
        data.name,
    )
    return service.create_complainant(case_id, data)


# ==============================================================
# GET /cases/{case_id}/complainants — List Case Complainants
# ==============================================================

@router.get(
    "/cases/{case_id}/complainants",
    response_model=ComplainantListResponse,
    summary="List Complainants for a Case",
    description=(
        "Retrieve a paginated list of complainant summaries linked to a case. "
        "Supports query parameters for filtering, sorting, and pagination. "
        "Requires ADMIN, SUPERVISOR, INVESTIGATOR, or ANALYST role."
    ),
    responses={
        200: {"description": "List of case complainants retrieved successfully."},
    },
)
async def list_case_complainants(
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
    sort_by: ComplainantSortField = Query(
        default=ComplainantSortField.CREATED_DATE,
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
    service: ComplainantService = Depends(),
) -> ComplainantListResponse:
    """List complainants for a case."""
    # Compose flat query parameters into structured ComplainantQueryOptions
    options = ComplainantQueryOptions(
        case_master_id=case_id,
        name=name,
        mobile_no=mobile_no,
        email=email,
        gender=gender,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return service.search_complainants(options)


# ==============================================================
# GET /complainants/{complainant_id} — Retrieve Complainant Details
# ==============================================================

@router.get(
    "/complainants/{complainant_id}",
    response_model=ComplainantResponse,
    summary="Get Complainant Details",
    description=(
        "Retrieve the full detail view of a complainant record. "
        "Requires ADMIN, SUPERVISOR, INVESTIGATOR, or ANALYST role."
    ),
    responses={
        200: {"description": "Complainant details retrieved successfully."},
        404: {"description": "Complainant not found."},
    },
)
async def get_complainant(
    complainant_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: ComplainantService = Depends(),
) -> ComplainantResponse:
    """Get complainant by ID."""
    return service.get_complainant(complainant_id)


# ==============================================================
# PUT /complainants/{complainant_id} — Update Complainant
# ==============================================================

@router.put(
    "/complainants/{complainant_id}",
    response_model=ComplainantResponse,
    summary="Update Complainant",
    description=(
        "Update details of an existing complainant. "
        "Allows full and partial payload edits. "
        "Requires ADMIN, SUPERVISOR, or INVESTIGATOR role."
    ),
    responses={
        200: {"description": "Complainant updated successfully."},
        404: {"description": "Complainant not found."},
        409: {"description": "Duplicate complainant check failed."},
        422: {"description": "Invalid format or request body."},
    },
)
async def update_complainant(
    complainant_id: str,
    data: ComplainantUpdate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
        )
    ),
    service: ComplainantService = Depends(),
) -> ComplainantResponse:
    """Update complainant by ID."""
    complainant_logger.info(
        "Update complainant request | User=%s | ID=%s",
        current_user.employee_id,
        complainant_id,
    )
    return service.update_complainant(complainant_id, data)


# ==============================================================
# DELETE /complainants/{complainant_id} — Delete Complainant
# ==============================================================

@router.delete(
    "/complainants/{complainant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Complainant",
    description=(
        "Remove a complainant record from the system. "
        "Requires ADMIN or SUPERVISOR role."
    ),
    responses={
        204: {"description": "Complainant deleted successfully."},
        404: {"description": "Complainant not found."},
    },
)
async def delete_complainant(
    complainant_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
        )
    ),
    service: ComplainantService = Depends(),
) -> None:
    """Delete complainant by ID."""
    complainant_logger.info(
        "Delete complainant request | User=%s | ID=%s",
        current_user.employee_id,
        complainant_id,
    )
    service.delete_complainant(complainant_id)
