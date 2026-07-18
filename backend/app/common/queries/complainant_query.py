from dataclasses import dataclass
from typing import Optional

from app.common.enums import SortOrder
from app.schemas.complainant import ComplainantSortField


@dataclass
class ComplainantQueryOptions:
    """
    Typed query options passed from the Service to the Repository layer.
    Encapsulates all normalized filtering, sorting, and pagination options.
    """
    case_master_id: Optional[str] = None
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None

    # Sorting
    sort_by: ComplainantSortField = ComplainantSortField.CREATED_DATE
    sort_order: SortOrder = SortOrder.DESC

    # Pagination
    page: int = 1
    page_size: int = 20
