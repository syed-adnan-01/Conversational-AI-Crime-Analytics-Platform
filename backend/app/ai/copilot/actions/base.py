"""
Abstract Base Action Class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionMetadata, ActionResult


class BaseAction(ABC):
    """Abstract interface for all Copilot Actions."""

    @property
    @abstractmethod
    def metadata(self) -> ActionMetadata:
        """Returns ActionMetadata description."""
        pass

    @abstractmethod
    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        """Executes action logic and returns standardized ActionResult."""
        pass
