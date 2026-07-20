from uuid import uuid4
from datetime import datetime
from fastapi import Depends

from app.common.exceptions import (
    CaseNotFoundException,
    CourtProceedingNotFoundException,
)
from app.models.court_proceeding import CourtProceeding
from app.models.timeline import TimelineEventType
from app.repository.case_repository import CaseRepository
from app.repository.court_proceeding_repository import CourtProceedingRepository
from app.services.timeline_service import TimelineService
from app.common.queries.court_proceeding_query import CourtProceedingQueryOptions
from app.schemas.court_proceeding import (
    CourtProceedingCreate,
    CourtProceedingUpdate,
    CourtProceedingResponse,
    CourtProceedingSummary,
    CourtProceedingListResponse,
    PaginationMeta,
)


class CourtProceedingService:
    """
    Service responsible for Court Proceeding management business logic.
    """

    def __init__(
        self,
        case_repo=CaseRepository,
        proceeding_repo=CourtProceedingRepository,
        timeline_service=None,
    ):
        self.case_repo = case_repo
        self.proceeding_repo = proceeding_repo
        self.timeline_service = timeline_service or TimelineService()

    def create_proceeding(
        self, case_master_id: str, schema: CourtProceedingCreate
    ) -> CourtProceedingResponse:
        """
        Record a new court proceeding for a case.
        """
        case = self.case_repo.get_case_by_id(case_master_id)
        if case is None:
            raise CaseNotFoundException(case_master_id)

        proceeding_id = f"CP-{uuid4().hex[:12].upper()}"

        proceeding = CourtProceeding(
            proceeding_id=proceeding_id,
            case_master_id=case_master_id,
            court_name=schema.court_name.strip(),
            judge_name=schema.judge_name.strip(),
            hearing_date=schema.hearing_date,
            stage=schema.stage,
            summary=schema.summary.strip(),
            order_passed=schema.order_passed,
            next_hearing_date=schema.next_hearing_date,
        )

        stored = self.proceeding_repo.create_proceeding(proceeding)

        # Trigger Timeline Event
        self.timeline_service.record_event(
            case_master_id=case_master_id,
            event_type=TimelineEventType.COURT_HEARING,
            title=f"Court Hearing: {schema.stage.value}",
            description=f"Court proceeding recorded before {schema.judge_name} at {schema.court_name}.",
            reference_id=proceeding_id,
            reference_type="CourtProceeding",
        )

        return CourtProceedingResponse.model_validate(stored)

    def get_proceeding(self, proceeding_id: str) -> CourtProceedingResponse:
        """
        Retrieve court proceeding details by ID.
        """
        proceeding = self.proceeding_repo.get_proceeding_by_id(proceeding_id)
        if proceeding is None:
            raise CourtProceedingNotFoundException(proceeding_id)

        return CourtProceedingResponse.model_validate(proceeding)

    def update_proceeding(
        self, proceeding_id: str, schema: CourtProceedingUpdate
    ) -> CourtProceedingResponse:
        """
        Update an existing court proceeding.
        """
        existing = self.proceeding_repo.get_proceeding_by_id(proceeding_id)
        if existing is None:
            raise CourtProceedingNotFoundException(proceeding_id)

        updates = schema.model_dump(exclude_unset=True)

        if "court_name" in updates and updates["court_name"]:
            updates["court_name"] = updates["court_name"].strip()
        if "judge_name" in updates and updates["judge_name"]:
            updates["judge_name"] = updates["judge_name"].strip()
        if "summary" in updates and updates["summary"]:
            updates["summary"] = updates["summary"].strip()

        updated_proceeding = existing.model_copy(update=updates)
        stored = self.proceeding_repo.update_proceeding(updated_proceeding)

        if stored is None:
            raise CourtProceedingNotFoundException(proceeding_id)

        return CourtProceedingResponse.model_validate(stored)

    def delete_proceeding(self, proceeding_id: str) -> None:
        """
        Delete a court proceeding record by ID.
        """
        existing = self.proceeding_repo.get_proceeding_by_id(proceeding_id)
        if existing is None:
            raise CourtProceedingNotFoundException(proceeding_id)

        self.proceeding_repo.delete_proceeding(proceeding_id)

    def search_proceedings(
        self, options: CourtProceedingQueryOptions
    ) -> CourtProceedingListResponse:
        """
        Query court proceedings with options.
        """
        records, total = self.proceeding_repo.query_proceedings(options)
        items = [CourtProceedingResponse.model_validate(cp) for cp in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return CourtProceedingListResponse(items=items, pagination=meta)
