"""
============================================================
Section Domain Model
============================================================

Module  : Act & Section Management
Entity  : Section
Source   : Police FIR System ER Diagram (Primary Source of Truth)
Author  : CrimeSphere AI Architecture Team
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Section(BaseModel):
    """
    Domain entity representing a Section under a specific Act.
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Identifier (System-generated PK)
    section_id: Optional[str] = None

    # Foreign Key to Act (Required, never allow orphan sections)
    act_id: str

    # Section Details
    section_number: str
    title: str
    description: Optional[str] = None
    is_cognizable: bool = True
    is_bailable: bool = True
    maximum_punishment: Optional[str] = None

    # Audit Fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
