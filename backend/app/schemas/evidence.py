"""
============================================================
Evidence Pydantic Schemas
============================================================

Module  : Evidence Management
Purpose : Request/Response structures and API contract.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.evidence import EvidenceType, EvidenceCategory, EvidenceStatus, CustodyStatus
from app.schemas.complainant import PaginationMeta


# ==============================================================
# BASE SCHEMA
# ==============================================================

class EvidenceBase(BaseModel):
    """
    Shared fields between EvidenceCreate, EvidenceUpdate, and EvidenceResponse.
    """

    evidence_category: Optional[EvidenceCategory] = Field(
        default=None,
        description="Category of the evidence.",
        examples=[EvidenceCategory.DIGITAL],
    )
    custody_status: Optional[CustodyStatus] = Field(
        default=None,
        description="Chain of custody status.",
        examples=[CustodyStatus.IN_CUSTODY],
    )
    storage_key: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Provider-agnostic storage identifier key.",
        examples=["evidence/2026/07/item.png"],
    )
    mime_type: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Mime type of the attached evidence file.",
        examples=["image/png"],
    )
    file_size: Optional[int] = Field(
        default=None,
        ge=0,
        description="Size of the attached evidence file in bytes.",
        examples=[1048576],
    )
    checksum: Optional[str] = Field(
        default=None,
        max_length=128,
        description="Hash checksum of the evidence file.",
        examples=["e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"],
    )
    checksum_algorithm: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Hashing algorithm used for checksum (e.g. SHA-256).",
        examples=["SHA-256"],
    )
    remarks: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional case investigator remarks.",
        examples=["Sealed in standard plastic bag."],
    )


# ==============================================================
# 1. EvidenceCreate — Registration Request
# ==============================================================

class EvidenceCreate(EvidenceBase):
    """
    Schema for registering a new evidence record under a case.
    """

    evidence_number: Optional[str] = Field(
        default=None,
        max_length=100,
        description="User-supplied unique evidence number. System will auto-generate one if not supplied.",
        examples=["EVN-2026-0001"],
    )
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Title of the evidence item.",
        examples=["Redmi Note 12 Smartphone"],
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Detailed description of the evidence item.",
        examples=["Blue smartphone with cracked screen found near back gate."],
    )
    evidence_type: EvidenceType = Field(
        ...,
        description="Type category of the evidence.",
        examples=[EvidenceType.DIGITAL_DEVICE],
    )
    status: EvidenceStatus = Field(
        default=EvidenceStatus.COLLECTED,
        description="System workflow status of the evidence.",
        examples=[EvidenceStatus.COLLECTED],
    )
    collected_by: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name/ID of officer who collected this evidence.",
        examples=["Inspector Sharma"],
    )
    collection_date: datetime = Field(
        ...,
        description="Date and time when the evidence was collected.",
        examples=["2026-07-18T14:30:00"],
    )
    collection_location: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Location from where the evidence was collected.",
        examples=["M.G. Road Metro Station, Bengaluru"],
    )
    storage_location: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Physical repository storage shelf/locker location.",
        examples=["Locker B-4, Malleshwaram Police Station"],
    )

    # Optional references
    victim_id: Optional[str] = Field(
        default=None,
        description="Optional reference ID of associated victim.",
        examples=["VT-A1B2C3D4"],
    )
    accused_id: Optional[str] = Field(
        default=None,
        description="Optional reference ID of associated accused.",
        examples=["AC-X1Y2Z3W4"],
    )
    section_id: Optional[str] = Field(
        default=None,
        description="Optional reference ID of associated legal section.",
        examples=["SEC-IT66D"],
    )


# ==============================================================
# 2. EvidenceUpdate — Mutation Request
# ==============================================================

class EvidenceUpdate(EvidenceBase):
    """
    Schema for updating an existing evidence record. All fields are optional.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=200,
        description="Title of the evidence item.",
    )
    description: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=2000,
        description="Detailed description of the evidence item.",
    )
    evidence_type: Optional[EvidenceType] = Field(
        default=None,
        description="Type category of the evidence.",
    )
    status: Optional[EvidenceStatus] = Field(
        default=None,
        description="System workflow status of the evidence.",
    )
    collected_by: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Name/ID of officer who collected this evidence.",
    )
    collection_date: Optional[datetime] = Field(
        default=None,
        description="Date and time when the evidence was collected.",
    )
    collection_location: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=500,
        description="Location from where the evidence was collected.",
    )
    storage_location: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=500,
        description="Physical repository storage shelf/locker location.",
    )

    # Optional references
    victim_id: Optional[str] = Field(default=None, description="Optional associated victim ID.")
    accused_id: Optional[str] = Field(default=None, description="Optional associated accused ID.")
    section_id: Optional[str] = Field(default=None, description="Optional associated legal section ID.")


