"""
High-Level Workspace Service Facade.
"""

from typing import Optional
from app.ai.copilot.workspace.workspace_manager import WorkspaceManager
from app.ai.copilot.workspace.workspace_models import CopilotWorkspace


class WorkspaceService:
    """Service facade for Workspace operations."""

    @classmethod
    def get_or_create(cls, session_id: str, case_id: str) -> CopilotWorkspace:
        ws = WorkspaceManager.get_workspace(session_id)
        if not ws:
            ws = WorkspaceManager.create_workspace(session_id, case_id)
        return ws

    @classmethod
    def pin_item(cls, session_id: str, entity_type: str, entity_id: str) -> CopilotWorkspace:
        return WorkspaceManager.pin_entity(session_id, entity_type, entity_id)
