"""
============================================================
Semantic Chunk Strategy
============================================================

Module  : AI Chunking Engine
Purpose : Chunks InvestigationContext using configurable token windowing
          and semantic paragraph splitting.
"""

from app.ai.chunking.chunk_models import ChunkMetadata, ChunkType, ContextChunk
from app.ai.chunking.strategies.base import BaseChunkStrategy
from app.ai.config import ai_config
from app.ai.context.context_models import DetailLevel, InvestigationContext
from app.ai.context.serializers import InvestigationContextSerializer


class SemanticChunkStrategy(BaseChunkStrategy):
    """
    Token-window semantic chunking strategy. Breaks the full text representation
    of an InvestigationContext into overlapping passages based on MAX_CHUNK_TOKENS
    and CHUNK_OVERLAP_TOKENS.
    """

    def __init__(
        self,
        max_chunk_tokens: int = ai_config.MAX_CHUNK_TOKENS,
        chunk_overlap_tokens: int = ai_config.CHUNK_OVERLAP_TOKENS,
    ):
        self.max_chunk_tokens = max_chunk_tokens
        self.chunk_overlap_tokens = chunk_overlap_tokens

    def build_chunks(self, context: InvestigationContext) -> list[ContextChunk]:
        chunks: list[ContextChunk] = []
        case_id = context.metadata.case_id
        context_hash = context.metadata.context_hash

        # Extract full plain text representation
        full_text = InvestigationContextSerializer.to_text(context, level=DetailLevel.DETAILED)
        words = full_text.split()

        if not words:
            return chunks

        step = max(1, self.max_chunk_tokens - self.chunk_overlap_tokens)
        chunk_idx = 0

        for i in range(0, len(words), step):
            chunk_words = words[i : i + self.max_chunk_tokens]
            chunk_text = " ".join(chunk_words)

            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-SEM-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.CASE,
                    parent_entity_id=case_id,
                    parent_chunk_id=None,
                    content=chunk_text,
                    token_estimate=len(chunk_words),
                    metadata=ChunkMetadata(
                        entity_type="SemanticPassage",
                        entity_id=case_id,
                        custom_attributes={
                            "word_start": i,
                            "word_end": i + len(chunk_words),
                            "max_tokens": self.max_chunk_tokens,
                            "overlap_tokens": self.chunk_overlap_tokens,
                        },
                    ),
                )
            )
            chunk_idx += 1

        return chunks
