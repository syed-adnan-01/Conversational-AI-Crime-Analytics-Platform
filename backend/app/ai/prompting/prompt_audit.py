"""
Prompt Audit Logger linking retrieval traces, prompt IDs, and downstream LLM operations.
"""

from datetime import datetime, timezone
from typing import Any, List
from pydantic import BaseModel, ConfigDict, Field


class PromptAuditEntry(BaseModel):
    """Audit entry model for prompt generation activities."""
    model_config = ConfigDict(from_attributes=True)

    prompt_id: str
    prompt_fingerprint: str
    template_name: str
    version: str
    persona: str
    profile: str
    intent: str
    context_hash: str | None = None
    retrieval_id: str | None = None
    estimated_tokens: int
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    quality_score: float


class PromptAuditTrail:
    """In-memory audit logger for tracking prompt creation events."""

    _entries: List[PromptAuditEntry] = []

    @classmethod
    def record(cls, entry: PromptAuditEntry) -> None:
        """Appends an entry to the audit log."""
        cls._entries.append(entry)

    @classmethod
    def get_entries(cls, limit: int = 100) -> List[PromptAuditEntry]:
        """Returns recent audit entries."""
        return cls._entries[-limit:]

    @classmethod
    def clear(cls) -> None:
        """Clears audit logs (useful for testing)."""
        cls._entries.clear()
