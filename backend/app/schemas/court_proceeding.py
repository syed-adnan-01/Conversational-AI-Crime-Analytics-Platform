from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from app.models.court_proceeding import ProceedingStage
from app.schemas.case import PaginationMeta


class CourtProceedingSortField(str, Enum):
    """Sort fields for court proceedings."""
    HEARING_DATE = "hearing_date"
    STAGE = "stage"
    NEXT_HEARING_DATE = "next_hearing_date"
    CREATED_AT = "created_at"


class CourtProceedingCreate(BaseModel):
    """Schema for registering a new court proceeding."""
    court_name: str = Field(..., min_length=2, max_length=200)
    judge_name: str = Field(..., min_length=2, max_length=150)
    hearing_date: datetime
    stage: ProceedingStage
    summary: str = Field(..., min_length=5)
    order_passed: Optional[str] = None
    next_hearing_date: Optional[datetime] = None


class CourtProceedingUpdate(BaseModel):
    """Schema for updating a court proceeding."""
    court_name: Optional[str] = Field(None, min_length=2, max_length=200)
    judge_name: Optional[str] = Field(None, min_length=2, max_length=150)
    hearing_date: Optional[datetime] = None
    stage: Optional[ProceedingStage] = None
    summary: Optional[str] = Field(None, min_length=5)
    order_passed: Optional[str] = None
    next_hearing_date: Optional[datetime] = None


class CourtProceedingResponse(BaseModel):
    """Detailed response schema for a court proceeding."""
    model_config = ConfigDict(from_attributes=True)

    proceeding_id: str
    case_master_id: str
    court_name: str
    judge_name: str
    hearing_date: datetime
    stage: ProceedingStage
    summary: str
    order_passed: Optional[str] = None
    next_hearing_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CourtProceedingSummary(BaseModel):
    """Summary schema for court proceeding list views."""
    model_config = ConfigDict(from_attributes=True)

    proceeding_id: str
    case_master_id: str
    court_name: str
    hearing_date: datetime
    stage: ProceedingStage
    next_hearing_date: Optional[datetime] = None


class CourtProceedingListResponse(BaseModel):
    """Paginated list response for court proceedings."""
    items: List[CourtProceedingResponse]
    pagination: PaginationMeta
