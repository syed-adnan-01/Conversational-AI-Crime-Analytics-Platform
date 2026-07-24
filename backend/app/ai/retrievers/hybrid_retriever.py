"""
============================================================
Hybrid Retriever
============================================================

Module  : AI Retrievers Subsystem
Purpose : Hybrid retrieval strategy combining dense vector search
          and sparse keyword matching.
"""

from typing import Optional

from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.retrieval.exceptions import RetrieverException
from app.ai.retrieval.retrieval_models import RetrievedChunk, SearchQuery
from app.ai.retrievers.base import BaseRetriever
from app.ai.retrievers.semantic_retriever import SemanticRetriever
from app.ai.vector_store.vector_service import VectorService


class HybridRetriever(BaseRetriever):
    """
    Retriever combining dense vector search scores with sparse term-frequency keyword matching scores.
    """

    def __init__(
        self,
        semantic_retriever: Optional[SemanticRetriever] = None,
        vector_service: Optional[VectorService] = None,
        embedding_service: Optional[EmbeddingService] = None,
    ):
        self.semantic_retriever = semantic_retriever or SemanticRetriever(
            embedding_service=embedding_service, vector_service=vector_service
        )

    @property
    def retriever_name(self) -> str:
        return "HybridRetriever"

    def _keyword_overlap_score(self, query: str, content: str) -> float:
        """Calculate simple term overlap ratio between query and chunk content."""
        q_words = set(query.lower().split())
        c_words = set(content.lower().split())
        if not q_words or not c_words:
            return 0.0
        overlap = len(q_words.intersection(c_words))
        return round(overlap / len(q_words), 4)

    def retrieve(self, query: SearchQuery) -> list[RetrievedChunk]:
        try:
            # 1. Retrieve candidates via dense vector search
            chunks = self.semantic_retriever.retrieve(query)

            # 2. Re-weight scores with keyword overlap
            hybrid_chunks: list[RetrievedChunk] = []
            for chunk in chunks:
                kw_score = self._keyword_overlap_score(query.query, chunk.content)
                # Hybrid score: 70% vector similarity + 30% keyword match
                hybrid_score = round(0.7 * chunk.similarity_score + 0.3 * kw_score, 4)

                overall_conf = round((hybrid_score + chunk.source_reliability) / 2.0, 4)
                conf_level = "HIGH" if overall_conf >= 0.8 else ("MEDIUM" if overall_conf >= 0.6 else "LOW")

                chunk.rerank_score = hybrid_score
                chunk.retrieval_confidence = hybrid_score
                chunk.overall_confidence = overall_conf
                chunk.confidence_level = conf_level
                hybrid_chunks.append(chunk)

            # Sort descending by hybrid rerank_score
            hybrid_chunks.sort(key=lambda c: c.rerank_score, reverse=True)
            return hybrid_chunks[: query.top_k]

        except Exception as exc:
            raise RetrieverException(self.retriever_name, str(exc)) from exc
