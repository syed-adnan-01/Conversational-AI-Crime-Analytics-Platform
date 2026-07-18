from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.permissions import require_roles
from app.core.logging import app_logger
from app.core.roles import UserRole
from app.models.user import User
from app.common.enums import SortOrder
from app.common.queries.case_section_query import CaseSectionQueryOptions
from app.schemas.case_section import (
    CaseSectionCreate,
    CaseSectionListResponse,
    CaseSectionResponse,
)
from app.services.case_section_service import CaseSectionService

router = APIRouter()


# ==============================================================
# POST /cases/{case_id}/sections — Assign Section
# ==============================================================

@router.post(
    "/cases/{case_id}/sections",
    response_model=CaseSectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign Legal Section to a Case",
    description=(
        "Links a legislative Section to a Case record. "
        "Requires INVESTIGATOR, SUPERVISOR, or ADMIN role. "
        "Validates case/section existence and prevents duplicate links."
    ),
    responses={
        201: {"description": "Section assigned successfully."},
        404: {"description": "Case or Section not found."},
        409: {"description": "Section already assigned to this case."},
    },
)
async def assign_section(
    case_id: str,
    data: CaseSectionCreate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
        )
    ),
    service: CaseSectionService = Depends(),
) -> CaseSectionResponse:
    app_logger.info(
        "Assign section request | User=%s | CaseID=%s | SectionID=%s",
        current_user.employee_id,
        case_id,
        data.section_id,
    )
    return service.assign_section(case_id, data)


# ==============================================================
# GET /cases/{case_id}/sections — List Case Sections
# ==============================================================

@router.get(
    "/cases/{case_id}/sections",
    response_model=CaseSectionListResponse,
    summary="List Sections Assigned to a Case",
    description=(
        "Retrieve detailed paginated summaries of all legal sections "
        "assigned to a case. Requires authentication."
    ),
)
async def list_case_sections(
    case_id: str,
    section_id: Optional[str] = Query(default=None),
    remarks: Optional[str] = Query(default=None),
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
    service: CaseSectionService = Depends(),
) -> CaseSectionListResponse:
    options = CaseSectionQueryOptions(
        case_master_id=case_id,
        section_id=section_id,
        remarks=remarks,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return service.search_case_sections(options)


# ==============================================================
# DELETE /cases/{case_id}/sections/{association_id} — Unassign Section
# ==============================================================

@router.delete(
    "/cases/{case_id}/sections/{association_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove Section Assignment",
    description="Deletes a case-section link. Requires SUPERVISOR or ADMIN role.",
    responses={
        204: {"description": "Section assignment removed successfully."},
        404: {"description": "Case or Assignment link not found."},
    },
)
async def remove_section(
    case_id: str,
    association_id: str,
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: CaseSectionService = Depends(),
) -> None:
    app_logger.info(
        "Remove section assignment request | User=%s | CaseID=%s | LinkID=%s",
        current_user.employee_id,
        case_id,
        association_id,
    )
    service.remove_section(case_id, association_id)
