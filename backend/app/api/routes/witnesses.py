from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_roles
from app.core.roles import UserRole
from app.models.user import User
from app.common.enums import SortOrder, Gender, IdentificationType
from app.common.queries.witness_query import WitnessQueryOptions
from app.schemas.witness import (
    WitnessCreate,
    WitnessUpdate,
    WitnessResponse,
    WitnessListResponse,
    WitnessSortField,
)
from app.services.witness_service import WitnessService

router = APIRouter()


@router.post(
    "/cases/{case_id}/witnesses",
    response_model=WitnessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new witness for a case",
)
def create_witness(
    case_id: str,
    payload: WitnessCreate,
    witness_service: WitnessService = Depends(WitnessService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Register a witness associated with a case.
    Requires Investigator, Supervisor, or Admin role.
    """
    return witness_service.create_witness(case_id, payload)


@router.get(
    "/cases/{case_id}/witnesses",
    response_model=WitnessListResponse,
    status_code=status.HTTP_200_OK,
    summary="List witnesses registered under a case",
)
def get_case_witnesses(
    case_id: str,
    name: Optional[str] = Query(None, description="Keyword search in name"),
    mobile_no: Optional[str] = Query(None, description="Filter by mobile number"),
    gender: Optional[Gender] = Query(None, description="Filter by gender"),
    is_hostile: Optional[bool] = Query(None, description="Filter by hostile witness status"),
    id_type: Optional[IdentificationType] = Query(None, description="Filter by ID type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: WitnessSortField = Query(
        WitnessSortField.CREATED_AT, description="Sort field"
    ),
    sort_order: SortOrder = Query(
        SortOrder.DESC, description="Sort order: asc or desc"
    ),
    witness_service: WitnessService = Depends(WitnessService),
    current_user: User = Depends(get_current_user),
):
    """
    List witnesses associated with a case with filtering, searching, and pagination.
    Requires authentication.
    """
    options = WitnessQueryOptions(
        case_master_id=case_id,
        name=name,
        mobile_no=mobile_no,
        gender=gender,
        is_hostile=is_hostile,
        id_type=id_type,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return witness_service.search_witnesses(options)


@router.get(
    "/witnesses/{id}",
    response_model=WitnessResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve witness details by ID",
)
def get_witness(
    id: str,
    witness_service: WitnessService = Depends(WitnessService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve witness details by ID.
    Requires authentication.
    """
    return witness_service.get_witness(id)


@router.put(
    "/witnesses/{id}",
    response_model=WitnessResponse,
    status_code=status.HTTP_200_OK,
    summary="Update witness details",
)
def update_witness(
    id: str,
    payload: WitnessUpdate,
    witness_service: WitnessService = Depends(WitnessService),
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Update witness details by ID.
    Requires Investigator, Supervisor, or Admin role.
    """
    return witness_service.update_witness(id, payload)


@router.delete(
    "/witnesses/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a witness record",
)
def delete_witness(
    id: str,
    witness_service: WitnessService = Depends(WitnessService),
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
):
    """
    Delete a witness record by ID.
    Requires Supervisor or Admin role.
    """
    witness_service.delete_witness(id)
