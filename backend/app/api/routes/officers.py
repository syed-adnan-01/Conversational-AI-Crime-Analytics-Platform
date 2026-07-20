from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_roles
from app.core.roles import UserRole
from app.models.user import User
from app.models.officer import OfficerRole
from app.common.enums import SortOrder
from app.common.queries.officer_query import OfficerAssignmentQueryOptions
from app.schemas.officer import (
    OfficerMasterCreate,
    OfficerMasterResponse,
    OfficerAssignmentCreate,
    OfficerAssignmentUpdate,
    OfficerAssignmentResponse,
    OfficerAssignmentListResponse,
    OfficerSortField,
)
from app.services.officer_service import OfficerService

router = APIRouter()


# ----------------------------------------------------------
# Officer Master Routes
# ----------------------------------------------------------

@router.post(
    "/officers",
    response_model=OfficerMasterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new officer in Master Database",
)
def create_officer(
    payload: OfficerMasterCreate,
    officer_service: OfficerService = Depends(OfficerService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Create an officer master profile.
    Requires Investigator, Supervisor, or Admin role.
    """
    return officer_service.create_officer(payload)


@router.get(
    "/officers",
    response_model=List[OfficerMasterResponse],
    status_code=status.HTTP_200_OK,
    summary="List all registered officer profiles",
)
def list_officers(
    officer_service: OfficerService = Depends(OfficerService),
    current_user: User = Depends(get_current_user),
):
    """
    List officer profiles.
    Requires authentication.
    """
    return officer_service.list_officers()


@router.get(
    "/officers/{id}",
    response_model=OfficerMasterResponse,
    status_code=status.HTTP_200_OK,
    summary="Get officer master profile by ID",
)
def get_officer(
    id: str,
    officer_service: OfficerService = Depends(OfficerService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve officer master profile by ID.
    Requires authentication.
    """
    return officer_service.get_officer(id)


# ----------------------------------------------------------
# Officer Assignment Routes
# ----------------------------------------------------------

@router.post(
    "/cases/{case_id}/officers",
    response_model=OfficerAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign an officer to a case",
)
@router.post(
    "/cases/{case_id}/officer-assignments",
    response_model=OfficerAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign an officer to a case (alias)",
)
def assign_officer(
    case_id: str,
    payload: OfficerAssignmentCreate,
    officer_service: OfficerService = Depends(OfficerService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Assign an officer to a case.
    Requires Investigator, Supervisor, or Admin role.
    """
    return officer_service.assign_officer(case_id, payload)


@router.get(
    "/cases/{case_id}/officers",
    response_model=OfficerAssignmentListResponse,
    status_code=status.HTTP_200_OK,
    summary="List officer assignments for a case",
)
@router.get(
    "/cases/{case_id}/officer-assignments",
    response_model=OfficerAssignmentListResponse,
    status_code=status.HTTP_200_OK,
    summary="List officer assignments for a case (alias)",
)
def get_case_officer_assignments(
    case_id: str,
    officer_id: Optional[str] = Query(None, description="Filter by officer ID"),
    role: Optional[OfficerRole] = Query(None, description="Filter by officer role"),
    is_active: Optional[bool] = Query(None, description="Filter active assignments"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: OfficerSortField = Query(
        OfficerSortField.ASSIGNED_DATE, description="Sort field"
    ),
    sort_order: SortOrder = Query(
        SortOrder.DESC, description="Sort order: asc or desc"
    ),
    officer_service: OfficerService = Depends(OfficerService),
    current_user: User = Depends(get_current_user),
):
    """
    List officer assignments for a case with filtering, pagination, and sorting.
    Requires authentication.
    """
    options = OfficerAssignmentQueryOptions(
        case_master_id=case_id,
        officer_id=officer_id,
        role=role,
        is_active=is_active,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return officer_service.search_assignments(options)


@router.put(
    "/officers/assignments/{id}",
    response_model=OfficerAssignmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update officer assignment details",
)
@router.put(
    "/cases/{case_id}/officer-assignments/{id}",
    response_model=OfficerAssignmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update officer assignment details for a case",
)
def update_assignment(
    id: str,
    payload: OfficerAssignmentUpdate,
    case_id: Optional[str] = None,
    officer_service: OfficerService = Depends(OfficerService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Update an officer assignment record.
    Requires Investigator, Supervisor, or Admin role.
    """
    return officer_service.update_assignment(id, payload)


@router.delete(
    "/officers/assignments/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an officer assignment record",
)
@router.delete(
    "/cases/{case_id}/officer-assignments/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an officer assignment record for a case",
)
def delete_assignment(
    id: str,
    case_id: Optional[str] = None,
    officer_service: OfficerService = Depends(OfficerService),
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Delete an officer assignment record by ID.
    Requires Supervisor or Admin role.
    """
    officer_service.delete_assignment(id)
