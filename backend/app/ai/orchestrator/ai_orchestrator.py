"""
AI Orchestrator Facade.
Coordinates end-to-end AI workflows while keeping Retrieval, Prompting, and Gateway decoupled.
"""

from sqlalchemy.orm import Session
from app.ai.orchestrator.pipeline import OrchestrationPipeline
from app.ai.orchestrator.workflow import OrchestrationRequest, OrchestrationResult


class AIOrchestrator:
    """End-to-End AI Orchestrator service facade."""

    @classmethod
    def run(cls, db: Session, request: OrchestrationRequest) -> OrchestrationResult:
        """Executes full multi-stage AI workflow: Retrieval -> Prompt Engine -> LLM Gateway."""
        return OrchestrationPipeline.execute(db, request)
