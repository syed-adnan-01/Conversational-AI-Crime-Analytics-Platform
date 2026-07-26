"""
Abstract Base Skill Class.
A Skill orchestrates multiple actions to achieve a domain goal.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult


class BaseSkill(ABC):
    """Abstract base class for Copilot Skills."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        pass
