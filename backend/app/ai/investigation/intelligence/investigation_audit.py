"""Investigation audit trail."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    case_id: str | None
    detail: str
    timestamp: datetime


class InvestigationAudit:
    """In-memory audit log."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event_type: str, case_id: str | None, detail: str) -> None:
        self._events.append(AuditEvent(event_type=event_type, case_id=case_id, detail=detail, timestamp=datetime.now(timezone.utc)))

    def list(self) -> list[AuditEvent]:
        return list(self._events)

    def count(self) -> int:
        return len(self._events)
