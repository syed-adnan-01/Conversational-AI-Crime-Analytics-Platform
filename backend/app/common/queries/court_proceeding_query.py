from typing import Optional
from pydantic import BaseModel, Field

from app.common.enums import SortOrder
from app.models.court_proceeding import ProceedingStage
from app.schemas.court_proceeding import CourtProceedingSortField


class CourtProceedingQueryOptions(BaseModel):
    """
    Query options for court proceeding searching, filtering, sorting, and pagination.
    """
    case_master_id: Optional[str] = None
    court_name: Optional[str] = None
    judge_name: Optional[str] = None
    stage: Optional[ProceedingStage] = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    sort_by: CourtProceedingSortField = CourtProceedingSortField.HEARING_DATE
    sort_order: SortOrder = SortOrder.DESC
