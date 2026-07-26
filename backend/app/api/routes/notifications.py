"""Notification API facade; returns an explicit empty state until a source is added."""
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
def list_notifications(current_user: User = Depends(get_current_user)):
    return {"items": [], "total": 0, "detail": "TODO: notification persistence is not implemented by the current backend."}
