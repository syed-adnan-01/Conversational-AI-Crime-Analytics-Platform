"""
Copilot Audit — immutable structured audit log for investigation AI activity.
"""

import threading
from datetime import datetime
from typing import Any, Dict, List, Optional


class AuditEntry:
    __slots__ = ("timestamp", "session_id", "event_type", "actor", "description", "metadata")

    def __init__(
        self,
        session_id: str,
        event_type: str,
        actor: str = "system",
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.timestamp = datetime.utcnow().isoformat()
        self.session_id = session_id
        self.event_type = event_type
        self.actor = actor
        self.description = description
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "event_type": self.event_type,
            "actor": self.actor,
            "description": self.description,
            "metadata": self.metadata,
        }


class CopilotAudit:
    """Thread-safe append-only audit log."""

    _lock = threading.Lock()
    _log: List[AuditEntry] = []

    @classmethod
    def record(
        cls,
        session_id: str,
        event_type: str,
        actor: str = "system",
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        entry = AuditEntry(session_id, event_type, actor, description, metadata)
        with cls._lock:
            cls._log.append(entry)

    @classmethod
    def get_session_log(cls, session_id: str) -> List[Dict[str, Any]]:
        with cls._lock:
            return [e.to_dict() for e in cls._log if e.session_id == session_id]

    @classmethod
    def all_entries(cls) -> List[Dict[str, Any]]:
        with cls._lock:
            return [e.to_dict() for e in cls._log]

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            cls._log.clear()
