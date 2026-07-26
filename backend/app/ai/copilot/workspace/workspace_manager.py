"""
Workspace Manager handling in-memory session workspaces.
"""

from typing import Dict, Optional
from app.ai.copilot.workspace.workspace_models import CopilotWorkspace, PinnedContext, WorkspaceMetadata


class WorkspaceManager:
    """Manages Copilot Workspace state in memory."""

    _workspaces: Dict[str, CopilotWorkspace] = {}

    @classmethod
    def create_workspace(cls, session_id: str, case_id: str) -> CopilotWorkspace:
        ws_id = f"WS-{session_id}"
        workspace = CopilotWorkspace(
            workspace_id=ws_id,
            session_id=session_id,
            metadata=WorkspaceMetadata(case_id=case_id),
        )
        cls._workspaces[session_id] = workspace
        return workspace

    @classmethod
    def get_workspace(cls, session_id: str) -> Optional[CopilotWorkspace]:
        return cls._workspaces.get(session_id)

    @classmethod
    def pin_entity(cls, session_id: str, entity_type: str, entity_id: str) -> CopilotWorkspace:
        ws = cls.get_workspace(session_id)
        if not ws:
            ws = cls.create_workspace(session_id, case_id="CM-DEFAULT")

        if entity_type == "EVIDENCE" and entity_id not in ws.pinned_context.pinned_evidence:
            ws.pinned_context.pinned_evidence.append(entity_id)
        elif entity_type == "WITNESS" and entity_id not in ws.pinned_context.pinned_witnesses:
            ws.pinned_context.pinned_witnesses.append(entity_id)
        elif entity_type == "ACCUSED" and entity_id not in ws.pinned_context.pinned_accused:
            ws.pinned_context.pinned_accused.append(entity_id)
        elif entity_type == "TIMELINE" and entity_id not in ws.pinned_context.pinned_timeline:
            ws.pinned_context.pinned_timeline.append(entity_id)

        ws.touch()
        return ws

    @classmethod
    def clear(cls) -> None:
        cls._workspaces.clear()
