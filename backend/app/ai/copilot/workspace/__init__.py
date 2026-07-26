"""
Copilot Workspace Package.
"""

from app.ai.copilot.workspace.workspace_manager import WorkspaceManager
from app.ai.copilot.workspace.workspace_models import CopilotWorkspace, PinnedContext, WorkspaceMetadata
from app.ai.copilot.workspace.workspace_service import WorkspaceService

__all__ = [
    "CopilotWorkspace",
    "PinnedContext",
    "WorkspaceMetadata",
    "WorkspaceManager",
    "WorkspaceService",
]
