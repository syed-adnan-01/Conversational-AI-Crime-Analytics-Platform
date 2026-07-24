"""
============================================================
Semantic Retriever
============================================================

Module  : AI Retrievers Subsystem
Purpose : Semantic vector-based similarity retrieval strategy.
"""

from typing import Optional

from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.retrieval.exceptions import RetrieverException
from app.ai.retrieval.retrieval_models import (
    CitationReference,
    RetrievedChunk,
    SearchQuery,
)
from app.ai.retrievers.base import BaseRetriever
from app.ai.vector_store.vector_models import SearchFilter
from app.ai.vector_store.vector_service import VectorService


class SemanticRetriever(BaseRetriever):
    """
    Retriever executing dense vector similarity search against the vector database.
    """

    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        vector_service: Optional[VectorService] = None,
    ):
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_service = vector_service or VectorService()

    @property
    def retriever_name(self) -> str:
        return "SemanticRetriever"

    def _determine_priority(self, chunk_type: str) -> int:
        priorities = {
            "CASE": 100,
            "SECTION": 95,
            "EVIDENCE": 90,
            "CHARGESHEET": 85,
            "ARREST": 80,
            "COURT": 75,
            "TIMELINE": 70,
            "COMPLAINANT": 65,
            "ACCUSED": 60,
            "VICTIM": 55,
            "WITNESS": 50,
            "OFFICER": 40,
        }
        return priorities.get(chunk_type.upper(), 50)

    def _determine_source_reliability(self, chunk_type: str) -> float:
        # Court, Chargesheet, Evidence have higher reliability than unverified witness statements
        reliabilities = {
            "CASE": 1.0,
            "SECTION": 1.0,
            "CHARGESHEET": 1.0,
            "COURT": 1.0,
            "EVIDENCE": 0.95,
            "ARREST": 0.95,
            "TIMELINE": 0.90,
            "COMPLAINANT": 0.85,
            "ACCUSED": 0.80,
            "WITNESS": 0.75,
        }
        return reliabilities.get(chunk_type.upper(), 0.85)

    def retrieve(self, query: SearchQuery) -> list[RetrievedChunk]:
        try:
            # 1. Compute query vector if not provided
            if query.query_embedding:
                query_vector = query.query_embedding
            else:
                query_vector = self.embedding_service.generate_embedding_for_text(query.query)

            # 2. Build vector store filter
            sf = SearchFilter(
                case_id=query.filters.case_id,
                chunk_types=query.filters.chunk_types,
                metadata_filters=query.filters.custom_filters,
            )

            # 3. Search vector store
            search_results = self.vector_service.search(
                query_vector=query_vector,
                filter_criteria=sf,
                top_k=query.top_k,
            )

            # 4. Map to RetrievedChunk domain model
            chunks: list[RetrievedChunk] = []
            for res in search_results:
                if res.score < query.min_similarity:
                    continue

                source_rel = self._determine_source_reliability(res.chunk_type)
                overall_conf = round((res.score + source_rel) / 2.0, 4)
                conf_level = "HIGH" if overall_conf >= 0.8 else ("MEDIUM" if overall_conf >= 0.6 else "LOW")

                citation = CitationReference(
                    source_reference=f"[{res.chunk_type} #{res.chunk_id}]",
                    entity_name=res.chunk_type,
                    entity_id=res.chunk_id,
                    module="VectorStore",
                )

                chunks.append(
                    RetrievedChunk(
                        chunk_id=res.chunk_id,
                        case_id=res.case_id,
                        chunk_type=res.chunk_type,
                        content=res.content,
                        token_estimate=len(res.content.split()),
                        similarity_score=res.score,
                        rerank_score=res.score,
                        retrieval_confidence=res.score,
                        source_reliability=source_rel,
                        overall_confidence=overall_conf,
                        confidence_level=conf_level,
                        priority=self._determine_priority(res.chunk_type),
                        citation=citation,
                        parent_entity_id=res.parent_entity_id,
                        metadata=res.metadata,
                    )
                )

            return chunks

        except Exception as exc:
            raise RetrieverException(self.retriever_name, str(exc)) from exc
