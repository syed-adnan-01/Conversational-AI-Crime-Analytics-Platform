from uuid import uuid4
from datetime import datetime
from typing import Optional
from fastapi import Depends

from app.common.exceptions import CaseNotFoundException
from app.models.timeline import TimelineEvent, TimelineEventType
from app.repository.case_repository import CaseRepository
from app.repository.timeline_repository import TimelineRepository
from app.common.queries.timeline_query import TimelineQueryOptions
from app.schemas.timeline import (
    TimelineEventCreate,
    TimelineEventResponse,
    TimelineEventListResponse,
    PaginationMeta,
)


class TimelineService:
    """
    Service for investigation timeline management.
    Handles automatic and explicit event logging, timeline queries, and case validations.
    """

    def __init__(
        self,
        case_repo=CaseRepository,
        timeline_repo=TimelineRepository,
    ):
        self.case_repo = case_repo
        self.timeline_repo = timeline_repo

    def record_event(
        self,
        case_master_id: str,
        event_type: TimelineEventType,
        title: str,
        description: str,
        reference_id: Optional[str] = None,
        reference_type: Optional[str] = None,
        created_by: Optional[str] = None,
        event_time: Optional[datetime] = None,
    ) -> TimelineEventResponse:
        """
        Record a new timeline event for a case.
        Validates case existence before appending.
        """
        case = self.case_repo.get_case_by_id(case_master_id)
        if case is None:
            raise CaseNotFoundException(case_master_id)

        event_id = f"EV-{uuid4().hex[:12].upper()}"
        event_timestamp = event_time or datetime.now()

        event = TimelineEvent(
            event_id=event_id,
            case_master_id=case_master_id,
            event_type=event_type,
            title=title,
            description=description,
            reference_id=reference_id,
            reference_type=reference_type,
            created_by=created_by,
            event_time=event_timestamp,
        )

        stored = self.timeline_repo.create_event(event)
        return TimelineEventResponse.model_validate(stored)

    def create_explicit_event(
        self, case_master_id: str, schema: TimelineEventCreate
    ) -> TimelineEventResponse:
        """
        Create a timeline event from explicit schema input.
        """
        return self.record_event(
            case_master_id=case_master_id,
            event_type=schema.event_type,
            title=schema.title,
            description=schema.description,
            reference_id=schema.reference_id,
            reference_type=schema.reference_type,
            created_by=schema.created_by,
            event_time=schema.event_time,
        )

    def get_case_timeline(
        self, options: TimelineQueryOptions
    ) -> TimelineEventListResponse:
        """
        Retrieve timeline events matching query options.
        """
        if options.case_master_id:
            case = self.case_repo.get_case_by_id(options.case_master_id)
            if case is None:
                raise CaseNotFoundException(options.case_master_id)

        records, total = self.timeline_repo.query_timeline(options)
        items = [TimelineEventResponse.model_validate(e) for e in records]
        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return TimelineEventListResponse(items=items, pagination=meta)
