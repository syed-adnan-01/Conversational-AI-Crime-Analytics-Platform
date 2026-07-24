"""
============================================================
Retrieval Audit Events
============================================================

Module  : AI Retrieval Engine
Purpose : Audit logging and event generation for compliance tracking.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.logging import app_logger


class RetrievalAuditEvent(BaseModel):
    """
    Audit event record for compliance and investigation tracking.
    """
    model_config = ConfigDict(from_attributes=True)

    query_id: str
    user_id: Optional[str] = None
    case_id: Optional[str] = None
    query_text: str
    chunks_retrieved_count: int
    duration_ms: float
    timestamp: datetime = Field(default_factory=datetime.now)

    def log_event(self) -> None:
        """Log event to application audit logger."""
        app_logger.info(
            "RetrievalAuditEvent | QueryID=%s | User=%s | CaseID=%s | Chunks=%s | Duration=%.2fms",
            self.query_id,
            self.user_id or "System",
            self.case_id or "Global",
            self.chunks_retrieved_count,
            self.duration_ms,
        )
