"""Minimal user-administration facade over the existing user repository."""
from fastapi import APIRouter, Depends
from app.auth.permissions import require_roles
from app.core.roles import UserRole
from app.models.user import User

router = APIRouter()

@router.get("/")
def list_users(current_user: User = Depends(require_roles(UserRole.ADMIN))):
    return {
        "items": [],
        "total": 0,
        "detail": "TODO: the current public user repository does not expose a list operation.",
    }
