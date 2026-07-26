"""High-level QuickML knowledge base retrieval service."""

from __future__ import annotations

import json
from typing import Any

from app.ai.quickml.quickml_cache import QuickMLCache
from app.ai.quickml.quickml_client import QuickMLClient
from app.ai.quickml.quickml_config import QuickMLConfig, quickml_config
from app.ai.quickml.quickml_metrics import QuickMLMetrics
from app.ai.quickml.quickml_models import QuickMLHealthSnapshot, QuickMLRetrievalResult


class KnowledgeBaseService:
    def __init__(
        self,
        config: QuickMLConfig | None = None,
        client: QuickMLClient | None = None,
    ) -> None:
        self.config = config or quickml_config
        self.client = client or QuickMLClient(self.config)

    def retrieve(self, query: str, case_context: dict[str, Any] | None = None) -> QuickMLRetrievalResult:
        documents = list(self.config.QUICKML_DOC_IDS)
        if not documents:
            raise RuntimeError("No QuickML documents configured")

        cached = QuickMLCache.get(query, documents, case_context)
        if cached is not None:
            QuickMLMetrics.record_success(cached.latency_ms, cached=True)
            return cached

        enriched_query = self._enrich_query(query, case_context)
        try:
            result = self.client.answer(enriched_query, documents)
        except Exception as exc:
            QuickMLMetrics.record_failure(str(exc))
            raise

        QuickMLCache.put(query, documents, result, case_context)
        QuickMLMetrics.record_success(result.latency_ms, cached=False)
        return result

    def health(self) -> dict[str, Any]:
        snapshot = QuickMLHealthSnapshot(
            project_id=self.config.CATALYST_PROJECT_ID,
            configured_documents=list(self.config.QUICKML_DOC_IDS),
            cache_size=QuickMLCache.size(),
            last_query_time=QuickMLMetrics.last_query_time(),
        )
        return snapshot.model_dump()

    @staticmethod
    def _enrich_query(query: str, case_context: dict[str, Any] | None) -> str:
        if not case_context:
            return query
        context_blob = json.dumps(case_context, sort_keys=True, default=str, ensure_ascii=True)
        return f"{query}\n\nCase context:\n{context_blob}"


knowledge_base_service = KnowledgeBaseService()