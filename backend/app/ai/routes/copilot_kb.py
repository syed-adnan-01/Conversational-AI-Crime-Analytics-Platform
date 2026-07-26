"""QuickML knowledge base routes for Copilot integration."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from app.ai.quickml.knowledge_base_service import knowledge_base_service
from app.ai.quickml.quickml_metrics import QuickMLMetrics

router = APIRouter()


@router.get("/health", summary="QuickML knowledge base health")
def health() -> Dict[str, Any]:
    kb_health = knowledge_base_service.health()
    metrics = QuickMLMetrics.snapshot()
    avg_latency = metrics.get("average_latency_ms", 0)
    
    return {
        "status": "healthy" if kb_health.get("status") == "ok" else "unhealthy",
        "provider": "quickml",
        "documents_loaded": len(kb_health.get("configured_documents", [])),
        "cache": "active" if kb_health.get("cache_size", 0) >= 0 else "inactive",
        "last_query_latency": f"{int(avg_latency)}ms",
        "metrics": {
            "cache_hit_ratio": metrics.get("cache_hits", 0) / max(1, metrics.get("requests", 1)),
            "query_count": metrics.get("requests", 0)
        }
    }