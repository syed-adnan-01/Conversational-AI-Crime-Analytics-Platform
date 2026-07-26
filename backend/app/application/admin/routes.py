from fastapi import APIRouter,Depends
from app.auth.permissions import require_roles
from app.core.roles import UserRole
from app.models.user import User
from .service import AdminService
router=APIRouter(); service=AdminService()
def admin(current_user:User=Depends(require_roles(UserRole.ADMIN))): return current_user
@router.get('/users',summary='List users')
def users(current_user:User=Depends(admin)): return service.users()
@router.get('/officers',summary='List officers')
def officers(current_user:User=Depends(admin)): return service.officers()
@router.get('/roles',summary='List roles')
def roles(current_user:User=Depends(admin)): return service.roles()
@router.get('/departments',summary='List departments')
def departments(current_user:User=Depends(admin)): return service.departments()
@router.get('/audit',summary='List application audit records')
def audit(current_user:User=Depends(admin)): return service.audit()
