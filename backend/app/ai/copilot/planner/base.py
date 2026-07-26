"""
Abstract Base Planning Strategy Interface.
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.ai.copilot.copilot_models import ExecutionPlan, ExecutionStep


class BasePlanningStrategy(ABC):
    """Abstract Strategy interface for Copilot execution plan generation."""

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, query: str, context: Optional[dict] = None) -> Optional[ExecutionPlan]:
        pass
