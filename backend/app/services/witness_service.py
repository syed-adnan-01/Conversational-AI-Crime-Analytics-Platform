from uuid import uuid4
from fastapi import Depends

from app.common.exceptions import (
    CaseNotFoundException,
    WitnessNotFoundException,
    DuplicateWitnessException,
)
from app.common.validators import validate_email, validate_phone
from app.models.witness import Witness
from app.models.timeline import TimelineEventType
from app.repository.case_repository import CaseRepository
from app.repository.witness_repository import WitnessRepository
from app.services.timeline_service import TimelineService
from app.common.queries.witness_query import WitnessQueryOptions
from app.schemas.witness import (
    WitnessCreate,
    WitnessUpdate,
    WitnessResponse,
    WitnessSummary,
    WitnessListResponse,
    PaginationMeta,
)


class WitnessService:
    """
    Service responsible for Witness management business logic.
    """

    def __init__(
        self,
        case_repo=CaseRepository,
        witness_repo=WitnessRepository,
        timeline_service=None,
    ):
        self.case_repo = case_repo
        self.witness_repo = witness_repo
        self.timeline_service = timeline_service or TimelineService()

    def create_witness(
        self, case_master_id: str, schema: WitnessCreate
    ) -> WitnessResponse:
        """
        Register a new witness for a specific case.
        """
        case = self.case_repo.get_case_by_id(case_master_id)
        if case is None:
            raise CaseNotFoundException(case_master_id)

        mobile_no = validate_phone(schema.mobile_no) if schema.mobile_no else None
        email = validate_email(schema.email) if schema.email else None
        name = schema.name.strip()

        # Duplicate check in same case (matching name and mobile)
        existing_witnesses = self.witness_repo.get_witnesses_by_case_id(case_master_id)
        for existing in existing_witnesses:
            if existing.name.lower() == name.lower() and mobile_no and existing.mobile_no == mobile_no:
                raise DuplicateWitnessException(name, case_master_id)

        witness_id = f"WT-{uuid4().hex[:12].upper()}"

        witness = Witness(
            witness_id=witness_id,
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
            statement=schema.statement,
            statement_date=schema.statement_date,
            is_hostile=schema.is_hostile,
        )

        stored = self.witness_repo.create_witness(witness)

        # Trigger Timeline Event
        self.timeline_service.record_event(
            case_master_id=case_master_id,
            event_type=TimelineEventType.WITNESS_ADDED,
            title=f"Witness Registered: {name}",
            description=f"Witness '{name}' recorded for case {case_master_id}.",
            reference_id=witness_id,
            reference_type="Witness",
        )

        return WitnessResponse.model_validate(stored)

    def get_witness(self, witness_id: str) -> WitnessResponse:
        """
        Retrieve a witness by ID.
        """
        witness = self.witness_repo.get_witness_by_id(witness_id)
        if witness is None:
            raise WitnessNotFoundException(witness_id)

        return WitnessResponse.model_validate(witness)

    def update_witness(
        self, witness_id: str, schema: WitnessUpdate
    ) -> WitnessResponse:
        """
        Update an existing witness record.
        """
        existing = self.witness_repo.get_witness_by_id(witness_id)
        if existing is None:
            raise WitnessNotFoundException(witness_id)

        updates = schema.model_dump(exclude_unset=True)

        if "mobile_no" in updates and updates["mobile_no"]:
            updates["mobile_no"] = validate_phone(updates["mobile_no"])
        if "email" in updates and updates["email"]:
            updates["email"] = validate_email(updates["email"])
        if "name" in updates and updates["name"]:
            updates["name"] = updates["name"].strip()

        updated_name = updates.get("name", existing.name)
        updated_mobile = updates.get("mobile_no", existing.mobile_no)

        if updated_name != existing.name or updated_mobile != existing.mobile_no:
            existing_witnesses = self.witness_repo.get_witnesses_by_case_id(existing.case_master_id)
            for other in existing_witnesses:
                if other.witness_id == witness_id:
                    continue
                if (
                    other.name.lower() == updated_name.lower()
                    and updated_mobile
                    and other.mobile_no == updated_mobile
                ):
                    raise DuplicateWitnessException(updated_name, existing.case_master_id)

        updated_witness = existing.model_copy(update=updates)
        stored = self.witness_repo.update_witness(updated_witness)

        if stored is None:
            raise WitnessNotFoundException(witness_id)

        return WitnessResponse.model_validate(stored)

    def delete_witness(self, witness_id: str) -> None:
        """
        Delete a witness by ID.
        """
        existing = self.witness_repo.get_witness_by_id(witness_id)
        if existing is None:
            raise WitnessNotFoundException(witness_id)

        self.witness_repo.delete_witness(witness_id)

    def search_witnesses(
        self, options: WitnessQueryOptions
    ) -> WitnessListResponse:
        """
        Query witnesses with options.
        """
        records, total = self.witness_repo.query_witnesses(options)
        summaries = [WitnessSummary.model_validate(w) for w in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return WitnessListResponse(items=summaries, pagination=meta)
