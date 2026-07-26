from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
class DashboardSummary(BaseModel): total_cases:int; open_cases:int; closed_cases:int; pending_cases:int; investigation_completion_percent:float; evidence_uploaded:int; officers_assigned:int
class RecentCase(BaseModel): case_id:str; case_number:Optional[str]=None; fir:str; district:Optional[str]=None; officer:Optional[str]=None; priority:Optional[str]=None; status:Optional[str]=None; created_date:datetime; risk_score:Optional[float]=None
