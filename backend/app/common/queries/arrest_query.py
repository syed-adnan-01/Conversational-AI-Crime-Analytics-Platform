from typing import Optional
from pydantic import BaseModel, Field

from app.common.enums import SortOrder
from app.models.arrest import ArrestStatus
from app.schemas.arrest import ArrestSortField


class ArrestQueryOptions(BaseModel):
    """
    Query options for arrest searching, filtering, sorting, and pagination.
    """
    case_master_id: Optional[str] = None
    accused_id: Optional[str] = None
    status: Optional[ArrestStatus] = None
    arresting_officer: Optional[str] = None
    arrest_location: Optional[str] = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    sort_by: ArrestSortField = ArrestSortField.ARREST_DATE
    sort_order: SortOrder = SortOrder.DESC
