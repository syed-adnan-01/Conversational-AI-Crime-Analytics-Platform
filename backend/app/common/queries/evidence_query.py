from dataclasses import dataclass
from typing import Optional

from app.common.enums import SortOrder
from app.models.evidence import EvidenceType, EvidenceCategory, EvidenceStatus, CustodyStatus
from app.schemas.evidence import EvidenceSortField


@dataclass
class EvidenceQueryOptions:
    """
    Typed query options passed from the Service to the Repository layer.
    Encapsulates all filtering, searching, sorting, and pagination options.
    """
    case_master_id: Optional[str] = None
    evidence_number: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    evidence_type: Optional[EvidenceType] = None
    evidence_category: Optional[EvidenceCategory] = None
    status: Optional[EvidenceStatus] = None
    custody_status: Optional[CustodyStatus] = None
    collected_by: Optional[str] = None
    victim_id: Optional[str] = None
    accused_id: Optional[str] = None
    section_id: Optional[str] = None

    # Sorting
    sort_by: EvidenceSortField = EvidenceSortField.CREATED_DATE
    sort_order: SortOrder = SortOrder.DESC

    # Pagination
    page: int = 1
    page_size: int = 20
