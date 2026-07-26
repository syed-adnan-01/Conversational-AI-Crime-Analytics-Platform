from fastapi import APIRouter,Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from .service import DashboardService
router=APIRouter(); service=DashboardService()
@router.get('/summary',summary='Dashboard summary')
def summary(current_user:User=Depends(get_current_user)): return service.summary()
@router.get('/recent-cases',summary='Recent cases')
def recent_cases(current_user:User=Depends(get_current_user)): return service.recent_cases()
import datetime

@router.get('/trends',summary='Case trends')
def trends(current_user:User=Depends(get_current_user)):
    return [
        {"month": "Jan", "active": 120, "resolved": 90},
        {"month": "Feb", "active": 130, "resolved": 95},
        {"month": "Mar", "active": 145, "resolved": 110},
        {"month": "Apr", "active": 160, "resolved": 115},
        {"month": "May", "active": 155, "resolved": 120},
        {"month": "Jun", "active": 170, "resolved": 135}
    ]

@router.get('/alerts',summary='Dashboard alerts')
def alerts(current_user:User=Depends(get_current_user)):
    return [
        {
            "id": "1",
            "title": "High Priority Suspicious Activity",
            "description": "Unusual volume of transactions in sector 4.",
            "severity": "high",
            "time": datetime.datetime.utcnow().isoformat() + "Z",
            "read": False
        },
        {
            "id": "2",
            "title": "Evidence Processing Complete",
            "description": "AI analysis finished for case CR-2026-WIT01.",
            "severity": "info",
            "time": (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).isoformat() + "Z",
            "read": True
        }
    ]

@router.get('/ai',summary='Dashboard AI insights')
def ai(current_user:User=Depends(get_current_user)):
    return [
        {
            "id": "1",
            "title": "Pattern Detected",
            "description": "Similar Modus Operandi found across 3 recent cases.",
            "type": "pattern",
            "confidence": 85,
            "actionable": True
        }
    ]

