from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_roles
from app.core.roles import UserRole
from app.models.user import User
from app.models.court_proceeding import ProceedingStage
from app.common.enums import SortOrder
from app.common.queries.court_proceeding_query import CourtProceedingQueryOptions
from app.schemas.court_proceeding import (
    CourtProceedingCreate,
    CourtProceedingUpdate,
    CourtProceedingResponse,
    CourtProceedingListResponse,
    CourtProceedingSortField,
)
from app.services.court_proceeding_service import CourtProceedingService

router = APIRouter()


@router.post(
    "/cases/{case_id}/court-proceedings",
    response_model=CourtProceedingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a new court proceeding for a case",
)
def create_court_proceeding(
    case_id: str,
    payload: CourtProceedingCreate,
    proceeding_service: CourtProceedingService = Depends(CourtProceedingService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Record a court proceeding for a case.
    Requires Investigator, Supervisor, or Admin role.
    """
    return proceeding_service.create_proceeding(case_id, payload)


@router.get(
    "/cases/{case_id}/court-proceedings",
    response_model=CourtProceedingListResponse,
    status_code=status.HTTP_200_OK,
    summary="List court proceedings for a case",
)
def get_case_court_proceedings(
    case_id: str,
    court_name: Optional[str] = Query(None, description="Search by court name"),
    judge_name: Optional[str] = Query(None, description="Search by judge name"),
    stage: Optional[ProceedingStage] = Query(None, description="Filter by proceeding stage"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: CourtProceedingSortField = Query(
        CourtProceedingSortField.HEARING_DATE, description="Sort field"
    ),
    sort_order: SortOrder = Query(
        SortOrder.DESC, description="Sort order: asc or desc"
    ),
    proceeding_service: CourtProceedingService = Depends(CourtProceedingService),
    current_user: User = Depends(get_current_user),
):
    """
    List court proceedings for a case with filtering, searching, and pagination.
    Requires authentication.
    """
    options = CourtProceedingQueryOptions(
        case_master_id=case_id,
        court_name=court_name,
        judge_name=judge_name,
        stage=stage,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return proceeding_service.search_proceedings(options)


@router.get(
    "/court-proceedings/{id}",
    response_model=CourtProceedingResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve court proceeding details by ID",
)
def get_court_proceeding(
    id: str,
    proceeding_service: CourtProceedingService = Depends(CourtProceedingService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve court proceeding details by ID.
    Requires authentication.
    """
    return proceeding_service.get_proceeding(id)


@router.put(
    "/court-proceedings/{id}",
    response_model=CourtProceedingResponse,
    status_code=status.HTTP_200_OK,
    summary="Update court proceeding details",
)
def update_court_proceeding(
    id: str,
    payload: CourtProceedingUpdate,
    proceeding_service: CourtProceedingService = Depends(CourtProceedingService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Update court proceeding details by ID.
    Requires Investigator, Supervisor, or Admin role.
    """
    return proceeding_service.update_proceeding(id, payload)


@router.delete(
    "/court-proceedings/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a court proceeding record",
)
def delete_court_proceeding(
    id: str,
    proceeding_service: CourtProceedingService = Depends(CourtProceedingService),
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Delete a court proceeding record by ID.
    Requires Supervisor or Admin role.
    """
    proceeding_service.delete_proceeding(id)
