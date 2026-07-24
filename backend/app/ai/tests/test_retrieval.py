"""
============================================================
AI RAG Retrieval Engine Test Suite
============================================================

Module  : AI Retrieval Engine
Purpose : Unit & Integration tests for query processing, retrievers, rerankers,
          compressors, budget manager, context assembly, policies, evaluation metrics,
          and FastAPI REST endpoints.
"""

from fastapi.testclient import TestClient

from app.ai.compressors import SummaryCompressor
from app.ai.context_assembly import ContextAssembler, PromptBudgetManager
from app.ai.evaluation import RetrievalMetrics
from app.ai.indexing.indexing_service import IndexingService
from app.ai.query_processing import QueryClassifier, QueryExpander, QueryNormalizer
from app.ai.rerankers import DiversityReranker, ScoreReranker
from app.ai.retrieval.retrieval_models import (
    RetrievalFilter,
    RetrievalMode,
    SearchQuery,
)
from app.ai.retrieval.retrieval_pipeline import RetrievalPipeline
from app.ai.retrieval.retrieval_policies import EvidencePolicy, LegalPolicy
from app.ai.retrieval.retrieval_service import RetrievalService
from app.ai.retrievers import HybridRetriever, MetadataRetriever, SemanticRetriever
from app.ai.tests.test_context_builder import clear_all_repositories, setup_sample_case_data
from app.main import app


def test_query_processing():
    """Verify Normalizer, Expander, and Classifier."""
    norm = QueryNormalizer.normalize("  What   WEAPON was used?  ")
    assert norm == "what weapon was used?"

    expanded = QueryExpander.expand("knife")
    assert "weapon" in expanded
    assert "blade" in expanded

    legal_intent = QueryClassifier.classify_intent("Which IPC section applies to fraud?")
    assert legal_intent.value == "LEGAL_QUERY"

    policy = QueryClassifier.resolve_policy(legal_intent)
    assert policy.policy_name == "LegalPolicy"


def test_retrievers_and_rerankers():
    """Verify SemanticRetriever, HybridRetriever, and Rerankers."""
    case_id = setup_sample_case_data()
    IndexingService.index_case(case_id)

    sq = SearchQuery(
        query="Server Logs transaction receipts digital device",
        top_k=5,
        filters=RetrievalFilter(case_id=case_id),
    )

    # 1. Semantic Retriever
    sem_ret = SemanticRetriever()
    chunks1 = sem_ret.retrieve(sq)
    assert len(chunks1) > 0

    # 2. Hybrid Retriever
    hyb_ret = HybridRetriever()
    chunks2 = hyb_ret.retrieve(sq)
    assert len(chunks2) > 0

    # 3. Score Reranker
    score_reranker = ScoreReranker()
    reranked = score_reranker.rerank(sq.query, chunks2)
    assert len(reranked) > 0
    assert reranked[0].overall_confidence > 0.0
    assert reranked[0].citation.source_reference is not None

    # 4. Diversity Reranker
    div_reranker = DiversityReranker(max_per_type=2)
    div_chunks = div_reranker.rerank(sq.query, chunks2)
    assert len(div_chunks) > 0


def test_context_assembly_and_budget():
    """Verify ContextAssembler and PromptBudgetManager."""
    case_id = setup_sample_case_data()
    IndexingService.index_case(case_id)

    sq = SearchQuery(
        query="Case details evidence witness statement",
        top_k=10,
        filters=RetrievalFilter(case_id=case_id),
    )

    retriever = HybridRetriever()
    chunks = retriever.retrieve(sq)

    # Budget manager allocation
    kept, compressed, discarded = PromptBudgetManager.allocate_budget(chunks, max_tokens=150)
    assert len(kept) + len(compressed) <= len(chunks)

    # Context Assembly
    context = ContextAssembler.assemble("investigation summary", chunks, max_token_budget=2048)
    assert context.version == "1.0.0"
    assert "=== SYSTEM CONTEXT ===" in context.assembled_text
    assert context.provenance.context_hash != ""


def test_retrieval_evaluation_metrics():
    """Verify RetrievalMetrics calculation."""
    retrieved = ["EVI-001", "EVI-002", "SEC-420", "WIT-001"]
    relevant = {"EVI-001", "EVI-002"}

    p_at_2 = RetrievalMetrics.precision_at_k(retrieved, relevant, k=2)
    assert p_at_2 == 1.0

    r_at_2 = RetrievalMetrics.recall_at_k(retrieved, relevant, k=2)
    assert r_at_2 == 1.0

    mrr = RetrievalMetrics.mean_reciprocal_rank(retrieved, relevant)
    assert mrr == 1.0


def test_retrieval_pipeline_and_policies():
    """Verify RetrievalPipeline execution trace and policy overrides."""
    case_id = setup_sample_case_data()
    IndexingService.index_case(case_id)

    sq = SearchQuery(
        query="recovery of stolen phone and sharp knife weapon",
        mode=RetrievalMode.COMPREHENSIVE,
        filters=RetrievalFilter(case_id=case_id),
    )

    pipeline = RetrievalPipeline(policy=EvidencePolicy())
    search_res, context, trace = pipeline.run_pipeline(sq)

    assert search_res.total_found > 0
    assert context.token_count > 0
    assert trace.policy_used == "EvidencePolicy"
    assert "retrieval_ms" in trace.timings_ms


def test_retrieval_api_endpoints():
    """Verify REST API endpoints under /ai/retrieve."""
    clear_all_repositories()
    case_id = setup_sample_case_data()
    IndexingService.index_case(case_id)

    client = TestClient(app)

    with client as c:
        # Authenticate user
        login_res = c.post(
            "/auth/login",
            json={"employee_id": "EMP001", "password": "password123", "department": "Cyber Crime"},
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. POST /ai/retrieve
        ret_res = c.post(
            "/ai/retrieve",
            json={
                "query": "financial fraud IPC 420 section",
                "top_k": 5,
                "filters": {"case_id": case_id},
            },
            headers=headers,
        )
        assert ret_res.status_code == 200
        assert ret_res.json()["total_found"] > 0

        # 2. POST /ai/retrieve/context
        ctx_res = c.post(
            "/ai/retrieve/context?policy=LegalPolicy",
            json={
                "query": "criminal conspiracy section 120B and fraud",
                "filters": {"case_id": case_id},
            },
            headers=headers,
        )
        assert ctx_res.status_code == 200
        assert "=== LEGAL & CHARGESHEET ===" in ctx_res.json()["assembled_text"]

        # 3. POST /ai/retrieve/debug
        dbg_res = c.post(
            "/ai/retrieve/debug",
            json={
                "query": "stolen phone weapon evidence",
                "filters": {"case_id": case_id},
            },
            headers=headers,
        )
        assert dbg_res.status_code == 200
        assert "trace" in dbg_res.json()
        assert dbg_res.json()["trace"]["raw_query"] == "stolen phone weapon evidence"
