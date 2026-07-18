from dataclasses import dataclass
from typing import Optional

from app.common.enums import SortOrder
from app.schemas.section import SectionSortField


@dataclass
class SectionQueryOptions:
    """
    Typed query options for legal Sections.
    """
    act_id: Optional[str] = None
    section_number: Optional[str] = None
    title: Optional[str] = None
    is_cognizable: Optional[bool] = None
    is_bailable: Optional[bool] = None

    # Sorting
    sort_by: SectionSortField = SectionSortField.SECTION_NUMBER
    sort_order: SortOrder = SortOrder.ASC

    # Pagination
    page: int = 1
    page_size: int = 20
