"""
============================================================
Base Retrieval Plugin Interface
============================================================

Module  : AI Retrieval Engine
Purpose : Extensibility hooks for PII masking, jurisdiction filtering,
          safety filtering, and compliance plugins.
"""

from abc import ABC
from app.ai.retrieval.retrieval_models import RetrievalContext, RetrievedChunk, SearchQuery


class BaseRetrievalPlugin(ABC):
    """
    Abstract plugin interface providing life-cycle hooks for retrieval pipeline stages.
    """

    def before_retrieve(self, query: SearchQuery) -> SearchQuery:
        """Hook executed prior to vector retrieval."""
        return query

    def after_retrieve(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """Hook executed immediately after candidate retrieval."""
        return chunks

    def before_assembly(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """Hook executed prior to context assembly & prompt generation."""
        return chunks

    def after_assembly(self, context: RetrievalContext) -> RetrievalContext:
        """Hook executed after context assembly completion."""
        return context
