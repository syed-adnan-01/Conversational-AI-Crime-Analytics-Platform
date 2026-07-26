"""
Memory Planning Strategy.
"""

from typing import Optional
from app.ai.copilot.copilot_models import ExecutionPlan, ExecutionStep
from app.ai.copilot.planner.base import BasePlanningStrategy


class MemoryStrategy(BasePlanningStrategy):
    """Planning strategy for conversation recall and history lookup queries."""

    @property
    def strategy_name(self) -> str:
        return "MEMORY_LOOKUP"

    def evaluate(self, query: str, context: Optional[dict] = None) -> Optional[ExecutionPlan]:
        q_lower = query.lower()
        if any(w in q_lower for w in ["earlier", "previously", "remember", "we discussed", "what did i ask"]):
            return ExecutionPlan(
                plan_id="PLAN-MEMORY",
                selected_strategy=self.strategy_name,
                confidence=0.90,
                reason="Query asks for recall of previous session history or memory.",
                steps=[
                    ExecutionStep(step_name="memory_lookup", action_type="MEMORY", description="Recall turns from three-tier memory"),
                ],
            )
        return None
