from uuid import uuid4
from typing import Optional
from fastapi import Depends

from app.common.exceptions import CaseNotFoundException, AccusedNotFoundException, DuplicateAccusedException
from app.common.validators import validate_email, validate_phone
from app.models.accused import Accused
from app.repository.case_repository import CaseRepository
from app.repository.accused_repository import AccusedRepository
from app.common.queries.accused_query import AccusedQueryOptions
from app.schemas.accused import (
    AccusedCreate,
    AccusedResponse,
    AccusedSummary,
    AccusedListResponse,
    PaginationMeta,
    AccusedUpdate,
)


class AccusedService:
    """
    Service responsible for accused management business logic.

    Uses constructor-based dependency injection to access repositories,
    ensuring isolation and clean testing patterns.
    """

    def __init__(
        self,
        case_repo: CaseRepository = Depends(lambda: CaseRepository),
        accused_repo: AccusedRepository = Depends(
            lambda: AccusedRepository
        ),
    ):
        self.case_repo = case_repo
        self.accused_repo = accused_repo

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    def create_accused(
        self, case_master_id: str, schema: AccusedCreate
    ) -> AccusedResponse:
        """
        Register a new accused for a specific case.

        Validates case existence, applies phone/email format checks,
        performs duplicate record verification, and generates the ID.
        """
        # 1. Verify Case Existence
        case = self.case_repo.get_case_by_id(case_master_id)
        if case is None:
            raise CaseNotFoundException(case_master_id)

        # 2. Format & Validate Inputs
        mobile_no = validate_phone(schema.mobile_no)
        email = validate_email(schema.email)
        name = schema.name.strip()

        # 3. Check for Duplicate Accused in same case
        # Duplicate detection is intentionally simple and designed to evolve
        existing_accused_list = self.accused_repo.get_accused_by_case_id(
            case_master_id
        )
        for existing in existing_accused_list:
            # Check duplicate name & mobile number
            if (
                existing.name.lower() == name.lower()
                and existing.mobile_no == mobile_no
            ):
                raise DuplicateAccusedException(name, case_master_id)

        # 4. Generate ID in the Service
        accused_id = f"AC-{uuid4().hex[:12].upper()}"

        # 5. Build Domain Entity
        accused = Accused(
            accused_id=accused_id,
            case_master_id=case_master_id,
            name=name,
            gender=schema.gender,
            age=schema.age,
            mobile_no=mobile_no,
            email=email,
            address=schema.address,
            nationality=schema.nationality,
            occupation=schema.occupation,
            id_type=schema.id_type,
            id_number=schema.id_number,
        )

        # 6. Persist
        stored = self.accused_repo.create_accused(accused)

        # 7. Trigger Timeline Event
        try:
            from app.models.timeline import TimelineEventType
            from app.services.timeline_service import TimelineService
            timeline_svc = TimelineService()
            timeline_svc.record_event(
                case_master_id=case_master_id,
                event_type=TimelineEventType.ACCUSED_ADDED,
                title=f"Accused Recorded: {name}",
                description=f"Accused '{name}' named in case {case_master_id}.",
                reference_id=accused_id,
                reference_type="Accused",
            )
        except Exception as e:
            pass

        return AccusedResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Retrieve
    # ----------------------------------------------------------

    def get_accused(self, accused_id: str) -> AccusedResponse:
        """
        Retrieve an accused by ID.
        Throws AccusedNotFoundException if the record is missing.
        """
        accused = self.accused_repo.get_accused_by_id(accused_id)
        if accused is None:
            raise AccusedNotFoundException(accused_id)

        return AccusedResponse.model_validate(accused)

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    def update_accused(
        self, accused_id: str, schema: AccusedUpdate
    ) -> AccusedResponse:
        """
        Update an existing accused record.

        Validates inputs, verifies duplicate constraints, and replaces the
        entire domain object in the repository.
        """
        # 1. Fetch Existing
        existing = self.accused_repo.get_accused_by_id(accused_id)
        if existing is None:
            raise AccusedNotFoundException(accused_id)

        # 2. Format & Validate Inputs
        updates = schema.model_dump(exclude_unset=True)

        if "mobile_no" in updates:
            updates["mobile_no"] = validate_phone(updates["mobile_no"])
        if "email" in updates:
            updates["email"] = validate_email(updates["email"])
        if "name" in updates:
            updates["name"] = updates["name"].strip()

        # 3. Check duplicate constraints (if name or mobile is being updated)
        updated_name = updates.get("name", existing.name)
        updated_mobile = updates.get("mobile_no", existing.mobile_no)

        if updated_name != existing.name or updated_mobile != existing.mobile_no:
            existing_accused_list = self.accused_repo.get_accused_by_case_id(
                existing.case_master_id
            )
            for other in existing_accused_list:
                if other.accused_id == accused_id:
                    continue
                if (
                    other.name.lower() == updated_name.lower()
                    and other.mobile_no == updated_mobile
                ):
                    raise DuplicateAccusedException(
                        updated_name, existing.case_master_id
                    )

        # 4. Perform Complete Domain Object Replacement
        updated_accused = existing.model_copy(update=updates)
        stored = self.accused_repo.update_accused(updated_accused)

        if stored is None:
            raise AccusedNotFoundException(accused_id)

        return AccusedResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    def delete_accused(self, accused_id: str) -> None:
        """
        Delete an accused by ID.
        """
        existing = self.accused_repo.get_accused_by_id(accused_id)
        if existing is None:
            raise AccusedNotFoundException(accused_id)

        self.accused_repo.delete_accused(accused_id)

    # ----------------------------------------------------------
    # Search / List
    # ----------------------------------------------------------

    def search_accused(
        self, options: AccusedQueryOptions
    ) -> AccusedListResponse:
        """
        Perform accused queries using a structured AccusedQueryOptions.
        Returns a paginated list response.
        """
        records, total = self.accused_repo.query_accused(options)

        summaries = [AccusedSummary.model_validate(a) for a in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )

        return AccusedListResponse(items=summaries, pagination=meta)
