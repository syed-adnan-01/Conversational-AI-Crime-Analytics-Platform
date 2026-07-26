"""
Direct LLM Planning Strategy.
"""

from typing import Optional
from app.ai.copilot.copilot_models import ExecutionPlan, ExecutionStep
from app.ai.copilot.planner.base import BasePlanningStrategy


class DirectLLMStrategy(BasePlanningStrategy):
    """Fallback planning strategy for general conversational queries."""

    @property
    def strategy_name(self) -> str:
        return "DIRECT_LLM"

    def evaluate(self, query: str, context: Optional[dict] = None) -> Optional[ExecutionPlan]:
        return ExecutionPlan(
            plan_id="PLAN-DIRECT",
            selected_strategy=self.strategy_name,
            confidence=0.80,
            reason="General conversational query.",
            steps=[
                ExecutionStep(step_name="direct_generation", action_type="GENERATE", description="Direct LLM prompt generation"),
            ],
        )
