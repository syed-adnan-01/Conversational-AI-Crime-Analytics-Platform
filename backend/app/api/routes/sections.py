from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.permissions import require_roles
from app.core.logging import app_logger
from app.core.roles import UserRole
from app.models.user import User
from app.common.enums import SortOrder
from app.common.queries.section_query import SectionQueryOptions
from app.schemas.section import (
    SectionCreate,
    SectionListResponse,
    SectionResponse,
    SectionSortField,
    SectionUpdate,
)
from app.services.section_service import SectionService

router = APIRouter()


# ==============================================================
# POST /sections — Create Section
# ==============================================================

@router.post(
    "/sections",
    response_model=SectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Legal Section",
    description="Registers a new Section under an Act. Requires SUPERVISOR or ADMIN role.",
    responses={
        201: {"description": "Section created successfully."},
        404: {"description": "Referenced Act not found."},
        409: {"description": "Duplicate Section under the Act."},
    },
)
async def create_section(
    act_id: str = Query(..., description="ID of the parent legislative Act."),
    data: SectionCreate = None,
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: SectionService = Depends(),
) -> SectionResponse:
    app_logger.info(
        "Create section request | User=%s | ActID=%s | SecNo=%s",
        current_user.employee_id,
        act_id,
        data.section_number if data else None,
    )
    return service.create_section(act_id, data)


# ==============================================================
# GET /sections — List/Search Sections
# ==============================================================

@router.get(
    "/sections",
    response_model=SectionListResponse,
    summary="List Legal Sections",
    description="Retrieve a paginated list of Sections across all Acts. Requires authentication.",
)
async def list_sections(
    act_id: Optional[str] = Query(default=None, description="Filter by Act ID."),
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


# ==============================================================
# GET /sections/{section_id} — Get Section Details
# ==============================================================

@router.get(
    "/sections/{section_id}",
    response_model=SectionResponse,
    summary="Get Section Details",
    description="Retrieve details of a specific Section. Requires authentication.",
    responses={
        200: {"description": "Section details retrieved successfully."},
        404: {"description": "Section not found."},
    },
)
async def get_section(
    section_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: SectionService = Depends(),
) -> SectionResponse:
    return service.get_section(section_id)


# ==============================================================
# PUT /sections/{section_id} — Update Section
# ==============================================================

@router.put(
    "/sections/{section_id}",
    response_model=SectionResponse,
    summary="Update Section Details",
    description="Update an existing Section master record. Requires SUPERVISOR or ADMIN role.",
    responses={
        200: {"description": "Section updated successfully."},
        404: {"description": "Section not found."},
        409: {"description": "Constraint violation (duplicate section number)."},
    },
)
async def update_section(
    section_id: str,
    data: SectionUpdate,
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: SectionService = Depends(),
) -> SectionResponse:
    app_logger.info("Update section request | User=%s | ID=%s", current_user.employee_id, section_id)
    return service.update_section(section_id, data)


# ==============================================================
# DELETE /sections/{section_id} — Delete Section
# ==============================================================

@router.delete(
    "/sections/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Section",
    description="Deletes a Section from the system. Requires ADMIN role.",
    responses={
        204: {"description": "Section deleted successfully."},
        404: {"description": "Section not found."},
    },
)
async def delete_section(
    section_id: str,
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
    service: SectionService = Depends(),
) -> None:
    app_logger.info("Delete section request | User=%s | ID=%s", current_user.employee_id, section_id)
    service.delete_section(section_id)
