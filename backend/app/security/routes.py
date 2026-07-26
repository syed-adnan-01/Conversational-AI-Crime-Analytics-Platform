from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from .models import SecurityRequest
from .security_service import SecurityService
router = APIRouter(); _service = SecurityService()
@router.post('/policies/evaluate')
def policies(body: SecurityRequest, current_user: User = Depends(get_current_user)): return _service.inspect(body)
@router.post('/redaction')
def redaction(body: SecurityRequest, current_user: User = Depends(get_current_user)): return _service.inspect(body).masked_text
@router.get('/audits')
def audits(current_user: User = Depends(get_current_user)): return _service.audit.entries
@router.get('/metrics')
def metrics(current_user: User = Depends(get_current_user)): return _service.metrics.value
@router.get('/rate-limits')
def rate_limits(current_user: User = Depends(get_current_user)): return {'per_user_limit': _service.config.user_limit}
@router.get('/quotas')
def quotas(current_user: User = Depends(get_current_user)): return {'status': 'configured externally'}
@router.get('/health')
def health(): return _service.health()
