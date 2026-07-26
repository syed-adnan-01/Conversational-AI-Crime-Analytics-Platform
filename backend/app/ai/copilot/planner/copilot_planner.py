"""
Copilot Planner evaluating query intents via registered BasePlanningStrategy objects.
"""

from typing import List, Optional
from app.ai.copilot.copilot_models import ExecutionPlan
from app.ai.copilot.planner.base import BasePlanningStrategy
from app.ai.copilot.planner.direct_llm_strategy import DirectLLMStrategy
from app.ai.copilot.planner.memory_strategy import MemoryStrategy
from app.ai.copilot.planner.rag_strategy import RAGStrategy
from app.ai.copilot.planner.workflow_strategy import WorkflowStrategy


class CopilotPlanner:
    """Intelligent Planner using strategy pattern to evaluate execution plans."""

    _strategies: List[BasePlanningStrategy] = []

    @classmethod
    def _initialize(cls) -> None:
        if not cls._strategies:
            cls._strategies = [
                WorkflowStrategy(),
                MemoryStrategy(),
                RAGStrategy(),
                DirectLLMStrategy(),  # Fallback
            ]

    @classmethod
    def plan(cls, query: str, context: Optional[dict] = None) -> ExecutionPlan:
        """Evaluates strategies in order and returns highest confidence ExecutionPlan."""
        cls._initialize()
        for strategy in cls._strategies:
            plan = strategy.evaluate(query, context)
            if plan:
                return plan
        # Ultimate fallback
        return DirectLLMStrategy().evaluate(query, context)  # type: ignore
