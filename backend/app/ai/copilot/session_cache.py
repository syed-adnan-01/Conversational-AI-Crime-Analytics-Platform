"""
Session Cache — LRU-style in-memory session cache for fast copilot state lookup.
"""

import threading
from collections import OrderedDict
from typing import Any, Dict, Optional


class SessionCache:
    """Thread-safe LRU in-memory cache for active session state."""

    def __init__(self, maxsize: int = 512) -> None:
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._maxsize = maxsize
        self._lock = threading.Lock()

    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if session_id in self._cache:
                self._cache.move_to_end(session_id)
                return self._cache[session_id]
        return None

    def set(self, session_id: str, data: Dict[str, Any]) -> None:
        with self._lock:
            if session_id in self._cache:
                self._cache.move_to_end(session_id)
            self._cache[session_id] = data
            if len(self._cache) > self._maxsize:
                self._cache.popitem(last=False)

    def delete(self, session_id: str) -> None:
        with self._lock:
            self._cache.pop(session_id, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        return len(self._cache)
