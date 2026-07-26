"""
Workflow Planning Strategy.
"""

from typing import Optional
from app.ai.copilot.copilot_models import ExecutionPlan, ExecutionStep
from app.ai.copilot.planner.base import BasePlanningStrategy


class WorkflowStrategy(BasePlanningStrategy):
    """Planning strategy for multi-action investigation workflow execution."""

    @property
    def strategy_name(self) -> str:
        return "WORKFLOW_EXECUTION"

    def evaluate(self, query: str, context: Optional[dict] = None) -> Optional[ExecutionPlan]:
        q_lower = query.lower()
        if "chargesheet" in q_lower or "summary report" in q_lower or "legal review" in q_lower:
            return ExecutionPlan(
                plan_id="PLAN-WORKFLOW",
                selected_strategy=self.strategy_name,
                confidence=0.95,
                reason="Query explicitly requests complex investigation workflow execution.",
                steps=[
                    ExecutionStep(step_name="workflow_dispatch", action_type="WORKFLOW", description="Dispatch to registered Workflow"),
                ],
            )
        return None
