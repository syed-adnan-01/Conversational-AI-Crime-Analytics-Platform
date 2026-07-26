"""AI Investigation Intelligence REST routes."""

from __future__ import annotations

from importlib import import_module

from fastapi import APIRouter, Depends, status

from app.ai.investigation.intelligence.investigation_models import InvestigationRequest
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
_service = import_module("app.ai.investigation.intelligence.investigation_service").InvestigationService()


def _user_id(current_user: User) -> str:
    return str(getattr(current_user, "employee_id", "unknown"))


@router.post("/analyze", response_model=None, status_code=status.HTTP_200_OK, summary="Run full investigation analysis")
def analyze(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.analyze(body, user_id=_user_id(current_user))


@router.post("/similar", response_model=None, status_code=status.HTTP_200_OK, summary="Find similar cases")
def similar(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.similar(body, user_id=_user_id(current_user))


@router.post("/evidence", response_model=None, status_code=status.HTTP_200_OK, summary="Analyze evidence")
def evidence(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.evidence(body, user_id=_user_id(current_user))


@router.post("/timeline", response_model=None, status_code=status.HTTP_200_OK, summary="Analyze timeline")
def timeline(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.timeline(body, user_id=_user_id(current_user))


@router.post("/contradictions", response_model=None, status_code=status.HTTP_200_OK, summary="Detect contradictions")
def contradictions(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.contradictions(body, user_id=_user_id(current_user))


@router.post("/recommend", response_model=None, status_code=status.HTTP_200_OK, summary="Generate recommendations")
def recommend(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.recommend(body, user_id=_user_id(current_user))


@router.post("/completeness", response_model=None, status_code=status.HTTP_200_OK, summary="Assess completeness")
def completeness(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.completeness(body, user_id=_user_id(current_user))


@router.post("/legal", response_model=None, status_code=status.HTTP_200_OK, summary="Run legal analysis")
def legal(body: InvestigationRequest, current_user: User = Depends(get_current_user)):
    return _service.legal(body, user_id=_user_id(current_user))


@router.get("/graph/{case_id}", response_model=None, status_code=status.HTTP_200_OK, summary="Build case graph")
def graph(case_id: str, current_user: User = Depends(get_current_user)):
    return _service.build_graph(case_id)


@router.get("/metrics", response_model=None, status_code=status.HTTP_200_OK, summary="Investigation metrics")
def metrics():
    return _service.metrics()


@router.get("/health", response_model=None, status_code=status.HTTP_200_OK, summary="Investigation health")
def health():
    return _service.health()
