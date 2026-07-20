from uuid import uuid4
from fastapi import Depends

from app.common.exceptions import (
    CaseNotFoundException,
    OfficerNotFoundException,
    DuplicateOfficerBadgeException,
    OfficerAssignmentNotFoundException,
)
from app.models.officer import OfficerMaster, OfficerAssignment
from app.repository.case_repository import CaseRepository
from app.repository.officer_repository import OfficerRepository
from app.common.queries.officer_query import OfficerAssignmentQueryOptions
from app.schemas.officer import (
    OfficerMasterCreate,
    OfficerMasterResponse,
    OfficerAssignmentCreate,
    OfficerAssignmentUpdate,
    OfficerAssignmentResponse,
    OfficerAssignmentListResponse,
    PaginationMeta,
)


class OfficerService:
    """
    Service for managing Officer profiles and transactional case assignments.
    """

    def __init__(
        self,
        case_repo=CaseRepository,
        officer_repo=OfficerRepository,
    ):
        self.case_repo = case_repo
        self.officer_repo = officer_repo

    # ----------------------------------------------------------
    # Master Officer Management
    # ----------------------------------------------------------

    def create_officer(self, schema: OfficerMasterCreate) -> OfficerMasterResponse:
        """
        Create a new Officer master profile.
        """
        badge = schema.badge_number.strip()
        existing = self.officer_repo.get_officer_by_badge(badge)
        if existing:
            raise DuplicateOfficerBadgeException(badge)

        officer_id = f"OFF-{uuid4().hex[:12].upper()}"

        officer = OfficerMaster(
            officer_id=officer_id,
            badge_number=badge,
            name=schema.name.strip(),
            rank=schema.rank,
            department=schema.department.strip(),
            police_station_id=schema.police_station_id,
            mobile_no=schema.mobile_no,
            email=schema.email,
            is_active=schema.is_active,
        )

        stored = self.officer_repo.create_officer(officer)
        return OfficerMasterResponse.model_validate(stored)

    def get_officer(self, officer_id: str) -> OfficerMasterResponse:
        """
        Get officer details by ID.
        """
        officer = self.officer_repo.get_officer_by_id(officer_id)
        if officer is None:
            raise OfficerNotFoundException(officer_id)
        return OfficerMasterResponse.model_validate(officer)

    def list_officers(self) -> list[OfficerMasterResponse]:
        """
        List all officer master profiles.
        """
        officers = self.officer_repo.list_officers()
        return [OfficerMasterResponse.model_validate(o) for o in officers]

    # ----------------------------------------------------------
    # Transactional Case Assignment Management
    # ----------------------------------------------------------

    def assign_officer(
        self, case_master_id: str, schema: OfficerAssignmentCreate
    ) -> OfficerAssignmentResponse:
        """
        Assign an officer to a case.
        """
        case = self.case_repo.get_case_by_id(case_master_id)
        if case is None:
            raise CaseNotFoundException(case_master_id)

        officer = self.officer_repo.get_officer_by_id(schema.officer_id)
        if officer is None:
            raise OfficerNotFoundException(schema.officer_id)

        assignment_id = f"OA-{uuid4().hex[:12].upper()}"

        assignment = OfficerAssignment(
            assignment_id=assignment_id,
            case_master_id=case_master_id,
            officer_id=schema.officer_id,
            role=schema.role,
            assigned_date=schema.assigned_date,
            relieved_date=schema.relieved_date,
            is_active=schema.is_active,
            remarks=schema.remarks,
        )

        stored = self.officer_repo.create_assignment(assignment)
        response = OfficerAssignmentResponse.model_validate(stored)
        response.officer_name = officer.name
        response.badge_number = officer.badge_number
        response.rank = officer.rank
        return response

    def update_assignment(
        self, assignment_id: str, schema: OfficerAssignmentUpdate
    ) -> OfficerAssignmentResponse:
        """
        Update an officer assignment.
        """
        existing = self.officer_repo.get_assignment_by_id(assignment_id)
        if existing is None:
            raise OfficerAssignmentNotFoundException(assignment_id)

        updates = schema.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=updates)

        stored = self.officer_repo.update_assignment(updated)
        if stored is None:
            raise OfficerAssignmentNotFoundException(assignment_id)

        response = OfficerAssignmentResponse.model_validate(stored)
        officer = self.officer_repo.get_officer_by_id(stored.officer_id)
        if officer:
            response.officer_name = officer.name
            response.badge_number = officer.badge_number
            response.rank = officer.rank
        return response

    def delete_assignment(self, assignment_id: str) -> None:
        """
        Delete an officer assignment record.
        """
        existing = self.officer_repo.get_assignment_by_id(assignment_id)
        if existing is None:
            raise OfficerAssignmentNotFoundException(assignment_id)
        self.officer_repo.delete_assignment(assignment_id)

    def search_assignments(
        self, options: OfficerAssignmentQueryOptions
    ) -> OfficerAssignmentListResponse:
        """
        Query officer assignments.
        """
        records, total = self.officer_repo.query_assignments(options)
        responses = []
        for r in records:
            res = OfficerAssignmentResponse.model_validate(r)
            officer = self.officer_repo.get_officer_by_id(r.officer_id)
            if officer:
                res.officer_name = officer.name
                res.badge_number = officer.badge_number
                res.rank = officer.rank
            responses.append(res)

        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return OfficerAssignmentListResponse(items=responses, pagination=meta)
