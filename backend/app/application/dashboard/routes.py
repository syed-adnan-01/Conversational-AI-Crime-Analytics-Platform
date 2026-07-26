from fastapi import APIRouter,Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from .service import DashboardService
router=APIRouter(); service=DashboardService()
@router.get('/summary',summary='Dashboard summary')
def summary(current_user:User=Depends(get_current_user)): return service.summary()
@router.get('/recent-cases',summary='Recent cases')
def recent_cases(current_user:User=Depends(get_current_user)): return service.recent_cases()
@router.get('/trends',summary='Case trends')
def trends(current_user:User=Depends(get_current_user)): return []
@router.get('/alerts',summary='Dashboard alerts')
def alerts(current_user:User=Depends(get_current_user)): return []
@router.get('/ai',summary='Dashboard AI insights')
def ai(current_user:User=Depends(get_current_user)): return []
