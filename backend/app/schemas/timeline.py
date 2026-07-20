from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from app.models.timeline import TimelineEventType
from app.schemas.case import PaginationMeta


class TimelineSortField(str, Enum):
    """Sort fields for timeline queries."""
    EVENT_TIME = "event_time"
    EVENT_TYPE = "event_type"
    CREATED_AT = "created_at"


class TimelineEventCreate(BaseModel):
    """Schema for creating a timeline event."""
    event_type: TimelineEventType
    title: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=2)
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    created_by: Optional[str] = None
    event_time: Optional[datetime] = None


class TimelineEventResponse(BaseModel):
    """Detailed response schema for a timeline event."""
    model_config = ConfigDict(from_attributes=True)

    event_id: str
    case_master_id: str
    event_type: TimelineEventType
    title: str
    description: str
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    created_by: Optional[str] = None
    event_time: datetime
    created_at: datetime


class TimelineEventSummary(BaseModel):
    """Summary schema for timeline list views."""
    model_config = ConfigDict(from_attributes=True)

    event_id: str
    case_master_id: str
    event_type: TimelineEventType
    title: str
    description: str
    event_time: datetime


class TimelineEventListResponse(BaseModel):
    """Paginated list response for timeline events."""
    items: List[TimelineEventResponse]
    pagination: PaginationMeta
