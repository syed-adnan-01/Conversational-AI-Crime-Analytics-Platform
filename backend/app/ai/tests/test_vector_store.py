"""
============================================================
AI Vector Store Test Suite
============================================================

Module  : AI Vector Store Layer
Purpose : Unit tests for MockVectorStoreProvider, ChromaDBProvider,
          VectorService, upsert, search, delete, and filtering.
"""

from app.ai.chunking.chunk_builder import ChunkBuilder
from app.ai.chunking.chunk_models import ChunkType
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.services.context_service import ContextService
from app.ai.tests.test_context_builder import setup_sample_case_data
from app.ai.vector_store.providers import ChromaDBProvider, MockVectorStoreProvider
from app.ai.vector_store.vector_models import SearchFilter
from app.ai.vector_store.vector_service import VectorService


def test_mock_vector_store_operations():
    """Verify upsert, search, delete, count, and list operations in MockVectorStoreProvider."""
    store = MockVectorStoreProvider()
    case_id = setup_sample_case_data()

    context = ContextService.build_context(case_id)
    chunks = ChunkBuilder.build_chunks(context)
    emb_svc = EmbeddingService()
    records = emb_svc.generate_embeddings_for_chunks(chunks)

    # Upsert
    assert store.upsert(records, chunks) is True
    assert store.exists(case_id) is True
    assert store.count(case_id) == len(chunks)

    # Search with filter
    query_vec = records[0].vector
    sf = SearchFilter(case_id=case_id, chunk_types=[ChunkType.CASE])
    res = store.search(query_vec, filter_criteria=sf, top_k=5)

    assert len(res) > 0
    assert res[0].case_id == case_id
    assert res[0].chunk_type == ChunkType.CASE.value

    # Delete
    assert store.delete(case_id) is True
    assert store.exists(case_id) is False
    assert store.count(case_id) == 0


def test_chromadb_provider_fallback():
    """Verify ChromaDBProvider operations or fallback."""
    provider = ChromaDBProvider()
    assert provider.provider_name == "chromadb"

    case_id = setup_sample_case_data()
    context = ContextService.build_context(case_id)
    chunks = ChunkBuilder.build_chunks(context)
    emb_svc = EmbeddingService()
    records = emb_svc.generate_embeddings_for_chunks(chunks)

    assert provider.upsert(records, chunks) is True
    assert provider.exists(case_id) is True

    query_vec = records[0].vector
    sf = SearchFilter(case_id=case_id)
    res = provider.search(query_vec, filter_criteria=sf, top_k=3)
    assert len(res) > 0

    assert provider.delete(case_id) is True
    assert provider.exists(case_id) is False


def test_vector_service_facade():
    """Verify VectorService facade."""
    service = VectorService(provider=MockVectorStoreProvider())
    case_id = setup_sample_case_data()

    context = ContextService.build_context(case_id)
    chunks = ChunkBuilder.build_chunks(context)
    emb_svc = EmbeddingService()
    records = emb_svc.generate_embeddings_for_chunks(chunks)

    assert service.upsert(records, chunks) is True
    assert service.count(case_id) == len(chunks)
    assert case_id in service.list_all_case_ids()

    service.clear()
    assert service.count() == 0
