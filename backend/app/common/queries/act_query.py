from dataclasses import dataclass
from typing import Optional

from app.common.enums import SortOrder
from app.schemas.act import ActSortField


@dataclass
class ActQueryOptions:
    """
    Typed query options for legislative Acts.
    """
    name: Optional[str] = None
    short_name: Optional[str] = None
    year: Optional[int] = None

    # Sorting
    sort_by: ActSortField = ActSortField.CREATED_DATE
    sort_order: SortOrder = SortOrder.DESC

    # Pagination
    page: int = 1
    page_size: int = 20
