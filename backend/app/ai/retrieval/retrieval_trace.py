"""
============================================================
Retrieval Trace Log
============================================================

Module  : AI Retrieval Engine
Purpose : Detailed execution trace model capturing step-by-step pipeline state.
"""

from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class RetrievalTrace(BaseModel):
    """
    Complete execution trace of a multi-stage retrieval request for debugging and audit.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    query_id: str
    raw_query: str
    normalized_query: str = ""
    expanded_query: str = ""
    classified_intent: str = "GENERAL"
    policy_used: str = "InvestigationPolicy"
    retriever_used: str = "HybridRetriever"
    reranker_used: str = "ScoreReranker"
    compressor_used: str = "SummaryCompressor"
    raw_chunks_count: int = 0
    reranked_chunks_count: int = 0
    compressed_chunks_count: int = 0
    chosen_chunk_ids: list[str] = Field(default_factory=list)
    timings_ms: dict[str, float] = Field(default_factory=dict)
