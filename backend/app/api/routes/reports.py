"""Report API facade. The existing system has no persisted report aggregate yet."""
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
def list_reports(current_user: User = Depends(get_current_user)):
    return {"items": [], "total": 0, "detail": "TODO: report persistence is not implemented by the current backend."}
