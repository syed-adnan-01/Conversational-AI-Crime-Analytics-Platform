"""Service facade for the investigation layer."""

from __future__ import annotations

from app.ai.investigation.intelligence.investigation_engine import InvestigationEngine
from app.ai.investigation.intelligence.investigation_models import InvestigationRequest


class InvestigationService:
    """Public application service consumed by routes and tests."""

    def __init__(self, engine: InvestigationEngine | None = None) -> None:
        self.engine = engine or InvestigationEngine()

    def analyze(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.analyze(request, user_id=user_id)

    def similar(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.similar(request, user_id=user_id)

    def evidence(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.evidence(request, user_id=user_id)

    def timeline(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.timeline(request, user_id=user_id)

    def contradictions(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.contradictions(request, user_id=user_id)

    def recommend(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.recommend(request, user_id=user_id)

    def completeness(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.completeness(request, user_id=user_id)

    def legal(self, request: InvestigationRequest, user_id: str | None = None):
        return self.engine.legal(request, user_id=user_id)

    def build_graph(self, case_id: str):
        return self.engine.build_graph(case_id)

    def metrics(self):
        return self.engine.metrics_snapshot()

    def health(self):
        return self.engine.health()
