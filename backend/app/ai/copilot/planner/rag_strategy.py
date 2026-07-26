"""
RAG Planning Strategy.
"""

from typing import Optional
from app.ai.copilot.copilot_models import ExecutionPlan, ExecutionStep
from app.ai.copilot.planner.base import BasePlanningStrategy


class RAGStrategy(BasePlanningStrategy):
    """Planning strategy for RAG retrieval queries."""

    @property
    def strategy_name(self) -> str:
        return "RAG_RETRIEVAL"

    def evaluate(self, query: str, context: Optional[dict] = None) -> Optional[ExecutionPlan]:
        q_lower = query.lower()
        if any(w in q_lower for w in ["search", "find", "evidence", "witness", "accused", "fir", "case"]):
            return ExecutionPlan(
                plan_id="PLAN-RAG",
                selected_strategy=self.strategy_name,
                confidence=0.92,
                reason="Query contains evidence/case search keywords requiring RAG retrieval.",
                steps=[
                    ExecutionStep(step_name="vector_retrieval", action_type="RETRIEVE", description="Retrieve relevant case chunks"),
                    ExecutionStep(step_name="llm_generation", action_type="GENERATE", description="Generate answer using prompt engine"),
                ],
            )
        return None
