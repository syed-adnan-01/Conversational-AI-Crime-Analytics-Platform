from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.permissions import require_roles
from app.core.logging import app_logger
from app.core.roles import UserRole
from app.models.user import User
from app.common.enums import SortOrder
from app.common.queries.act_query import ActQueryOptions
from app.common.queries.section_query import SectionQueryOptions
from app.schemas.act import (
    ActCreate,
    ActListResponse,
    ActResponse,
    ActSortField,
    ActUpdate,
)
from app.schemas.section import SectionListResponse, SectionSortField
from app.services.act_service import ActService
from app.services.section_service import SectionService

router = APIRouter()


# ==============================================================
# POST /acts — Create Act
# ==============================================================

@router.post(
    "/acts",
    response_model=ActResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Legislative Act",
    description="Registers a new Act in the legal catalog. Requires SUPERVISOR or ADMIN role.",
    responses={
        201: {"description": "Act created successfully."},
        409: {"description": "Duplicate Act registered."},
    },
)
async def create_act(
    data: ActCreate,
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: ActService = Depends(),
) -> ActResponse:
    app_logger.info("Create act request | User=%s | ShortName=%s", current_user.employee_id, data.short_name)
    return service.create_act(data)


# ==============================================================
# GET /acts — Search/List Acts
# ==============================================================

@router.get(
    "/acts",
    response_model=ActListResponse,
    summary="List Legislative Acts",
    description="Retrieve a paginated list of Acts. Supports filters, sorting, and pagination. Requires authentication.",
)
async def list_acts(
    name: Optional[str] = Query(default=None, description="Search by name."),
    short_name: Optional[str] = Query(default=None, description="Search by short name."),
    year: Optional[int] = Query(default=None, description="Filter by year."),
    sort_by: ActSortField = Query(default=ActSortField.CREATED_DATE),
    sort_order: SortOrder = Query(default=SortOrder.DESC),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: ActService = Depends(),
) -> ActListResponse:
    options = ActQueryOptions(
        name=name,
        short_name=short_name,
        year=year,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return service.search_acts(options)


# ==============================================================
# GET /acts/{act_id} — Get Act Details
# ==============================================================

@router.get(
    "/acts/{act_id}",
    response_model=ActResponse,
    summary="Get Act Details",
    description="Retrieve full details of an Act by ID. Requires authentication.",
    responses={
        200: {"description": "Act details retrieved successfully."},
        404: {"description": "Act not found."},
    },
)
async def get_act(
    act_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: ActService = Depends(),
) -> ActResponse:
    return service.get_act(act_id)


# ==============================================================
# PUT /acts/{act_id} — Update Act
# ==============================================================

@router.put(
    "/acts/{act_id}",
    response_model=ActResponse,
    summary="Update Act Details",
    description="Update details of an existing Act. Requires SUPERVISOR or ADMIN role.",
    responses={
        200: {"description": "Act updated successfully."},
        404: {"description": "Act not found."},
        409: {"description": "Constraint violation (duplicate)."},
    },
)
async def update_act(
    act_id: str,
    data: ActUpdate,
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: ActService = Depends(),
) -> ActResponse:
    app_logger.info("Update act request | User=%s | ID=%s", current_user.employee_id, act_id)
    return service.update_act(act_id, data)


# ==============================================================
# DELETE /acts/{act_id} — Delete Act
# ==============================================================

@router.delete(
    "/acts/{act_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Act",
    description="Deletes an Act from the system. Requires ADMIN role.",
    responses={
        204: {"description": "Act deleted successfully."},
        404: {"description": "Act not found."},
    },
)
async def delete_act(
    act_id: str,
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
    service: ActService = Depends(),
) -> None:
    app_logger.info("Delete act request | User=%s | ID=%s", current_user.employee_id, act_id)
    service.delete_act(act_id)


# ==============================================================
# GET /acts/{act_id}/sections — Get Sections under Act
# ==============================================================

@router.get(
    "/acts/{act_id}/sections",
    response_model=SectionListResponse,
    summary="List Sections under a specific Act",
    description="Retrieve a paginated list of Sections linked to a specific Act. Requires authentication.",
)
async def list_act_sections(
    act_id: str,
    section_number: Optional[str] = Query(default=None, description="Search by section number."),
    title: Optional[str] = Query(default=None, description="Search by title."),
    is_cognizable: Optional[bool] = Query(default=None),
    is_bailable: Optional[bool] = Query(default=None),
    sort_by: SectionSortField = Query(default=SectionSortField.SECTION_NUMBER),
    sort_order: SortOrder = Query(default=SortOrder.ASC),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: SectionService = Depends(),
) -> SectionListResponse:
    # Set the act_id filter specifically
    options = SectionQueryOptions(
        act_id=act_id,
        section_number=section_number,
        title=title,
        is_cognizable=is_cognizable,
        is_bailable=is_bailable,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return service.search_sections(options)
