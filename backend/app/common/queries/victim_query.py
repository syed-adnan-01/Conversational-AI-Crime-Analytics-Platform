from dataclasses import dataclass
from typing import Optional

from app.common.enums import Gender, IdentificationType, SortOrder
from app.schemas.victim import VictimSortField


@dataclass
class VictimQueryOptions:
    """
    Typed query options passed from the Service to the Repository layer.
    Encapsulates all normalized filtering, sorting, and pagination options.
    """
    case_master_id: Optional[str] = None
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    nationality: Optional[str] = None
    occupation: Optional[str] = None
    id_type: Optional[IdentificationType] = None
    id_number: Optional[str] = None

    # Sorting
    sort_by: VictimSortField = VictimSortField.CREATED_DATE
    sort_order: SortOrder = SortOrder.DESC

    # Pagination
    page: int = 1
    page_size: int = 20
