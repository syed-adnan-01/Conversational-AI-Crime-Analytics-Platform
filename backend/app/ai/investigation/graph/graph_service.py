"""Graph service facade."""

from __future__ import annotations

from importlib import import_module


class GraphService:
    """Public facade for relationship graph generation."""

    def __init__(self, engine=None):
        engine_cls = import_module("app.ai.investigation.intelligence.investigation_engine").InvestigationEngine
        self.engine = engine or engine_cls()

    def build(self, case_id: str):
        return self.engine.build_graph(case_id)
