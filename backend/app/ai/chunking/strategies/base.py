"""
============================================================
Base Chunk Strategy Interface
============================================================

Module  : AI Chunking Engine
Purpose : Defines abstract strategy interface for context chunkers.
"""

from abc import ABC, abstractmethod

from app.ai.chunking.chunk_models import ContextChunk
from app.ai.context.context_models import InvestigationContext


class BaseChunkStrategy(ABC):
    """
    Abstract strategy for transforming InvestigationContext into ordered ContextChunks.
    """

    @abstractmethod
    def build_chunks(self, context: InvestigationContext) -> list[ContextChunk]:
        """
        Build and return ordered list of ContextChunk objects from context.
        """
        pass
