from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.models.timeline import TimelineEventType
from app.models.user import User
from app.common.enums import SortOrder
from app.common.queries.timeline_query import TimelineQueryOptions
from app.schemas.timeline import TimelineEventCreate, TimelineEventResponse, TimelineEventListResponse, TimelineSortField
from app.services.timeline_service import TimelineService

router = APIRouter()


@router.post(
    "/cases/{case_id}/timeline",
    response_model=TimelineEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record explicit timeline event for a case",
)
def create_timeline_event(
    case_id: str,
    schema: TimelineEventCreate,
    timeline_service: TimelineService = Depends(TimelineService),
    current_user: User = Depends(get_current_user),
):
    """
    Record an explicit investigation event/note to the append-only timeline.
    """
    schema.created_by = current_user.employee_id
    return timeline_service.create_explicit_event(case_id, schema)


@router.get(
    "/timeline/{event_id}",
    response_model=TimelineEventResponse,
    status_code=status.HTTP_200_OK,
    summary="Get timeline event details",
)
def get_timeline_event(
    event_id: str,
    timeline_service: TimelineService = Depends(TimelineService),
    current_user: User = Depends(get_current_user),
):
    """
    Get details for a single timeline event.
    """
    event = timeline_service.timeline_repo.get_event_by_id(event_id)
    if event is None:
        from app.common.exceptions import DomainException
        raise DomainException(f"Timeline event with ID '{event_id}' not found.", status_code=404)
    return TimelineEventResponse.model_validate(event)


@router.get(
    "/cases/{case_id}/timeline",
    response_model=TimelineEventListResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve chronological timeline events for a case",
)
def get_case_timeline(
    case_id: str,
    event_type: Optional[TimelineEventType] = Query(None, description="Filter by event type"),
    title: Optional[str] = Query(None, description="Keyword search in title"),
    description: Optional[str] = Query(None, description="Keyword search in description"),
    from_date: Optional[datetime] = Query(None, description="Filter events from date"),
    to_date: Optional[datetime] = Query(None, description="Filter events to date"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: TimelineSortField = Query(
        TimelineSortField.EVENT_TIME, description="Sort field"
    ),
    sort_order: SortOrder = Query(
        SortOrder.DESC, description="Sort order: asc or desc"
    ),
    timeline_service: TimelineService = Depends(TimelineService),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve chronological timeline events for a specific case with filtering, pagination, and sorting.
    Requires authentication.
    """
    options = TimelineQueryOptions(
        case_master_id=case_id,
        event_type=event_type,
        title=title,
        description=description,
        from_date=from_date,
        to_date=to_date,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return timeline_service.get_case_timeline(options)