# ==============================================================
# 3. EvidenceResponse — Full Detail View
# ==============================================================

class EvidenceResponse(EvidenceBase):
    """
    Complete evidence record returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    evidence_id: str = Field(
        ...,
        description="Unique system-generated identifier for the evidence.",
        examples=["EV-F1G2H3J4K5L6"],
    )
    case_master_id: str = Field(
        ...,
        description="ID of the case this evidence belongs to.",
        examples=["CM-5065C147B4E7"],
    )
    evidence_number: str = Field(
        ...,
        description="Unique evidence number for identification.",
        examples=["EVN-2026-0001"],
    )
    title: str = Field(..., description="Title of the evidence item.")
    description: str = Field(..., description="Detailed description of the evidence item.")
    evidence_type: EvidenceType = Field(..., description="Type of the evidence.")
    status: EvidenceStatus = Field(..., description="Status of the evidence.")
    collected_by: str = Field(..., description="Officer who collected the evidence.")
    collection_date: datetime = Field(..., description="Date and time of collection.")
    collection_location: str = Field(..., description="Location of collection.")
    storage_location: str = Field(..., description="Storage location of physical item.")

    # References
    victim_id: Optional[str] = None
    accused_id: Optional[str] = None
    section_id: Optional[str] = None

    # De-normalized expanded fields for premium API responses
    victim_name: Optional[str] = Field(default=None, description="Expanded victim name.")
    accused_name: Optional[str] = Field(default=None, description="Expanded accused name.")
    section_number: Optional[str] = Field(default=None, description="Expanded section number.")
    act_short_name: Optional[str] = Field(default=None, description="Expanded associated Act short name.")

    created_at: datetime = Field(..., description="Timestamp when evidence record was created.")
    updated_at: datetime = Field(..., description="Timestamp when evidence record was last updated.")


# ==============================================================
# 4. EvidenceSummary — Lightweight List View
# ==============================================================

class EvidenceSummary(BaseModel):
    """
    Lightweight summary of an evidence record optimized for list views.
    """

    model_config = ConfigDict(from_attributes=True)

    evidence_id: str
    case_master_id: str
    evidence_number: str
    title: str
    evidence_type: EvidenceType
    evidence_category: Optional[EvidenceCategory] = None
    status: EvidenceStatus
    custody_status: Optional[CustodyStatus] = None
    collected_by: str
    collection_date: datetime


# ==============================================================
# 5. EvidenceListResponse — Paginated List
# ==============================================================

class EvidenceListResponse(BaseModel):
    """Wrapper encapsulating a page of evidence summaries and metadata."""

    items: list[EvidenceSummary] = Field(..., description="Page of evidence records.")
    pagination: PaginationMeta = Field(..., description="Pagination state metadata.")


# ==============================================================
# 6. Sorting Enums
# ==============================================================

class EvidenceSortField(str, Enum):
    """Allowed sort fields for Evidence."""

    EVIDENCE_NUMBER = "evidence_number"
    TITLE = "title"
    TYPE = "evidence_type"
    STATUS = "status"
    COLLECTION_DATE = "collection_date"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"
