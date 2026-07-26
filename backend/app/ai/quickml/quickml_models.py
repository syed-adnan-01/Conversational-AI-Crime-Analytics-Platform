"""Pydantic models used by QuickML integration."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class QuickMLRetrievalRequest(BaseModel):
    query: str
    documents: list[str] = Field(default_factory=list)


class QuickMLRetrievalResult(BaseModel):
    query: str
    answer: str
    citations: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    latency_ms: int = 0
    cached: bool = False
    documents: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuickMLHealthSnapshot(BaseModel):
    status: str = "ok"
    project_id: str = ""
    configured_documents: list[str] = Field(default_factory=list)
    cache_size: int = 0
    last_query_time: datetime | None = None