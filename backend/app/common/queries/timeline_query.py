from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.common.enums import SortOrder
from app.models.timeline import TimelineEventType
from app.schemas.timeline import TimelineSortField


class TimelineQueryOptions(BaseModel):
    """
    Query options for timeline event searching, filtering, sorting, and pagination.
    """
    case_master_id: Optional[str] = None
    event_type: Optional[TimelineEventType] = None
    title: Optional[str] = None
    description: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    sort_by: TimelineSortField = TimelineSortField.EVENT_TIME
    sort_order: SortOrder = SortOrder.DESC

    @field_validator("to_date")
    @classmethod
    def validate_date_range(cls, v: Optional[datetime], info) -> Optional[datetime]:
        from_date = info.data.get("from_date")
        if from_date and v and v < from_date:
            raise ValueError("to_date must be after or equal to from_date")
        return v
