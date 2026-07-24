"""
============================================================
Chunk Builder
============================================================

Module  : AI Chunking Engine
Purpose : Orchestrates context chunking using selectable strategy algorithms.
"""

from typing import Optional

from app.ai.chunking.chunk_models import ContextChunk
from app.ai.chunking.exceptions import ChunkingException
from app.ai.chunking.strategies import (
    BaseChunkStrategy,
    SectionChunkStrategy,
    SemanticChunkStrategy,
)
from app.ai.config import ai_config
from app.ai.context.context_models import InvestigationContext


class ChunkBuilder:
    """
    Builder responsible for transforming InvestigationContext objects
    into ordered ContextChunk lists using pluggable strategies.
    """

    @classmethod
    def get_default_strategy(cls) -> BaseChunkStrategy:
        """Resolve default strategy based on AIConfig setting."""
        if ai_config.CHUNK_STRATEGY.lower() == "semantic":
            return SemanticChunkStrategy()
        return SectionChunkStrategy()

    @classmethod
    def build_chunks(
        cls,
        context: InvestigationContext,
        strategy: Optional[BaseChunkStrategy] = None,
    ) -> list[ContextChunk]:
        """
        Build chunks for an InvestigationContext.
        """
        try:
            active_strategy = strategy or cls.get_default_strategy()
            return active_strategy.build_chunks(context)
        except Exception as exc:
            raise ChunkingException(
                f"Failed to chunk context for case '{context.metadata.case_id}': {exc}"
            ) from exc
