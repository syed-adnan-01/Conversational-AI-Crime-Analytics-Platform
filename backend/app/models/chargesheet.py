from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ChargesheetStatus(str, Enum):
    """Workflow statuses for chargesheet filing."""
    DRAFT = "DRAFT"
    FILED = "FILED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    SUPPLEMENTARY = "SUPPLEMENTARY"


class ChargesheetAccused(BaseModel):
    """
    Association entity linking a Chargesheet to an Accused.
    """
    model_config = ConfigDict(from_attributes=True)

    chargesheet_id: str
    accused_id: str
    charges_summary: Optional[str] = None
    created_at: Optional[datetime] = None


class ChargesheetEvidence(BaseModel):
    """
    Association entity linking a Chargesheet to Evidence.
    """
    model_config = ConfigDict(from_attributes=True)

    chargesheet_id: str
    evidence_id: str
    relevance_notes: Optional[str] = None
    created_at: Optional[datetime] = None


class ChargesheetSection(BaseModel):
    """
    Association entity linking a Chargesheet to an Act Section.
    """
    model_config = ConfigDict(from_attributes=True)

    chargesheet_id: str
    section_id: str
    offence_details: Optional[str] = None
    created_at: Optional[datetime] = None


class Chargesheet(BaseModel):
    """
    Domain aggregate root entity representing a Chargesheet filed in court.
    """
    model_config = ConfigDict(from_attributes=True)

    chargesheet_id: Optional[str] = None
    case_master_id: str
    chargesheet_number: str
    filing_date: datetime
    investigating_officer: str
    summary: str
    remarks: Optional[str] = None
    status: ChargesheetStatus = ChargesheetStatus.FILED
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
