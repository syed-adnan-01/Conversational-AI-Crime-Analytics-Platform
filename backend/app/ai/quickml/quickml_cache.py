"""In-memory cache for QuickML knowledge-base responses."""

from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from threading import RLock

from app.ai.quickml.quickml_models import QuickMLRetrievalResult


class QuickMLCache:
    _lock = RLock()
    _cache: "OrderedDict[str, QuickMLRetrievalResult]" = OrderedDict()
    _max_size: int = 256

    @classmethod
    def _key(cls, query: str, documents: list[str], case_context: object | None = None) -> str:
        payload = {
            "query": query.strip(),
            "documents": documents,
            "case_context": case_context,
        }
        raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def get(cls, query: str, documents: list[str], case_context: object | None = None) -> QuickMLRetrievalResult | None:
        key = cls._key(query, documents, case_context)
        with cls._lock:
            result = cls._cache.get(key)
            if result is None:
                return None
            
            from datetime import datetime, timezone
            ttl_seconds = 3600 # 1 hour TTL
            if (datetime.now(timezone.utc) - result.created_at).total_seconds() > ttl_seconds:
                del cls._cache[key]
                return None
                
            cls._cache.move_to_end(key)
            return result.model_copy(update={"cached": True})

    @classmethod
    def put(
        cls,
        query: str,
        documents: list[str],
        result: QuickMLRetrievalResult,
        case_context: object | None = None,
    ) -> None:
        key = cls._key(query, documents, case_context)
        with cls._lock:
            cls._cache[key] = result
            cls._cache.move_to_end(key)
            while len(cls._cache) > cls._max_size:
                cls._cache.popitem(last=False)

    @classmethod
    def size(cls) -> int:
        with cls._lock:
            return len(cls._cache)

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            cls._cache.clear()