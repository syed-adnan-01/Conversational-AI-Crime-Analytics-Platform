"""
============================================================
AI Indexing Engine Test Suite
============================================================

Module  : AI Indexing Subsystem
Purpose : Integration tests for IndexManager, hash comparison, skip indexing,
          force rebuild, IndexingService, plain text search API, and endpoints.
"""

from fastapi.testclient import TestClient

from app.ai.chunking.chunk_builder import ChunkBuilder
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.indexing.index_manager import IndexManager
from app.ai.indexing.index_models import IndexStatus
from app.ai.indexing.indexing_service import IndexingService
from app.ai.services.context_service import ContextService
from app.ai.tests.test_context_builder import clear_all_repositories, setup_sample_case_data
from app.ai.vector_store.vector_models import SearchFilter, VectorSearchRequest
from app.ai.vector_store.vector_service import VectorService
from app.main import app
from app.models.evidence import Evidence
from app.repository.evidence_repository import EvidenceRepository


def test_index_manager_lifecycle_and_hash_skipping():
    """Verify IndexManager builds index, skips when context_hash matches, and rebuilds when forced or updated."""
    IndexManager.clear_metadata_store()
    EmbeddingService.clear_cache()

    vector_service = VectorService()
    vector_service.clear()

    manager = IndexManager(vector_service=vector_service)
    case_id = setup_sample_case_data()

    # 1. Initial Indexing
    meta1 = manager.index_case(case_id)
    assert meta1.status == IndexStatus.INDEXED
    assert meta1.chunk_count > 0
    assert meta1.indexing_duration_ms > 0.0
    assert meta1.provider == "mock"
    assert meta1.embedding_version == "1.0.0"

    # 2. Re-indexing with force=False skips redundant work
    meta2 = manager.index_case(case_id, force=False)
    assert meta2.indexed_at == meta1.indexed_at  # Unchanged timestamp

    # 3. Add new evidence to change context_hash
    new_evidence = Evidence(
        evidence_id="EVI-999",
        case_master_id=case_id,
        evidence_number="E-99",
        title="Audio Recording of Extortion",
        description="Audio clip",
        evidence_type="AUDIO",
        status="COLLECTED",
        collected_by="OFF-001",
        collection_date=meta1.indexed_at,
        collection_location="Station",
        storage_location="Locker 9",
    )
    EvidenceRepository.create_evidence(new_evidence)

    # 4. Outdated status detection
    assert manager.is_outdated(case_id) is True

    # 5. Re-indexing picks up context_hash change
    meta3 = manager.index_case(case_id, force=False)
    assert meta3.context_hash != meta1.context_hash
    assert meta3.chunk_count == meta1.chunk_count + 1

    # 6. Force rebuild
    meta4 = manager.index_case(case_id, force=True)
    assert meta4.status == IndexStatus.INDEXED


def test_plain_text_semantic_search():
    """Verify plain-text string search computes query embedding and retrieves relevant chunks."""
    IndexManager.clear_metadata_store()
    case_id = setup_sample_case_data()

    meta = IndexingService.index_case(case_id)
    assert meta.status == IndexStatus.INDEXED

    # Plain text search
    req = VectorSearchRequest(
        query="Server Logs transaction receipts digital device",
        top_k=3,
        filter=SearchFilter(case_id=case_id),
    )

    results = IndexingService.search(req)
    assert len(results) > 0
    assert results[0].case_id == case_id
    assert results[0].score > 0.0


def test_indexing_api_endpoints():
    """Verify REST API endpoints under /ai/index."""
    IndexManager.clear_metadata_store()
    clear_all_repositories()
    client = TestClient(app)

    with client as c:
        # Authenticate user
        login_res = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP001",
                "password": "password123",
                "department": "Cyber Crime",
            },
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create case
        case_res = c.post(
            "/cases/",
            json={"crime_no": "CR-INDEX-99", "crime_registered_date": "2026-07-20T10:00:00", "police_station_id": 1},
            headers=headers,
        )
        assert case_res.status_code == 201
        case_id = case_res.json()["case_master_id"]

        # POST /ai/index/{case_id}
        idx_res = c.post(f"/ai/index/{case_id}", headers=headers)
        assert idx_res.status_code == 200
        assert idx_res.json()["status"] == "INDEXED"

        # GET /ai/index/{case_id}/status
        status_res = c.get(f"/ai/index/{case_id}/status", headers=headers)
        assert status_res.status_code == 200
        assert status_res.json()["status"] == "INDEXED"

        # GET /ai/index (List all indexes)
        list_res = c.get("/ai/index", headers=headers)
        assert list_res.status_code == 200
        assert list_res.json()["total_cases_indexed"] >= 1

        # POST /ai/index/search (Plain text search)
        search_res = c.post(
            "/ai/index/search",
            json={"query": "FIR registered at station", "top_k": 3, "filter": {"case_id": case_id}},
            headers=headers,
        )
        assert search_res.status_code == 200
        assert len(search_res.json()) >= 1

        # POST /ai/index/{case_id}/rebuild
        rebuild_res = c.post(f"/ai/index/{case_id}/rebuild", headers=headers)
        assert rebuild_res.status_code == 200
        assert rebuild_res.json()["status"] == "INDEXED"

        # DELETE /ai/index/{case_id}
        del_res = c.delete(f"/ai/index/{case_id}", headers=headers)
        assert del_res.status_code == 200
        assert del_res.json()["success"] is True
