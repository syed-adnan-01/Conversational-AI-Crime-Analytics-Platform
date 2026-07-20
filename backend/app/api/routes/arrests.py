from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_roles
from app.core.roles import UserRole
from app.models.user import User
from app.models.arrest import ArrestStatus
from app.common.enums import SortOrder
from app.common.queries.arrest_query import ArrestQueryOptions
from app.schemas.arrest import (
    ArrestCreate,
    ArrestUpdate,
    ArrestResponse,
    ArrestListResponse,
    ArrestSortField,
)
from app.services.arrest_service import ArrestService

router = APIRouter()


@router.post(
    "/cases/{case_id}/arrests",
    response_model=ArrestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record an arrest under a case",
)
def create_arrest(
    case_id: str,
    payload: ArrestCreate,
    arrest_service: ArrestService = Depends(ArrestService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Record an arrest of an accused under a case.
    Requires Investigator, Supervisor, or Admin role.
    """
    return arrest_service.create_arrest(case_id, payload)


@router.get(
    "/cases/{case_id}/arrests",
    response_model=ArrestListResponse,
    status_code=status.HTTP_200_OK,
    summary="List arrests recorded under a case",
)
def get_case_arrests(
    case_id: str,
    accused_id: Optional[str] = Query(None, description="Filter by accused ID"),
    status_filter: Optional[ArrestStatus] = Query(None, alias="status", description="Filter by arrest status"),
    arresting_officer: Optional[str] = Query(None, description="Keyword search for arresting officer"),
    arrest_location: Optional[str] = Query(None, description="Keyword search for arrest location"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: ArrestSortField = Query(
        ArrestSortField.ARREST_DATE, description="Sort field"
    ),
    sort_order: SortOrder = Query(
        SortOrder.DESC, description="Sort order: asc or desc"
    ),
    arrest_service: ArrestService = Depends(ArrestService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve arrests for a case with filtering, pagination, and sorting.
    Requires authentication.
    """
    options = ArrestQueryOptions(
        case_master_id=case_id,
        accused_id=accused_id,
        status=status_filter,
        arresting_officer=arresting_officer,
        arrest_location=arrest_location,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return arrest_service.search_arrests(options)


@router.get(
    "/arrests/{id}",
    response_model=ArrestResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve arrest details by ID",
)
def get_arrest(
    id: str,
    arrest_service: ArrestService = Depends(ArrestService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve arrest record details by ID.
    Requires authentication.
    """
    return arrest_service.get_arrest(id)


@router.put(
    "/arrests/{id}",
    response_model=ArrestResponse,
    status_code=status.HTTP_200_OK,
    summary="Update arrest details",
)
def update_arrest(
    id: str,
    payload: ArrestUpdate,
    arrest_service: ArrestService = Depends(ArrestService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Update arrest record details by ID.
    Requires Investigator, Supervisor, or Admin role.
    """
    return arrest_service.update_arrest(id, payload)


@router.delete(
    "/arrests/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an arrest record",
)
def delete_arrest(
    id: str,
    arrest_service: ArrestService = Depends(ArrestService),
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Delete an arrest record by ID.
    Requires Supervisor or Admin role.
    """
    arrest_service.delete_arrest(id)
