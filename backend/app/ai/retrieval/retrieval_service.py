"""
============================================================
Retrieval Service Layer
============================================================

Module  : AI Retrieval Engine
Purpose : High-level Service Layer facade for candidate retrieval,
          prompt context assembly, and debug execution.
"""

from typing import Optional

from app.ai.retrieval.retrieval_models import (
    RetrievalContext,
    SearchQuery,
    SearchResult,
)
from app.ai.retrieval.retrieval_pipeline import RetrievalPipeline
from app.ai.retrieval.retrieval_policies import (
    EvidencePolicy,
    InvestigationPolicy,
    LegalPolicy,
    TimelinePolicy,
)


class RetrievalService:
    """
    Service Layer facade executing the Multi-Stage Retrieval Pipeline.
    """

    @classmethod
    def resolve_policy(cls, policy_name: Optional[str]):
        if not policy_name:
            return None
        p = policy_name.lower()
        if "legal" in p:
            return LegalPolicy()
        if "evidence" in p:
            return EvidencePolicy()
        if "timeline" in p:
            return TimelinePolicy()
        return InvestigationPolicy()

    @classmethod
    def retrieve(
        cls, query: SearchQuery, user_id: Optional[str] = None
    ) -> SearchResult:
        """Execute search query and return SearchResult."""
        pipeline = RetrievalPipeline()
        search_result, _, _ = pipeline.run_pipeline(query, user_id=user_id)
        return search_result

    @classmethod
    def retrieve_context(
        cls,
        query: SearchQuery,
        policy_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> RetrievalContext:
        """Execute search query and return assembled RetrievalContext."""
        policy = cls.resolve_policy(policy_name)
        pipeline = RetrievalPipeline(policy=policy)
        _, context, _ = pipeline.run_pipeline(query, user_id=user_id)
        return context

    @classmethod
    def retrieve_debug(
        cls, query: SearchQuery, user_id: Optional[str] = None
    ) -> dict:
        """Execute search query and return full debug trace dictionary."""
        pipeline = RetrievalPipeline()
        search_result, context, trace = pipeline.run_pipeline(query, user_id=user_id)
        return {
            "search_result": search_result.model_dump(mode="json"),
            "retrieval_context": context.model_dump(mode="json"),
            "trace": trace.model_dump(mode="json"),
        }
