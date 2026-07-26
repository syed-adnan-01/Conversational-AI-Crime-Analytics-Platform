from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from .continuous.models import BenchmarkSuite, EvaluationRequest
from .continuous.service import EvaluationService
router = APIRouter(); _service = EvaluationService()
@router.post('/evaluate')
def evaluate(body: EvaluationRequest, current_user: User = Depends(get_current_user)): return _service.evaluate(body)
@router.post('/benchmark')
def benchmark(body: BenchmarkSuite, current_user: User = Depends(get_current_user)): return _service.benchmark(body)
@router.get('/reports')
def reports(current_user: User = Depends(get_current_user)): return _service.report()
@router.get('/metrics')
def metrics(current_user: User = Depends(get_current_user)): return _service.metrics.snapshot()
@router.get('/datasets')
def datasets(current_user: User = Depends(get_current_user)): return _service.datasets.names()
@router.get('/leaderboard')
def leaderboard(current_user: User = Depends(get_current_user)): return _service.leaderboard()
@router.get('/health')
def health(): return _service.health()
