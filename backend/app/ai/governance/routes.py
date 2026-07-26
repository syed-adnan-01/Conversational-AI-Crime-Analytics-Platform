from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from .governance_service import GovernanceService
from .models import GovernancePolicy, GovernanceRequest
router = APIRouter(); _service = GovernanceService()
@router.get('/policies')
def policies(current_user: User = Depends(get_current_user)): return _service.policies()
@router.post('/policies')
def add_policy(body: GovernancePolicy, current_user: User = Depends(get_current_user)): _service.add_policy(body); return body
@router.post('/compliance')
def compliance(body: GovernanceRequest, current_user: User = Depends(get_current_user)): return _service.evaluate(body)
@router.get('/audits')
def audits(current_user: User = Depends(get_current_user)): return _service.engine.history
@router.get('/metrics')
def metrics(current_user: User = Depends(get_current_user)): return _service.report()
@router.get('/health')
def health(): return _service.health()
