from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from app.schemas.case import SortField, SortOrder


@dataclass
class CaseQueryOptions:
    """
    Typed query options passed from the Service to the Repository layer.
    Encapsulates all normalized filtering, sorting, and pagination options.
    """
    # Identifiers
    case_no: Optional[str] = None
    crime_no: Optional[str] = None

    # Date ranges
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    incident_from_date: Optional[datetime] = None
    incident_to_date: Optional[datetime] = None

    # Classifications
    case_status_id: Optional[int] = None
    case_category_id: Optional[int] = None
    gravity_offence_id: Optional[int] = None
    crime_major_head_id: Optional[int] = None
    crime_minor_head_id: Optional[int] = None

    # Organization
    police_station_id: Optional[int] = None
    police_person_id: Optional[int] = None
    court_id: Optional[int] = None
    district: Optional[str] = None
    state: Optional[str] = None

    # Keyword Search
    brief_facts: Optional[str] = None

    # Sorting
    sort_by: SortField = SortField.REGISTERED_DATE
    sort_order: SortOrder = SortOrder.DESC

    # Pagination
    page: int = 1
    page_size: int = 20
