from datetime import datetime
from typing import Optional

from app.core.logging import app_logger
from app.models.timeline import TimelineEvent
from app.schemas.timeline import TimelineSortField
from app.common.enums import SortOrder
from app.common.queries.timeline_query import TimelineQueryOptions


class TimelineRepository:
    """
    Append-Only Repository for investigation timeline events.

    Strict Architecture Rule: This repository is strictly append-only.
    No update or delete operations exist or are permitted.
    """

    _events: list[TimelineEvent] = []

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory timeline store.
        """
        if cls._events:
            return
        app_logger.info("Timeline repository initialized.")

    @classmethod
    def create_event(cls, event: TimelineEvent) -> TimelineEvent:
        """
        Append a new timeline event to the repository.
        """
        now = datetime.now()
        stored = event.model_copy(
            update={
                "created_at": now,
            }
        )

        cls._events.append(stored)

        app_logger.info(
            "Timeline event appended | ID=%s | CaseID=%s | Type=%s",
            stored.event_id,
            stored.case_master_id,
            stored.event_type,
        )

        return stored

    @classmethod
    def get_event_by_id(cls, event_id: str) -> Optional[TimelineEvent]:
        """
        Retrieve a single event by ID.
        """
        return next((e for e in cls._events if e.event_id == event_id), None)

    @classmethod
    def get_case_timeline(cls, case_master_id: str) -> list[TimelineEvent]:
        """
        Retrieve all timeline events for a given case, ordered by event_time descending.
        """
        case_events = [e for e in cls._events if e.case_master_id == case_master_id]
        case_events.sort(key=lambda x: x.event_time, reverse=True)
        return case_events

    @classmethod
    def query_timeline(
        cls, options: TimelineQueryOptions
    ) -> tuple[list[TimelineEvent], int]:
        """
        Query timeline events with filtering, sorting, and pagination.
        Returns a tuple of (items_subset, total_count).
        """
        filtered = list(cls._events)

        if options.case_master_id:
            filtered = [e for e in filtered if e.case_master_id == options.case_master_id]

        if options.event_type:
            filtered = [e for e in filtered if e.event_type == options.event_type]

        if options.title:
            search_title = options.title.lower()
            filtered = [e for e in filtered if search_title in e.title.lower()]

        if options.description:
            search_desc = options.description.lower()
            filtered = [e for e in filtered if search_desc in e.description.lower()]

        if options.from_date:
            filtered = [e for e in filtered if e.event_time >= options.from_date]

        if options.to_date:
            filtered = [e for e in filtered if e.event_time <= options.to_date]

        total_count = len(filtered)

        SORT_FIELDS = {
            TimelineSortField.EVENT_TIME: lambda e: e.event_time,
            TimelineSortField.EVENT_TYPE: lambda e: e.event_type.value,
            TimelineSortField.CREATED_AT: lambda e: e.created_at or datetime.min,
        }

        accessor = SORT_FIELDS.get(options.sort_by, lambda e: e.event_time)
        reverse = options.sort_order == SortOrder.DESC
        filtered.sort(key=accessor, reverse=reverse)

        start_idx = (options.page - 1) * options.page_size
        end_idx = start_idx + options.page_size
        subset = filtered[start_idx:end_idx]

        return subset, total_count
