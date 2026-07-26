from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from .service import AdminService

router = APIRouter()
service = AdminService()


def admin(current_user: User = Depends(get_current_user)):
    """Any authenticated user can access admin panel (role guard can be added later)."""
    return current_user


@router.get('/users', summary='List users')
def users(current_user: User = Depends(admin)):
    return service.users()


@router.get('/officers', summary='List officers')
def officers(current_user: User = Depends(admin)):
    return service.officers()


@router.get('/roles', summary='List roles')
def roles(current_user: User = Depends(admin)):
    return service.roles()


@router.get('/departments', summary='List departments')
def departments(current_user: User = Depends(admin)):
    return service.departments()


@router.get('/audit', summary='List application audit records')
def audit(current_user: User = Depends(admin)):
    return service.audit()
