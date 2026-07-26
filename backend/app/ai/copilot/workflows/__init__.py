"""
Copilot Workflows Package.
"""

from app.ai.copilot.workflows.base import BaseWorkflow
from app.ai.copilot.workflows.workflow_registry import WorkflowRegistry

__all__ = [
    "BaseWorkflow",
    "WorkflowRegistry",
]
