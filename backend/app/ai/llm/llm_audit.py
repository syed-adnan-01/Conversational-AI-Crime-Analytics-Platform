"""
LLM Audit Logger tracking execution trails for compliance and security auditing.
"""

from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LLMAuditEntry(BaseModel):
    """Audit entry model for an LLM generation event."""
    model_config = ConfigDict(from_attributes=True)

    request_id: str
    response_id: str
    provider: str
    model: str
    prompt_fingerprint: Optional[str] = None
    conversation_id: Optional[str] = None
    tokens_used: int
    cost_usd: float
    latency_ms: float
    retries: int = 0
    safety_passed: bool = True
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LLMAuditTrail:
    """In-memory audit log manager."""

    _entries: List[LLMAuditEntry] = []

    @classmethod
    def record(cls, entry: LLMAuditEntry) -> None:
        cls._entries.append(entry)

    @classmethod
    def get_entries(cls, limit: int = 100) -> List[LLMAuditEntry]:
        return cls._entries[-limit:]

    @classmethod
    def clear(cls) -> None:
        cls._entries.clear()
