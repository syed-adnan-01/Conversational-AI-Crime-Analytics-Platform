"""
============================================================
Prompt Budget Manager
============================================================

Module  : AI Context Assembly Subsystem
Purpose : Priority-aware token budget decision manager (KEEP, COMPRESS, DISCARD).
"""

from typing import Tuple

from app.ai.retrieval.retrieval_models import RetrievedChunk


class PromptBudgetManager:
    """
    Budget manager deciding chunk retention based on token limits and domain priorities.
    """

    @classmethod
    def allocate_budget(
        cls, chunks: list[RetrievedChunk], max_tokens: int
    ) -> Tuple[list[RetrievedChunk], list[RetrievedChunk], list[RetrievedChunk]]:
        """
        Allocate budget across chunks based on priority weight.
        Returns (kept_chunks, compressed_chunks, discarded_chunks).
        """
        # Sort by priority descending, then rerank_score descending
        sorted_chunks = sorted(chunks, key=lambda c: (c.priority, c.rerank_score), reverse=True)

        kept: list[RetrievedChunk] = []
        compressed: list[RetrievedChunk] = []
        discarded: list[RetrievedChunk] = []

        current_tokens = 0

        for chunk in sorted_chunks:
            est_tokens = chunk.token_estimate
            if current_tokens + est_tokens <= max_tokens:
                kept.append(chunk)
                current_tokens += est_tokens
            elif current_tokens + (est_tokens // 2) <= max_tokens:
                # Truncate content in half for compression
                truncated_words = chunk.content.split()[: max(5, est_tokens // 2)]
                chunk.content = " ".join(truncated_words) + "..."
                chunk.token_estimate = len(truncated_words)
                compressed.append(chunk)
                current_tokens += chunk.token_estimate
            else:
                discarded.append(chunk)

        # Restore original rerank score order for kept + compressed
        final_kept = sorted(kept + compressed, key=lambda c: c.rerank_score, reverse=True)
        return final_kept, compressed, discarded
