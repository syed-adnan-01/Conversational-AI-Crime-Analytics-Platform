from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.permissions import require_roles
from app.core.logging import app_logger
from app.core.roles import UserRole
from app.models.user import User
from app.common.enums import SortOrder
from app.models.evidence import EvidenceType, EvidenceCategory, EvidenceStatus, CustodyStatus
from app.common.queries.evidence_query import EvidenceQueryOptions
from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceUpdate,
    EvidenceResponse,
    EvidenceListResponse,
    EvidenceSortField,
)
from app.services.evidence_service import EvidenceService

router = APIRouter()


# ==============================================================
# POST /cases/{case_id}/evidence — Register Evidence
# ==============================================================

@router.post(
    "/cases/{case_id}/evidence",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register Evidence under Case",
    description="Registers a new evidence record and links it to a case. Requires INVESTIGATOR, SUPERVISOR, or ADMIN.",
    responses={
        201: {"description": "Evidence registered successfully."},
        400: {"description": "Validation error (future collection date)."},
        404: {"description": "Case, victim, accused, or section not found."},
        409: {"description": "Duplicate evidence number in case."},
    },
)
async def create_evidence(
    case_id: str,
    data: EvidenceCreate,
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: EvidenceService = Depends(),
) -> EvidenceResponse:
    app_logger.info(
        "Register evidence request | User=%s | CaseID=%s | Title=%s",
        current_user.employee_id,
        case_id,
        data.title if data else None,
    )
    return service.create_evidence(case_id, data)


# ==============================================================
# GET /cases/{case_id}/evidence — List Evidence for a Case
# ==============================================================

@router.get(
    "/cases/{case_id}/evidence",
    response_model=EvidenceListResponse,
    summary="List Evidence for a Case",
    description="Retrieve a paginated list of evidence records linked to a specific case. Requires authentication.",
)
async def list_case_evidence(
    case_id: str,
    evidence_number: Optional[str] = Query(default=None, description="Search by evidence number."),
    title: Optional[str] = Query(default=None, description="Search by title."),
    description: Optional[str] = Query(default=None, description="Search by description."),
    evidence_type: Optional[EvidenceType] = Query(default=None, description="Filter by type."),
    evidence_category: Optional[EvidenceCategory] = Query(default=None, description="Filter by category."),
    status: Optional[EvidenceStatus] = Query(default=None, description="Filter by status."),
    custody_status: Optional[CustodyStatus] = Query(default=None, description="Filter by custody status."),
    collected_by: Optional[str] = Query(default=None, description="Search by collecting officer."),
    victim_id: Optional[str] = Query(default=None, description="Filter by victim ID."),
    accused_id: Optional[str] = Query(default=None, description="Filter by accused ID."),
    section_id: Optional[str] = Query(default=None, description="Filter by legal section ID."),
    sort_by: EvidenceSortField = Query(default=EvidenceSortField.CREATED_DATE),
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
    service: EvidenceService = Depends(),
) -> EvidenceListResponse:
    options = EvidenceQueryOptions(
        case_master_id=case_id,
        evidence_number=evidence_number,
        title=title,
        description=description,
        evidence_type=evidence_type,
        evidence_category=evidence_category,
        status=status,
        custody_status=custody_status,
        collected_by=collected_by,
        victim_id=victim_id,
        accused_id=accused_id,
        section_id=section_id,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return service.search_evidence(options)


# ==============================================================
# GET /evidence/{evidence_id} — Get Evidence Details
# ==============================================================

@router.get(
    "/evidence/{evidence_id}",
    response_model=EvidenceResponse,
    summary="Get Evidence Details",
    description="Retrieve details of a specific evidence record. Requires authentication.",
    responses={
        200: {"description": "Evidence retrieved successfully."},
        404: {"description": "Evidence not found."},
    },
)
async def get_evidence(
    evidence_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.INVESTIGATOR,
            UserRole.ANALYST,
        )
    ),
    service: EvidenceService = Depends(),
) -> EvidenceResponse:
    app_logger.info(
        "Get evidence details request | User=%s | ID=%s",
        current_user.employee_id,
        evidence_id,
    )
    return service.get_evidence_by_id(evidence_id)


# ==============================================================
# PUT /evidence/{evidence_id} — Update Evidence
# ==============================================================

@router.put(
    "/evidence/{evidence_id}",
    response_model=EvidenceResponse,
    summary="Update Evidence Details",
    description="Update an existing evidence record. Requires INVESTIGATOR, SUPERVISOR, or ADMIN.",
    responses={
        200: {"description": "Evidence updated successfully."},
        400: {"description": "Validation error."},
        404: {"description": "Evidence or referenced entities not found."},
    },
)
async def update_evidence(
    evidence_id: str,
    data: EvidenceUpdate,
    current_user: User = Depends(
        require_roles(UserRole.INVESTIGATOR, UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: EvidenceService = Depends(),
) -> EvidenceResponse:
    app_logger.info(
        "Update evidence request | User=%s | ID=%s",
        current_user.employee_id,
        evidence_id,
    )
    return service.update_evidence(evidence_id, data)


# ==============================================================
# DELETE /evidence/{evidence_id} — Delete Evidence
# ==============================================================

@router.delete(
    "/evidence/{evidence_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Evidence",
    description="Deletes an evidence record from the system. Requires SUPERVISOR or ADMIN.",
    responses={
        204: {"description": "Evidence deleted successfully."},
        404: {"description": "Evidence not found."},
    },
)
async def delete_evidence(
    evidence_id: str,
    current_user: User = Depends(
        require_roles(UserRole.SUPERVISOR, UserRole.ADMIN)
    ),
    service: EvidenceService = Depends(),
) -> None:
    app_logger.info(
        "Delete evidence request | User=%s | ID=%s",
        current_user.employee_id,
        evidence_id,
    )
    service.delete_evidence(evidence_id)
