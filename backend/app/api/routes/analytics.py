"""Read-only dashboard analytics derived from the public case service."""
from collections import Counter
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.case_service import CaseService

router = APIRouter()

@router.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user)):
    cases = CaseService.get_all_cases()
    statuses = Counter(str(case.case_status_id) for case in cases)
    return {
        "total_cases": len(cases),
        "status_counts": dict(statuses),
        "recent_cases": [case.model_dump(mode="json") for case in sorted(cases, key=lambda item: item.crime_registered_date, reverse=True)[:10]],
        "alerts": [],  # TODO: notifications are not persisted by the current domain.
        "trends": [],  # TODO: a date-aggregation source is not available in the public service.
    }
