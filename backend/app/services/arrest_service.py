from uuid import uuid4
from datetime import datetime
from fastapi import Depends

from app.common.exceptions import (
    CaseNotFoundException,
    AccusedNotFoundException,
    ArrestNotFoundException,
    DuplicateArrestException,
)
from app.models.arrest import Arrest, ArrestStatus
from app.models.timeline import TimelineEventType
from app.repository.case_repository import CaseRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.arrest_repository import ArrestRepository
from app.services.timeline_service import TimelineService
from app.common.queries.arrest_query import ArrestQueryOptions
from app.schemas.arrest import (
    ArrestCreate,
    ArrestUpdate,
    ArrestResponse,
    ArrestListResponse,
    PaginationMeta,
)


class ArrestService:
    """
    Service responsible for Arrest management business logic.
    """

    def __init__(
        self,
        case_repo=CaseRepository,
        accused_repo=AccusedRepository,
        arrest_repo=ArrestRepository,
        timeline_service=None,
    ):
        self.case_repo = case_repo
        self.accused_repo = accused_repo
        self.arrest_repo = arrest_repo
        self.timeline_service = timeline_service or TimelineService()

    def create_arrest(
        self, case_master_id: str, schema: ArrestCreate
    ) -> ArrestResponse:
        """
        Record an arrest for an accused under a specific case.
        """
        case = self.case_repo.get_case_by_id(case_master_id)
        if case is None:
            raise CaseNotFoundException(case_master_id)

        accused = self.accused_repo.get_accused_by_id(schema.accused_id)
        if accused is None or accused.case_master_id != case_master_id:
            raise AccusedNotFoundException(schema.accused_id)

        # Check for duplicate active arrest for same accused in same case
        existing_arrests = self.arrest_repo.get_arrests_by_accused_id(schema.accused_id)
        for existing in existing_arrests:
            if existing.case_master_id == case_master_id and existing.status in [
                ArrestStatus.ARRESTED,
                ArrestStatus.REMANDED,
                ArrestStatus.DETAINED,
            ]:
                raise DuplicateArrestException(schema.accused_id, case_master_id)

        arrest_id = f"AR-{uuid4().hex[:12].upper()}"

        arrest = Arrest(
            arrest_id=arrest_id,
            case_master_id=case_master_id,
            accused_id=schema.accused_id,
            arrest_date=schema.arrest_date,
            arrest_time=schema.arrest_time,
            arrest_location=schema.arrest_location.strip(),
            grounds_for_arrest=schema.grounds_for_arrest.strip(),
            arresting_officer=schema.arresting_officer.strip(),
            arrest_memo=schema.arrest_memo,
            status=schema.status,
            remarks=schema.remarks,
        )

        stored = self.arrest_repo.create_arrest(arrest)

        # Trigger Timeline Event
        self.timeline_service.record_event(
            case_master_id=case_master_id,
            event_type=TimelineEventType.ARREST_MADE,
            title=f"Accused Arrested: {accused.name}",
            description=f"Accused '{accused.name}' arrested by {schema.arresting_officer} at {schema.arrest_location}.",
            reference_id=arrest_id,
            reference_type="Arrest",
        )

        response = ArrestResponse.model_validate(stored)
        response.accused_name = accused.name
        return response

    def get_arrest(self, arrest_id: str) -> ArrestResponse:
        """
        Retrieve arrest details by ID.
        """
        arrest = self.arrest_repo.get_arrest_by_id(arrest_id)
        if arrest is None:
            raise ArrestNotFoundException(arrest_id)

        response = ArrestResponse.model_validate(arrest)
        accused = self.accused_repo.get_accused_by_id(arrest.accused_id)
        if accused:
            response.accused_name = accused.name
        return response

    def update_arrest(
        self, arrest_id: str, schema: ArrestUpdate
    ) -> ArrestResponse:
        """
        Update an existing arrest record.
        """
        existing = self.arrest_repo.get_arrest_by_id(arrest_id)
        if existing is None:
            raise ArrestNotFoundException(arrest_id)

        updates = schema.model_dump(exclude_unset=True)

        if "arrest_location" in updates and updates["arrest_location"]:
            updates["arrest_location"] = updates["arrest_location"].strip()
        if "grounds_for_arrest" in updates and updates["grounds_for_arrest"]:
            updates["grounds_for_arrest"] = updates["grounds_for_arrest"].strip()
        if "arresting_officer" in updates and updates["arresting_officer"]:
            updates["arresting_officer"] = updates["arresting_officer"].strip()

        updated_arrest = existing.model_copy(update=updates)
        stored = self.arrest_repo.update_arrest(updated_arrest)

        if stored is None:
            raise ArrestNotFoundException(arrest_id)

        response = ArrestResponse.model_validate(stored)
        accused = self.accused_repo.get_accused_by_id(stored.accused_id)
        if accused:
            response.accused_name = accused.name
        return response

    def delete_arrest(self, arrest_id: str) -> None:
        """
        Delete an arrest record by ID.
        """
        existing = self.arrest_repo.get_arrest_by_id(arrest_id)
        if existing is None:
            raise ArrestNotFoundException(arrest_id)

        self.arrest_repo.delete_arrest(arrest_id)

    def search_arrests(
        self, options: ArrestQueryOptions
    ) -> ArrestListResponse:
        """
        Query arrests using query options.
        """
        records, total = self.arrest_repo.query_arrests(options)
        responses = []
        for r in records:
            res = ArrestResponse.model_validate(r)
            accused = self.accused_repo.get_accused_by_id(r.accused_id)
            if accused:
                res.accused_name = accused.name
            responses.append(res)

        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return ArrestListResponse(items=responses, pagination=meta)
