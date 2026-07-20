from typing import Optional
from pydantic import BaseModel, Field

from app.common.enums import SortOrder, Gender, IdentificationType
from app.schemas.witness import WitnessSortField


class WitnessQueryOptions(BaseModel):
    """
    Query options for witness searching, filtering, sorting, and pagination.
    """
    case_master_id: Optional[str] = None
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    gender: Optional[Gender] = None
    is_hostile: Optional[bool] = None
    id_type: Optional[IdentificationType] = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    sort_by: WitnessSortField = WitnessSortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC
