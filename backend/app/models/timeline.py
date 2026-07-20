from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TimelineEventType(str, Enum):
    """Supported timeline event types."""
    CASE_CREATED = "CASE_CREATED"
    COMPLAINANT_ADDED = "COMPLAINANT_ADDED"
    VICTIM_ADDED = "VICTIM_ADDED"
    ACCUSED_ADDED = "ACCUSED_ADDED"
    WITNESS_ADDED = "WITNESS_ADDED"
    SECTION_ASSIGNED = "SECTION_ASSIGNED"
    EVIDENCE_COLLECTED = "EVIDENCE_COLLECTED"
    ARREST_MADE = "ARREST_MADE"
    CHARGESHEET_FILED = "CHARGESHEET_FILED"
    COURT_HEARING = "COURT_HEARING"
    COURT_ORDER = "COURT_ORDER"
    CASE_CLOSED = "CASE_CLOSED"


class TimelineEvent(BaseModel):
    """
    Domain entity representing a chronological timeline event in an investigation.
    """

    model_config = ConfigDict(from_attributes=True)

    event_id: Optional[str] = None
    case_master_id: str
    event_type: TimelineEventType
    title: str
    description: str
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    created_by: Optional[str] = None
    event_time: datetime
    created_at: Optional[datetime] = None
