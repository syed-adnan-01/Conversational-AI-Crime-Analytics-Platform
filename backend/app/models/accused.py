"""
============================================================
Accused Domain Model
============================================================

Module  : Accused Management
Entity  : Accused
Source   : Police FIR System ER Diagram (Primary Source of Truth)
Author  : CrimeSphere AI Architecture Team
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.common.enums import Gender, IdentificationType


class Accused(BaseModel):
    """
    Domain entity representing an Accused linked to a CaseMaster record.
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Identifier (System-generated PK)
    accused_id: Optional[str] = None

    # Foreign Key to CaseMaster (Required, never allow orphan accused)
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

    # Identification
    id_type: Optional[IdentificationType] = None
    id_number: Optional[str] = None

    # Audit Fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
