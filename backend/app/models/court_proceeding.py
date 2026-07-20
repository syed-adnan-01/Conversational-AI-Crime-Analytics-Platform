from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProceedingStage(str, Enum):
    """Stages of court proceedings."""
    COGNIZANCE = "COGNIZANCE"
    BAIL_HEARING = "BAIL_HEARING"
    CHARGE_FRAMING = "CHARGE_FRAMING"
    EVIDENCE_RECORDING = "EVIDENCE_RECORDING"
    EXAMINATION = "EXAMINATION"
    ARGUMENTS = "ARGUMENTS"
    JUDGMENT = "JUDGMENT"
    SENTENCING = "SENTENCING"
    APPEAL = "APPEAL"


class CourtProceeding(BaseModel):
    """
    Domain entity representing a Court Proceeding record for a Case.
    """

    model_config = ConfigDict(from_attributes=True)

    proceeding_id: Optional[str] = None
    case_master_id: str
    court_name: str
    judge_name: str
    hearing_date: datetime
    stage: ProceedingStage
    summary: str
    order_passed: Optional[str] = None
    next_hearing_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
