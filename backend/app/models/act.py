"""
============================================================
Act Domain Model
============================================================

Module  : Act & Section Management
Entity  : Act
Source   : Police FIR System ER Diagram (Primary Source of Truth)
Author  : CrimeSphere AI Architecture Team
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Act(BaseModel):
    """
    Domain entity representing an Act (e.g. BNS, BNSS, IT Act).
    Act and Section are reference/master data.
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Identifier (System-generated PK)
    act_id: Optional[str] = None

    # Act Details
    name: str
    short_name: str
    year: Optional[int] = None
    description: Optional[str] = None

    # Audit Fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
