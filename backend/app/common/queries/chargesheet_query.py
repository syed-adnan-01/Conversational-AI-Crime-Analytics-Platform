from typing import Optional
from pydantic import BaseModel, Field

from app.common.enums import SortOrder
from app.models.chargesheet import ChargesheetStatus
from app.schemas.chargesheet import ChargesheetSortField


class ChargesheetQueryOptions(BaseModel):
    """
    Query options for chargesheet searching, filtering, sorting, and pagination.
    """
    case_master_id: Optional[str] = None
    chargesheet_number: Optional[str] = None
    status: Optional[ChargesheetStatus] = None
    investigating_officer: Optional[str] = None
    summary: Optional[str] = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    sort_by: ChargesheetSortField = ChargesheetSortField.FILING_DATE
    sort_order: SortOrder = SortOrder.DESC
