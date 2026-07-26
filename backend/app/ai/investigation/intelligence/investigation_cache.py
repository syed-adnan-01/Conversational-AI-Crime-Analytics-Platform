"""Simple in-memory cache for investigation results."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass(slots=True)
class _CacheEntry:
    value: Any
    expires_at: datetime


class InvestigationCache:
    """Very small TTL cache for repeated investigation calls."""

    def __init__(self, ttl_seconds: int = 60):
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, _CacheEntry] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.expires_at < datetime.now(timezone.utc):
            self._store.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = _CacheEntry(value=value, expires_at=datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds))

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        return len(self._store)
