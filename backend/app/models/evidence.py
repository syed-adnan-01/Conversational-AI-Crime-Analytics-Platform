"""
============================================================
Evidence Domain Model
============================================================

Module  : Evidence Management
Entity  : Evidence
Source   : Police FIR System ER Diagram (Primary Source of Truth)
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==============================================================
# EVIDENCE ENUMS
# ==============================================================

class EvidenceType(str, Enum):
    """Supported types of evidence."""
    DOCUMENT = "DOCUMENT"
    PHOTO = "PHOTO"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    WEAPON = "WEAPON"
    FINGERPRINT = "FINGERPRINT"
    DNA = "DNA"
    BLOOD_SAMPLE = "BLOOD_SAMPLE"
    DIGITAL_DEVICE = "DIGITAL_DEVICE"
    FORENSIC_REPORT = "FORENSIC_REPORT"
    OTHER = "OTHER"


class EvidenceCategory(str, Enum):
    """Categories of evidence classifying material properties."""
    PHYSICAL = "Physical"
    DIGITAL = "Digital"
    DOCUMENTARY = "Documentary"
    FORENSIC = "Forensic"
    BIOLOGICAL = "Biological"
    OTHER = "Other"


class EvidenceStatus(str, Enum):
    """System-level workflow statuses of evidence."""
    COLLECTED = "COLLECTED"
    SEALED = "SEALED"
    UNDER_ANALYSIS = "UNDER_ANALYSIS"
    SUBMITTED = "SUBMITTED"
    PRESENTED_IN_COURT = "PRESENTED_IN_COURT"
    RETURNED = "RETURNED"
    DISPOSED = "DISPOSED"


class CustodyStatus(str, Enum):
    """Chain of custody / possession statuses of evidence."""
    IN_CUSTODY = "In Custody"
    SEALED = "Sealed"
    RELEASED = "Released"
    DESTROYED = "Destroyed"
    TRANSFERRED = "Transferred"
    OTHER = "Other"


# ==============================================================
# DOMAIN ENTITY
# ==============================================================

class Evidence(BaseModel):
    """
    Domain entity representing Evidence collected during an investigation.
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Identifier
    evidence_id: Optional[str] = None

    # Foreign Keys
    case_master_id: str
    victim_id: Optional[str] = None
    accused_id: Optional[str] = None
    section_id: Optional[str] = None

    # Core Attributes
    evidence_number: str  # Automatically generated if not supplied
    title: str
    description: str
    evidence_type: EvidenceType
    evidence_category: Optional[EvidenceCategory] = None
    status: EvidenceStatus
    custody_status: Optional[CustodyStatus] = None

    # Collection Metadata
    collected_by: str
    collection_date: datetime
    collection_location: str
    storage_location: str

    # Provider-Agnostic Storage Reference & Metadata
    storage_key: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    checksum: Optional[str] = None
    checksum_algorithm: Optional[str] = None

    # Remarks
    remarks: Optional[str] = None

    # Audit Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
