from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.ai.decision.decision_models import DecisionRequest
from app.ai.decision.decision_service import DecisionService
router = APIRouter(); _service = DecisionService()
@router.post('/analyze')
def analyze(body: DecisionRequest, current_user: User = Depends(get_current_user)): return _service.analyze(body)
@router.post('/recommendations')
def recommendations(body: DecisionRequest, current_user: User = Depends(get_current_user)): return _service.recommendations(body)
@router.post('/hypotheses')
def hypotheses(body: DecisionRequest, current_user: User = Depends(get_current_user)): return _service.hypotheses(body)
@router.post('/explanation/{recommendation_id}')
def explanation(recommendation_id: str, body: DecisionRequest, current_user: User = Depends(get_current_user)):
    result = _service.explanation(body, recommendation_id)
    if result is None: raise HTTPException(404, 'Recommendation not found')
    return result
@router.post('/confidence')
def confidence(body: DecisionRequest, current_user: User = Depends(get_current_user)): return _service.confidence(body)
@router.get('/audit')
def audit(current_user: User = Depends(get_current_user)): return _service.audit()
@router.get('/metrics')
def metrics(current_user: User = Depends(get_current_user)): return _service.metrics()
@router.get('/health')
def health(): return _service.health()
