"""
============================================================
Complainant Domain Model
============================================================

Module  : Complainant Management
Entity  : Complainant
Source   : Police FIR System ER Diagram (Primary Source of Truth)
Author  : CrimeSphere AI Architecture Team
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.common.enums import Gender


class Complainant(BaseModel):
    """
    Domain entity representing a Complainant linked to a CaseMaster record.
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Identifier (System-generated PK)
    complainant_id: Optional[str] = None

    # Foreign Key to CaseMaster (Required, never allow orphan complainants)
    case_master_id: str

    # Personal Information
    name: str
    gender: Optional[Gender] = None
    age: Optional[int] = None
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    nationality: Optional[str] = None
    occupation: Optional[str] = None

    # Relationship Details
    relationship_type: Optional[str] = None  # e.g., Father, Mother, Victim, Relative
    relative_name: Optional[str] = None      # e.g., Father's name, Husband's name

    # Audit Fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
