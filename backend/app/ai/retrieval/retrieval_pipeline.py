"""
============================================================
Retrieval Pipeline Orchestrator
============================================================

Module  : AI Retrieval Engine
Purpose : Multi-stage retrieval pipeline orchestrator connecting query processing,
          retrievers, metadata filters, rerankers, compressors, plugins,
          context assembly, audit events, and trace logs.
"""

import time
import uuid
from typing import Optional

from app.ai.compressors.base import BaseCompressor
from app.ai.compressors.summary_compressor import SummaryCompressor
from app.ai.context_assembly.assembler import ContextAssembler
from app.ai.query_processing import QueryClassifier, QueryExpander, QueryNormalizer
from app.ai.rerankers import BaseReranker, DiversityReranker, ScoreReranker
from app.ai.retrieval.audit_events import RetrievalAuditEvent
from app.ai.retrieval.plugins import BaseRetrievalPlugin
from app.ai.retrieval.retrieval_models import (
    QueryIntent,
    RetrievalContext,
    RetrievalMode,
    RetrievalStatistics,
    RetrievedChunk,
    SearchQuery,
    SearchResult,
)
from app.ai.retrieval.retrieval_policies import BaseRetrievalPolicy, InvestigationPolicy
from app.ai.retrieval.retrieval_statistics import RetrievalStatisticsTracker
from app.ai.retrieval.retrieval_trace import RetrievalTrace
from app.ai.retrievers import BaseRetriever, HybridRetriever, MetadataRetriever, SemanticRetriever


class RetrievalPipeline:
    """
    Central Multi-Stage Retrieval Pipeline orchestrator.
    """

    def __init__(
        self,
        plugins: Optional[list[BaseRetrievalPlugin]] = None,
        retriever: Optional[BaseRetriever] = None,
        reranker: Optional[BaseReranker] = None,
        compressor: Optional[BaseCompressor] = None,
        policy: Optional[BaseRetrievalPolicy] = None,
    ):
        self.plugins = plugins or []
        self.retriever = retriever
        self.reranker = reranker
        self.compressor = compressor or SummaryCompressor()
        self.policy = policy or InvestigationPolicy()

    def run_pipeline(
        self, query: SearchQuery, user_id: Optional[str] = None
    ) -> tuple[SearchResult, RetrievalContext, RetrievalTrace]:
        """
        Execute multi-stage retrieval pipeline.
        Returns (SearchResult, RetrievalContext, RetrievalTrace).
        """
        start_total = time.perf_counter()
        q_id = f"Q-{uuid.uuid4().hex[:8]}"
        r_id = f"RET-{uuid.uuid4().hex[:8]}"
        timings: dict[str, float] = {}

        # 1. Plugin before_retrieve
        for plugin in self.plugins:
            query = plugin.before_retrieve(query)

        # 2. Query processing
        norm_query = QueryNormalizer.normalize(query.query)
        expanded_query = QueryExpander.expand(norm_query)
        intent = QueryClassifier.classify_intent(norm_query)

        active_policy = self.policy
        if not self.policy or isinstance(self.policy, InvestigationPolicy):
            active_policy = QueryClassifier.resolve_policy(intent)

        # 3. Select Retriever
        if self.retriever:
            active_retriever = self.retriever
        elif query.mode == RetrievalMode.FAST:
            active_retriever = SemanticRetriever()
        elif intent == QueryIntent.LEGAL_QUERY or query.filters.entity_type:
            active_retriever = MetadataRetriever()
        else:
            active_retriever = HybridRetriever()

        search_q = SearchQuery(
            query=expanded_query,
            query_embedding=query.query_embedding,
            mode=query.mode,
            top_k=query.top_k or active_policy.default_top_k,
            min_similarity=query.min_similarity,
            filters=query.filters,
        )

        # 4. Candidate Retrieval
        start_ret = time.perf_counter()
        raw_chunks = active_retriever.retrieve(search_q)
        ret_time = (time.perf_counter() - start_ret) * 1000
        timings["retrieval_ms"] = round(ret_time, 2)

        # Plugin after_retrieve
        for plugin in self.plugins:
            raw_chunks = plugin.after_retrieve(raw_chunks)

        # 5. Reranking
        start_rerank = time.perf_counter()
        if query.mode == RetrievalMode.FAST:
            active_reranker = ScoreReranker()
        else:
            active_reranker = self.reranker or DiversityReranker()

        reranked_chunks = active_reranker.rerank(norm_query, raw_chunks)
        rerank_time = (time.perf_counter() - start_rerank) * 1000
        timings["rerank_ms"] = round(rerank_time, 2)

        # 6. Compression
        start_comp = time.perf_counter()
        if query.mode == RetrievalMode.COMPREHENSIVE:
            final_chunks = self.compressor.compress(reranked_chunks, max_chunks=search_q.top_k)
        else:
            final_chunks = reranked_chunks[: search_q.top_k]
        comp_time = (time.perf_counter() - start_comp) * 1000
        timings["compression_ms"] = round(comp_time, 2)

        # Plugin before_assembly
        for plugin in self.plugins:
            final_chunks = plugin.before_assembly(final_chunks)

        # 7. Context Assembly
        total_time = (time.perf_counter() - start_total) * 1000
        timings["total_ms"] = round(total_time, 2)

        tracker = RetrievalStatisticsTracker()
        avg_sim = tracker.calculate_average_similarity(final_chunks)

        stats = RetrievalStatistics(
            retrieval_time_ms=round(ret_time, 2),
            rerank_time_ms=round(rerank_time, 2),
            compression_time_ms=round(comp_time, 2),
            total_time_ms=round(total_time, 2),
            chunks_examined=len(raw_chunks),
            chunks_returned=len(final_chunks),
            average_similarity=avg_sim,
        )

        context = ContextAssembler.assemble(
            query=norm_query,
            chunks=final_chunks,
            max_token_budget=active_policy.max_token_budget,
            statistics=stats,
            query_id=q_id,
            retrieval_id=r_id,
        )

        # Plugin after_assembly
        for plugin in self.plugins:
            context = plugin.after_assembly(context)

        # 8. Create SearchResult
        search_result = SearchResult(
            query=norm_query,
            intent=intent,
            chunks=final_chunks,
            total_found=len(final_chunks),
            statistics=stats,
        )

        # 9. Audit Event & Trace
        audit_event = RetrievalAuditEvent(
            query_id=q_id,
            user_id=user_id,
            case_id=query.filters.case_id,
            query_text=norm_query,
            chunks_retrieved_count=len(final_chunks),
            duration_ms=round(total_time, 2),
        )
        audit_event.log_event()

        trace = RetrievalTrace(
            query_id=q_id,
            raw_query=query.query,
            normalized_query=norm_query,
            expanded_query=expanded_query,
            classified_intent=intent.value,
            policy_used=active_policy.policy_name,
            retriever_used=active_retriever.retriever_name,
            reranker_used=active_reranker.reranker_name,
            compressor_used=self.compressor.compressor_name,
            raw_chunks_count=len(raw_chunks),
            reranked_chunks_count=len(reranked_chunks),
            compressed_chunks_count=len(final_chunks),
            chosen_chunk_ids=[c.chunk_id for c in final_chunks],
            timings_ms=timings,
        )

        return search_result, context, trace
