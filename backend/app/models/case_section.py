"""
============================================================
Case Section Association Domain Model
============================================================

Module  : Act & Section Management
Entity  : CaseSectionAssociation
Source   : Police FIR System ER Diagram (Primary Source of Truth)
Author  : CrimeSphere AI Architecture Team
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CaseSectionAssociation(BaseModel):
    """
    Domain entity linking a Section to a CaseMaster record.
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Identifier (System-generated PK)
    association_id: Optional[str] = None

    # Foreign Key references
    case_master_id: str
    section_id: str

    # Optional assignment remarks
    remarks: Optional[str] = None

    # Audit Fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
