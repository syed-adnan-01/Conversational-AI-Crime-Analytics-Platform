"""
============================================================
AI Chunking Engine Test Suite
============================================================

Module  : AI Chunking Engine
Purpose : Unit tests for ChunkBuilder, SectionChunkStrategy,
          SemanticChunkStrategy, typed ChunkMetadata, and parent hierarchy.
"""

from app.ai.chunking.chunk_builder import ChunkBuilder
from app.ai.chunking.chunk_models import ChunkType
from app.ai.chunking.strategies import SectionChunkStrategy, SemanticChunkStrategy
from app.ai.services.context_service import ContextService
from app.ai.tests.test_context_builder import setup_sample_case_data


def test_section_chunk_strategy():
    """Verify SectionChunkStrategy generates ordered chunks with typed metadata and parent IDs."""
    case_id = setup_sample_case_data()
    context = ContextService.build_context(case_id)

    strategy = SectionChunkStrategy()
    chunks = strategy.build_chunks(context)

    assert len(chunks) > 0
    # Case Header chunk is first
    case_chunk = chunks[0]
    assert case_chunk.chunk_type == ChunkType.CASE
    assert case_chunk.case_id == case_id
    assert case_chunk.parent_entity_id == case_id
    assert case_chunk.metadata.entity_type == "CaseMaster"

    # Sub-entity chunks link back to parent_chunk_id
    for chunk in chunks[1:]:
        assert chunk.parent_chunk_id == case_chunk.chunk_id
        assert chunk.metadata.entity_id is not None


def test_semantic_chunk_strategy():
    """Verify SemanticChunkStrategy with custom token window and overlap parameters."""
    case_id = setup_sample_case_data()
    context = ContextService.build_context(case_id)

    strategy = SemanticChunkStrategy(max_chunk_tokens=50, chunk_overlap_tokens=10)
    chunks = strategy.build_chunks(context)

    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.chunk_type == ChunkType.CASE
        assert chunk.token_estimate <= 50
        assert chunk.metadata.entity_type == "SemanticPassage"


def test_chunk_builder():
    """Verify ChunkBuilder delegates to strategy correctly."""
    case_id = setup_sample_case_data()
    context = ContextService.build_context(case_id)

    chunks_sec = ChunkBuilder.build_chunks(context, strategy=SectionChunkStrategy())
    assert any(c.chunk_type == ChunkType.EVIDENCE for c in chunks_sec)

    chunks_sem = ChunkBuilder.build_chunks(context, strategy=SemanticChunkStrategy(max_chunk_tokens=30))
    assert len(chunks_sem) > 0
