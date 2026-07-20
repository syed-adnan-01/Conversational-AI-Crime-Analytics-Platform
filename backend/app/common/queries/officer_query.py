from typing import Optional
from pydantic import BaseModel, Field

from app.common.enums import SortOrder
from app.models.officer import OfficerRole
from app.schemas.officer import OfficerSortField


class OfficerAssignmentQueryOptions(BaseModel):
    """
    Query options for filtering officer assignments.
    """
    case_master_id: Optional[str] = None
    officer_id: Optional[str] = None
    role: Optional[OfficerRole] = None
    is_active: Optional[bool] = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    sort_by: OfficerSortField = OfficerSortField.ASSIGNED_DATE
    sort_order: SortOrder = SortOrder.DESC
