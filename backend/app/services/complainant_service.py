from uuid import uuid4
from typing import Optional
from fastapi import Depends

from app.common.exceptions import CaseNotFoundException, ComplainantNotFoundException, DuplicateComplainantException
from app.common.validators import validate_email, validate_phone
from app.core.logging import complainant_logger
from app.models.complainant import Complainant
from app.repository.case_repository import CaseRepository
from app.repository.complainant_repository import ComplainantRepository
from app.common.queries.complainant_query import ComplainantQueryOptions
from app.schemas.complainant import (
    ComplainantCreate,
    ComplainantResponse,
    ComplainantSummary,
    ComplainantListResponse,
    PaginationMeta,
    ComplainantUpdate,
)


class ComplainantService:
    """
    Service responsible for complainant management business logic.

    Uses constructor-based dependency injection to access repositories,
    ensuring isolation and clean testing patterns.
    """

    def __init__(
        self,
        case_repo: CaseRepository = Depends(lambda: CaseRepository),
        complainant_repo: ComplainantRepository = Depends(
            lambda: ComplainantRepository
        ),
    ):
        self.case_repo = case_repo
        self.complainant_repo = complainant_repo

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    def create_complainant(
        self, case_master_id: str, schema: ComplainantCreate
    ) -> ComplainantResponse:
        """
        Register a new complainant for a specific case.

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

        # 3. Check for Duplicate Complainants in same case
        existing_complainants = self.complainant_repo.get_complainants_by_case_id(
            case_master_id
        )
        for existing in existing_complainants:
            # Check duplicate name & mobile number
            if (
                existing.name.lower() == name.lower()
                and existing.mobile_no == mobile_no
            ):
                raise DuplicateComplainantException(name, case_master_id)

        # 4. Generate ID in the Service
        complainant_id = f"CP-{uuid4().hex[:12].upper()}"

        # 5. Build Domain Entity
        complainant = Complainant(
            complainant_id=complainant_id,
            case_master_id=case_master_id,
            name=name,
            gender=schema.gender,
            age=schema.age,
            mobile_no=mobile_no,
            email=email,
            address=schema.address,
            nationality=schema.nationality,
            occupation=schema.occupation,
            relationship_type=schema.relationship_type,
            relative_name=schema.relative_name,
        )

        # 6. Persist
        stored = self.complainant_repo.create_complainant(complainant)

        # 7. Trigger Timeline Event
        try:
            from app.models.timeline import TimelineEventType
            from app.services.timeline_service import TimelineService
            timeline_svc = TimelineService()
            timeline_svc.record_event(
                case_master_id=case_master_id,
                event_type=TimelineEventType.COMPLAINANT_REGISTERED,
                title=f"Complainant Registered: {name}",
                description=f"Complainant '{name}' recorded for case {case_master_id}.",
                reference_id=complainant_id,
                reference_type="Complainant",
            )
        except Exception as e:
            complainant_logger.warning("Timeline event generation failed: %s", str(e))

        return ComplainantResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Retrieve
    # ----------------------------------------------------------

    def get_complainant(self, complainant_id: str) -> ComplainantResponse:
        """
        Retrieve a complainant by ID.
        Throws ComplainantNotFoundException if the record is missing.
        """
        complainant = self.complainant_repo.get_complainant_by_id(complainant_id)
        if complainant is None:
            raise ComplainantNotFoundException(complainant_id)

        return ComplainantResponse.model_validate(complainant)

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    def update_complainant(
        self, complainant_id: str, schema: ComplainantUpdate
    ) -> ComplainantResponse:
        """
        Update an existing complainant record.

        Validates inputs, verifies duplicate constraints, and replaces the
        entire domain object in the repository.
        """
        # 1. Fetch Existing
        existing = self.complainant_repo.get_complainant_by_id(complainant_id)
        if existing is None:
            raise ComplainantNotFoundException(complainant_id)

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
            existing_complainants = self.complainant_repo.get_complainants_by_case_id(
                existing.case_master_id
            )
            for other in existing_complainants:
                if other.complainant_id == complainant_id:
                    continue
                if (
                    other.name.lower() == updated_name.lower()
                    and other.mobile_no == updated_mobile
                ):
                    raise DuplicateComplainantException(
                        updated_name, existing.case_master_id
                    )

        # 4. Perform Complete Domain Object Replacement
        updated_complainant = existing.model_copy(update=updates)
        stored = self.complainant_repo.update_complainant(updated_complainant)

        if stored is None:
            raise ComplainantNotFoundException(complainant_id)

        return ComplainantResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    def delete_complainant(self, complainant_id: str) -> None:
        """
        Delete a complainant by ID.
        """
        existing = self.complainant_repo.get_complainant_by_id(complainant_id)
        if existing is None:
            raise ComplainantNotFoundException(complainant_id)

        self.complainant_repo.delete_complainant(complainant_id)

    # ----------------------------------------------------------
    # Search / List
    # ----------------------------------------------------------

    def search_complainants(
        self, options: ComplainantQueryOptions
    ) -> ComplainantListResponse:
        """
        Perform complainant queries using a structured ComplainantQueryOptions.
        Returns a paginated list response.
        """
        records, total = self.complainant_repo.query_complainants(options)

        summaries = [ComplainantSummary.model_validate(r) for r in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )

        return ComplainantListResponse(items=summaries, pagination=meta)
