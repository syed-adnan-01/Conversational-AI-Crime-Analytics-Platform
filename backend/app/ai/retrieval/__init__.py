"""
AI Retrieval Package.
"""

from app.ai.retrieval.audit_events import RetrievalAuditEvent
from app.ai.retrieval.exceptions import (
    ContextAssemblyException,
    RerankerException,
    RetrievalException,
    RetrieverException,
)
from app.ai.retrieval.retrieval_models import (
    CitationReference,
    PromptProvenance,
    PromptSections,
    QueryIntent,
    RetrievalContext,
    RetrievalFilter,
    RetrievalMode,
    RetrievalStatistics,
    RetrievedChunk,
    SearchQuery,
    SearchResult,
)
from app.ai.retrieval.retrieval_pipeline import RetrievalPipeline
from app.ai.retrieval.retrieval_policies import (
    BaseRetrievalPolicy,
    EvidencePolicy,
    InvestigationPolicy,
    LegalPolicy,
    TimelinePolicy,
)
from app.ai.retrieval.retrieval_service import RetrievalService

__all__ = [
    "RetrievalAuditEvent",
    "ContextAssemblyException",
    "RerankerException",
    "RetrievalException",
    "RetrieverException",
    "CitationReference",
    "PromptProvenance",
    "PromptSections",
    "QueryIntent",
    "RetrievalContext",
    "RetrievalFilter",
    "RetrievalMode",
    "RetrievalStatistics",
    "RetrievedChunk",
    "SearchQuery",
    "SearchResult",
    "RetrievalPipeline",
    "BaseRetrievalPolicy",
    "EvidencePolicy",
    "InvestigationPolicy",
    "LegalPolicy",
    "TimelinePolicy",
    "RetrievalService",
]
