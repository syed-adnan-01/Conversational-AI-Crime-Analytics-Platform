"""
============================================================
Victim Pydantic Schemas
============================================================

Module  : Victim Management
Purpose : Request/Response structures and API contract.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import Gender, IdentificationType
from app.schemas.complainant import PaginationMeta


# ==============================================================
# BASE SCHEMA
# ==============================================================

class VictimBase(BaseModel):
    """
    Shared fields between VictimCreate, VictimUpdate, and VictimResponse.
    """

    gender: Optional[Gender] = Field(
        default=None,
        description="Gender of the victim.",
        examples=[Gender.MALE],
    )
    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150,
        description="Age of the victim.",
        examples=[35],
    )
    address: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Address of the victim.",
        examples=["No 45, 2nd Main, Bengaluru"],
    )
    nationality: Optional[str] = Field(
        default="Indian",
        max_length=50,
        description="Nationality of the victim.",
        examples=["Indian"],
    )
    occupation: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Occupation of the victim.",
        examples=["Business Analyst"],
    )
    id_type: Optional[IdentificationType] = Field(
        default=None,
        description="Type of identification document.",
        examples=[IdentificationType.AADHAAR],
    )
    id_number: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Identification document number.",
        examples=["1234-5678-9012"],
    )


# ==============================================================
# 1. VictimCreate — Registration Request
# ==============================================================

class VictimCreate(VictimBase):
    """
    Schema for registering a new victim.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the victim.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the victim.",
        examples=["9876543210"],
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the victim.",
        examples=["amit.kumar@example.com"],
    )


# ==============================================================
# 2. VictimUpdate — Mutation Request
# ==============================================================

class VictimUpdate(VictimBase):
    """
    Schema for updating an existing victim.
    Every field is optional.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Full name of the victim.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the victim.",
        examples=["9876543210"],
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the victim.",
        examples=["amit.kumar@example.com"],
    )


# ==============================================================
# 3. VictimResponse — Full Detail View
# ==============================================================

class VictimResponse(VictimBase):
    """
    Complete victim record returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    victim_id: str = Field(
        ...,
        description="Unique system-generated identifier for the victim.",
        examples=["VT-A1B2C3D4E5F6"],
    )
    case_master_id: str = Field(
        ...,
        description="ID of the case this victim is associated with.",
        examples=["CM-5065C147B4E7"],
    )
    name: str = Field(
        ...,
        description="Full name of the victim.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the victim.",
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the victim.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the victim record was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the victim record was last updated.",
    )


# ==============================================================
# 4. VictimSummary — Lightweight View
# ==============================================================

class VictimSummary(BaseModel):
    """
    Lightweight summary of a victim, optimized for list views.
    """

    model_config = ConfigDict(from_attributes=True)

    victim_id: str
    case_master_id: str
    name: str
    gender: Optional[Gender] = None
    mobile_no: Optional[str] = None
    id_type: Optional[IdentificationType] = None
    id_number: Optional[str] = None


# ==============================================================
# 5. VictimListResponse — Paginated List
# ==============================================================

class VictimListResponse(BaseModel):
    """Wrapper encapsulating a page of victim summaries and metadata."""

    items: list[VictimSummary] = Field(..., description="Page of victim records.")
    pagination: PaginationMeta = Field(..., description="Pagination state metadata.")


# ==============================================================
# 6. Sorting Enums
# ==============================================================

class VictimSortField(str, Enum):
    """Allowed sort fields for Victims."""

    NAME = "name"
    AGE = "age"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"
