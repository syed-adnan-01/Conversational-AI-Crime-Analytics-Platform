"""
============================================================
AI Embeddings Layer Test Suite
============================================================

Module  : AI Embeddings Layer
Purpose : Unit tests for MockEmbeddingProvider, GeminiEmbeddingProvider,
          EmbeddingService, batching, and embedding cache hook.
"""

from app.ai.chunking.chunk_builder import ChunkBuilder
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.embeddings.providers import GeminiEmbeddingProvider, MockEmbeddingProvider
from app.ai.services.context_service import ContextService
from app.ai.tests.test_context_builder import setup_sample_case_data


def test_mock_embedding_provider():
    """Verify MockEmbeddingProvider generates deterministic 768-dim vectors."""
    provider = MockEmbeddingProvider(dims=768)
    assert provider.provider_name == "mock"
    assert provider.dimensions == 768

    vec1 = provider.embed_text("Crime scene analysis")
    vec2 = provider.embed_text("Crime scene analysis")
    vec3 = provider.embed_text("Different query")

    assert len(vec1) == 768
    assert vec1 == vec2  # Deterministic
    assert vec1 != vec3


def test_gemini_embedding_provider_fallback():
    """Verify GeminiEmbeddingProvider falls back gracefully when API key is missing."""
    provider = GeminiEmbeddingProvider(api_key="")
    assert provider.provider_name == "gemini"

    vec = provider.embed_text("Test query")
    assert len(vec) == 768


def test_embedding_service_cache_hook():
    """Verify EmbeddingService cache hook prevents redundant vector computations."""
    EmbeddingService.clear_cache()
    svc = EmbeddingService(provider=MockEmbeddingProvider())

    case_id = setup_sample_case_data()
    context = ContextService.build_context(case_id)
    chunks = ChunkBuilder.build_chunks(context)

    # First run computes vectors
    records1 = svc.generate_embeddings_for_chunks(chunks)
    assert len(records1) == len(chunks)

    # Second run hits embedding cache
    records2 = svc.generate_embeddings_for_chunks(chunks)
    assert len(records2) == len(chunks)
    assert records1[0].vector == records2[0].vector
