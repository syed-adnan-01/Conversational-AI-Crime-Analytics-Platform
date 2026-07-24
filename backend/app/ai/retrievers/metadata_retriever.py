"""
============================================================
Metadata Retriever
============================================================

Module  : AI Retrievers Subsystem
Purpose : Metadata-filtered candidate retrieval strategy.
"""

from typing import Optional

from app.ai.retrieval.exceptions import RetrieverException
from app.ai.retrieval.retrieval_models import RetrievedChunk, SearchQuery
from app.ai.retrievers.base import BaseRetriever
from app.ai.retrievers.semantic_retriever import SemanticRetriever


class MetadataRetriever(BaseRetriever):
    """
    Retriever applying strict metadata filtering criteria before similarity scoring.
    """

    def __init__(self, semantic_retriever: Optional[SemanticRetriever] = None):
        self.semantic_retriever = semantic_retriever or SemanticRetriever()

    @property
    def retriever_name(self) -> str:
        return "MetadataRetriever"

    def retrieve(self, query: SearchQuery) -> list[RetrievedChunk]:
        try:
            chunks = self.semantic_retriever.retrieve(query)
            filtered: list[RetrievedChunk] = []

            for chunk in chunks:
                meta = chunk.metadata or {}

                # Entity type filter
                if query.filters.entity_type and meta.get("entity_type") != query.filters.entity_type:
                    continue

                # Status filter
                if query.filters.status and meta.get("status") != query.filters.status:
                    continue

                # Officer filter
                if query.filters.officer and meta.get("officer") != query.filters.officer:
                    continue

                filtered.append(chunk)

            return filtered

        except Exception as exc:
            raise RetrieverException(self.retriever_name, str(exc)) from exc
