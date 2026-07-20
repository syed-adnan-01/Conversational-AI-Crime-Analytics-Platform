from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_roles
from app.core.roles import UserRole
from app.models.user import User
from app.models.chargesheet import ChargesheetStatus
from app.common.enums import SortOrder
from app.common.queries.chargesheet_query import ChargesheetQueryOptions
from app.schemas.chargesheet import (
    ChargesheetCreate,
    ChargesheetUpdate,
    ChargesheetResponse,
    ChargesheetListResponse,
    ChargesheetSortField,
)
from app.services.chargesheet_service import ChargesheetService

router = APIRouter()


@router.post(
    "/cases/{case_id}/chargesheets",
    response_model=ChargesheetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="File a new chargesheet for a case",
)
def create_chargesheet(
    case_id: str,
    payload: ChargesheetCreate,
    chargesheet_service: ChargesheetService = Depends(ChargesheetService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    File a chargesheet for a case with associated accused, evidence, and sections.
    Requires Investigator, Supervisor, or Admin role.
    """
    return chargesheet_service.create_chargesheet(case_id, payload)


@router.get(
    "/cases/{case_id}/chargesheets",
    response_model=ChargesheetListResponse,
    status_code=status.HTTP_200_OK,
    summary="List chargesheets filed under a case",
)
def get_case_chargesheets(
    case_id: str,
    chargesheet_number: Optional[str] = Query(None, description="Search by chargesheet number"),
    status_filter: Optional[ChargesheetStatus] = Query(None, alias="status", description="Filter by status"),
    investigating_officer: Optional[str] = Query(None, description="Search by investigating officer"),
    summary: Optional[str] = Query(None, description="Keyword search in summary"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: ChargesheetSortField = Query(
        ChargesheetSortField.FILING_DATE, description="Sort field"
    ),
    sort_order: SortOrder = Query(
        SortOrder.DESC, description="Sort order: asc or desc"
    ),
    chargesheet_service: ChargesheetService = Depends(ChargesheetService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve chargesheets for a case with filtering, searching, and pagination.
    Requires authentication.
    """
    options = ChargesheetQueryOptions(
        case_master_id=case_id,
        chargesheet_number=chargesheet_number,
        status=status_filter,
        investigating_officer=investigating_officer,
        summary=summary,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return chargesheet_service.search_chargesheets(options)


@router.get(
    "/chargesheets/{id}",
    response_model=ChargesheetResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve chargesheet details by ID",
)
def get_chargesheet(
    id: str,
    chargesheet_service: ChargesheetService = Depends(ChargesheetService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve chargesheet details by ID.
    Requires authentication.
    """
    return chargesheet_service.get_chargesheet(id)


@router.put(
    "/chargesheets/{id}",
    response_model=ChargesheetResponse,
    status_code=status.HTTP_200_OK,
    summary="Update chargesheet details",
)
def update_chargesheet(
    id: str,
    payload: ChargesheetUpdate,
    chargesheet_service: ChargesheetService = Depends(ChargesheetService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Update chargesheet details and association links by ID.
    Requires Investigator, Supervisor, or Admin role.
    """
    return chargesheet_service.update_chargesheet(id, payload)


@router.delete(
    "/chargesheets/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a chargesheet record",
)
def delete_chargesheet(
    id: str,
    chargesheet_service: ChargesheetService = Depends(ChargesheetService),
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Delete a chargesheet record by ID.
    Requires Supervisor or Admin role.
    """
    chargesheet_service.delete_chargesheet(id)
