from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from app.models.arrest import ArrestStatus
from app.schemas.case import PaginationMeta


class ArrestSortField(str, Enum):
    """Sort fields for arrest query options."""
    ARREST_DATE = "arrest_date"
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class ArrestCreate(BaseModel):
    """Schema for registering a new arrest."""
    accused_id: str
    arrest_date: datetime
    arrest_time: Optional[str] = None
    arrest_location: str = Field(..., min_length=2, max_length=250)
    grounds_for_arrest: str = Field(..., min_length=5)
    arresting_officer: str = Field(..., min_length=2, max_length=150)
    arrest_memo: Optional[str] = None
    status: ArrestStatus = ArrestStatus.ARRESTED
    remarks: Optional[str] = None


class ArrestUpdate(BaseModel):
    """Schema for updating an existing arrest record."""
    arrest_date: Optional[datetime] = None
    arrest_time: Optional[str] = None
    arrest_location: Optional[str] = Field(None, min_length=2, max_length=250)
    grounds_for_arrest: Optional[str] = Field(None, min_length=5)
    arresting_officer: Optional[str] = Field(None, min_length=2, max_length=150)
    arrest_memo: Optional[str] = None
    status: Optional[ArrestStatus] = None
    remarks: Optional[str] = None


class ArrestResponse(BaseModel):
    """Detailed response schema for an arrest record."""
    model_config = ConfigDict(from_attributes=True)

    arrest_id: str
    case_master_id: str
    accused_id: str
    accused_name: Optional[str] = None
    arrest_date: datetime
    arrest_time: Optional[str] = None
    arrest_location: str
    grounds_for_arrest: str
    arresting_officer: str
    arrest_memo: Optional[str] = None
    status: ArrestStatus
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ArrestSummary(BaseModel):
    """Summary schema for arrest list views."""
    model_config = ConfigDict(from_attributes=True)

    arrest_id: str
    case_master_id: str
    accused_id: str
    arrest_date: datetime
    arrest_location: str
    arresting_officer: str
    status: ArrestStatus


class ArrestListResponse(BaseModel):
    """Paginated list response for arrest records."""
    items: List[ArrestResponse]
    pagination: PaginationMeta
