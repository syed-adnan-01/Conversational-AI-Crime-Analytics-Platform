from uuid import uuid4
from typing import Optional
from fastapi import Depends

from app.common.exceptions import CaseNotFoundException, VictimNotFoundException, DuplicateVictimException
from app.common.validators import validate_email, validate_phone
from app.models.victim import Victim
from app.repository.case_repository import CaseRepository
from app.repository.victim_repository import VictimRepository
from app.common.queries.victim_query import VictimQueryOptions
from app.schemas.victim import (
    VictimCreate,
    VictimResponse,
    VictimSummary,
    VictimListResponse,
    PaginationMeta,
    VictimUpdate,
)


class VictimService:
    """
    Service responsible for victim management business logic.

    Uses constructor-based dependency injection to access repositories,
    ensuring isolation and clean testing patterns.
    """

    def __init__(
        self,
        case_repo: CaseRepository = Depends(lambda: CaseRepository),
        victim_repo: VictimRepository = Depends(
            lambda: VictimRepository
        ),
    ):
        self.case_repo = case_repo
        self.victim_repo = victim_repo

    # ----------------------------------------------------------
    # Create
    # ----------------------------------------------------------

    def create_victim(
        self, case_master_id: str, schema: VictimCreate
    ) -> VictimResponse:
        """
        Register a new victim for a specific case.

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

        # 3. Check for Duplicate Victims in same case
        # Duplicate detection is intentionally simple and designed to evolve
        existing_victims = self.victim_repo.get_victims_by_case_id(
            case_master_id
        )
        for existing in existing_victims:
            # Check duplicate name & mobile number
            if (
                existing.name.lower() == name.lower()
                and existing.mobile_no == mobile_no
            ):
                raise DuplicateVictimException(name, case_master_id)

        # 4. Generate ID in the Service
        victim_id = f"VT-{uuid4().hex[:12].upper()}"

        # 5. Build Domain Entity
        victim = Victim(
            victim_id=victim_id,
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
        stored = self.victim_repo.create_victim(victim)

        # 7. Trigger Timeline Event
        try:
            from app.models.timeline import TimelineEventType
            from app.services.timeline_service import TimelineService
            timeline_svc = TimelineService()
            timeline_svc.record_event(
                case_master_id=case_master_id,
                event_type=TimelineEventType.VICTIM_ADDED,
                title=f"Victim Recorded: {name}",
                description=f"Victim '{name}' added to case {case_master_id}.",
                reference_id=victim_id,
                reference_type="Victim",
            )
        except Exception as e:
            pass

        return VictimResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Retrieve
    # ----------------------------------------------------------

    def get_victim(self, victim_id: str) -> VictimResponse:
        """
        Retrieve a victim by ID.
        Throws VictimNotFoundException if the record is missing.
        """
        victim = self.victim_repo.get_victim_by_id(victim_id)
        if victim is None:
            raise VictimNotFoundException(victim_id)

        return VictimResponse.model_validate(victim)

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------

    def update_victim(
        self, victim_id: str, schema: VictimUpdate
    ) -> VictimResponse:
        """
        Update an existing victim record.

        Validates inputs, verifies duplicate constraints, and replaces the
        entire domain object in the repository.
        """
        # 1. Fetch Existing
        existing = self.victim_repo.get_victim_by_id(victim_id)
        if existing is None:
            raise VictimNotFoundException(victim_id)

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
            existing_victims = self.victim_repo.get_victims_by_case_id(
                existing.case_master_id
            )
            for other in existing_victims:
                if other.victim_id == victim_id:
                    continue
                if (
                    other.name.lower() == updated_name.lower()
                    and other.mobile_no == updated_mobile
                ):
                    raise DuplicateVictimException(
                        updated_name, existing.case_master_id
                    )

        # 4. Perform Complete Domain Object Replacement
        updated_victim = existing.model_copy(update=updates)
        stored = self.victim_repo.update_victim(updated_victim)

        if stored is None:
            raise VictimNotFoundException(victim_id)

        return VictimResponse.model_validate(stored)

    # ----------------------------------------------------------
    # Delete
    # ----------------------------------------------------------

    def delete_victim(self, victim_id: str) -> None:
        """
        Delete a victim by ID.
        """
        existing = self.victim_repo.get_victim_by_id(victim_id)
        if existing is None:
            raise VictimNotFoundException(victim_id)

        self.victim_repo.delete_victim(victim_id)

    # ----------------------------------------------------------
    # Search / List
    # ----------------------------------------------------------

    def search_victims(
        self, options: VictimQueryOptions
    ) -> VictimListResponse:
        """
        Perform victim queries using a structured VictimQueryOptions.
        Returns a paginated list response.
        """
        records, total = self.victim_repo.query_victims(options)

        summaries = [VictimSummary.model_validate(v) for v in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )

        return VictimListResponse(items=summaries, pagination=meta)
