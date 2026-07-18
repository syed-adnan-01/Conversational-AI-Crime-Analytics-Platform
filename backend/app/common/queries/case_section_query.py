from dataclasses import dataclass
from typing import Optional

from app.common.enums import SortOrder


@dataclass
class CaseSectionQueryOptions:
    """
    Typed query options for Case Section Associations.
    """
    case_master_id: Optional[str] = None
    section_id: Optional[str] = None
    act_id: Optional[str] = None
    remarks: Optional[str] = None

    # Sorting (always by association date)
    sort_order: SortOrder = SortOrder.DESC

    # Pagination
    page: int = 1
    page_size: int = 20
