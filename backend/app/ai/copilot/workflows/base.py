"""
Abstract Base Investigation Workflow Class.
A Workflow orchestrates Skills to fulfill an end-to-end domain process.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult


class BaseWorkflow(ABC):
    """Abstract interface for Copilot Workflows."""

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
