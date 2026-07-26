"""
Workspace Models including pinned context, notes, drafts, and versioning.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PinnedContext(BaseModel):
    """Pinned investigation entities explicitly prioritized by the investigator."""
    model_config = ConfigDict(from_attributes=True)

    pinned_evidence: List[str] = Field(default_factory=list, description="Pinned Evidence IDs")
    pinned_witnesses: List[str] = Field(default_factory=list, description="Pinned Witness IDs")
    pinned_accused: List[str] = Field(default_factory=list, description="Pinned Accused IDs")
    pinned_timeline: List[str] = Field(default_factory=list, description="Pinned Timeline Event IDs")
    pinned_sections: List[str] = Field(default_factory=list, description="Pinned Legal Act Sections")


class WorkspaceMetadata(BaseModel):
    """Session workspace metadata."""
    model_config = ConfigDict(from_attributes=True)

    case_id: str
    lead_officer_id: Optional[str] = None
    investigation_stage: str = "INITIAL_INQUIRY"
    current_objective: str = "Gather primary case facts and evidence overview"


class CopilotWorkspace(BaseModel):
    """
    Workspace model storing active case, pinned context, notes, drafts, reports, and checklists.
    Includes workspace_version, created_at, and updated_at for persistence synchronization.
    """
    model_config = ConfigDict(from_attributes=True)

    workspace_id: str
    session_id: str
    workspace_version: int = 1
    metadata: WorkspaceMetadata
    pinned_context: PinnedContext = Field(default_factory=PinnedContext)
    notes: List[str] = Field(default_factory=list)
    drafts: Dict[str, str] = Field(default_factory=dict)
    saved_prompts: List[str] = Field(default_factory=list)
    checklist: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        self.workspace_version += 1
        self.updated_at = datetime.now(timezone.utc)
