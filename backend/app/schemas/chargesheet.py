from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from app.models.chargesheet import ChargesheetStatus
from app.schemas.case import PaginationMeta


class ChargesheetSortField(str, Enum):
    """Sort fields for chargesheets."""
    FILING_DATE = "filing_date"
    CHARGESHEET_NUMBER = "chargesheet_number"
    STATUS = "status"
    CREATED_AT = "created_at"


class ChargesheetAccusedLinkCreate(BaseModel):
    """Link input for Accused association."""
    accused_id: str
    charges_summary: Optional[str] = None


class ChargesheetEvidenceLinkCreate(BaseModel):
    """Link input for Evidence association."""
    evidence_id: str
    relevance_notes: Optional[str] = None


class ChargesheetSectionLinkCreate(BaseModel):
    """Link input for Section association."""
    section_id: str
    offence_details: Optional[str] = None


class ChargesheetCreate(BaseModel):
    """Schema for creating a new chargesheet with association links."""
    chargesheet_number: Optional[str] = None
    filing_date: datetime
    investigating_officer: str = Field(..., min_length=2, max_length=150)
    summary: str = Field(..., min_length=5)
    remarks: Optional[str] = None
    status: ChargesheetStatus = ChargesheetStatus.FILED

    accused_links: List[ChargesheetAccusedLinkCreate] = []
    evidence_links: List[ChargesheetEvidenceLinkCreate] = []
    section_links: List[ChargesheetSectionLinkCreate] = []


class ChargesheetUpdate(BaseModel):
    """Schema for updating an existing chargesheet."""
    chargesheet_number: Optional[str] = None
    filing_date: Optional[datetime] = None
    investigating_officer: Optional[str] = Field(None, min_length=2, max_length=150)
    summary: Optional[str] = Field(None, min_length=5)
    remarks: Optional[str] = None
    status: Optional[ChargesheetStatus] = None

    accused_links: Optional[List[ChargesheetAccusedLinkCreate]] = None
    evidence_links: Optional[List[ChargesheetEvidenceLinkCreate]] = None
    section_links: Optional[List[ChargesheetSectionLinkCreate]] = None


class ChargesheetAccusedDetail(BaseModel):
    """Response detail for associated accused."""
    accused_id: str
    accused_name: Optional[str] = None
    charges_summary: Optional[str] = None


class ChargesheetEvidenceDetail(BaseModel):
    """Response detail for associated evidence."""
    evidence_id: str
    evidence_number: Optional[str] = None
    title: Optional[str] = None
    relevance_notes: Optional[str] = None


class ChargesheetSectionDetail(BaseModel):
    """Response detail for associated act section."""
    section_id: str
    section_number: Optional[str] = None
    offence_details: Optional[str] = None


class ChargesheetResponse(BaseModel):
    """Detailed response schema for a chargesheet."""
    model_config = ConfigDict(from_attributes=True)

    chargesheet_id: str
    case_master_id: str
    chargesheet_number: str
    filing_date: datetime
    investigating_officer: str
    summary: str
    remarks: Optional[str] = None
    status: ChargesheetStatus
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    accused: List[ChargesheetAccusedDetail] = []
    evidence: List[ChargesheetEvidenceDetail] = []
    sections: List[ChargesheetSectionDetail] = []


class ChargesheetSummary(BaseModel):
    """Summary schema for chargesheet list views."""
    model_config = ConfigDict(from_attributes=True)

    chargesheet_id: str
    case_master_id: str
    chargesheet_number: str
    filing_date: datetime
    investigating_officer: str
    status: ChargesheetStatus


class ChargesheetListResponse(BaseModel):
    """Paginated list response for chargesheets."""
    items: List[ChargesheetResponse]
    pagination: PaginationMeta
