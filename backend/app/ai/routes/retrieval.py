"""
============================================================
AI Retrieval API Routes
============================================================

Module  : AI Retrieval Engine
Purpose : Exposes REST API endpoints for candidate retrieval,
          prompt context assembly, and step-by-step debug traces.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.ai.retrieval.retrieval_models import (
    RetrievalContext,
    SearchQuery,
    SearchResult,
)
from app.ai.retrieval.retrieval_service import RetrievalService
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


# ==============================================================
# POST /ai/retrieve — Candidate Search Retrieval
# ==============================================================

@router.post(
    "",
    response_model=SearchResult,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Investigative Chunks",
    description=(
        "Executes multi-stage retrieval across indexed case vectors. "
        "Returns top matching chunks with confidence scores, citations, and metrics. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Chunks retrieved successfully."},
        401: {"description": "Unauthorized user."},
    },
)
async def retrieve_chunks(
    query: SearchQuery,
    current_user: User = Depends(get_current_user),
) -> SearchResult:
    """Retrieve candidate investigation chunks."""
    return RetrievalService.retrieve(query, user_id=str(current_user.employee_id))


# ==============================================================
# POST /ai/retrieve/context — Assembled LLM Prompt Context
# ==============================================================

@router.post(
    "/context",
    response_model=RetrievalContext,
    status_code=status.HTTP_200_OK,
    summary="Assemble LLM Prompt Context",
    description=(
        "Executes retrieval pipeline and formats a fully assembled, token-budgeted "
        "RetrievalContext with structured prompt sections ready for LLM consumption. "
        "Supports policy selection (LegalPolicy, EvidencePolicy, TimelinePolicy, InvestigationPolicy). "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Context assembled successfully."},
        401: {"description": "Unauthorized user."},
    },
)
async def retrieve_context(
    query: SearchQuery,
    policy: Optional[str] = Query(default=None, description="Domain policy (Legal, Evidence, Timeline, Investigation)"),
    current_user: User = Depends(get_current_user),
) -> RetrievalContext:
    """Assemble token-budgeted RetrievalContext for LLMs."""
    return RetrievalService.retrieve_context(query, policy_name=policy, user_id=str(current_user.employee_id))


# ==============================================================
# POST /ai/retrieve/debug — Pipeline Execution Trace
# ==============================================================

@router.post(
    "/debug",
    status_code=status.HTTP_200_OK,
    summary="Multi-Stage Retrieval Debug Trace",
    description=(
        "Development & audit endpoint returning complete step-by-step pipeline execution trace "
        "including query normalization, expansion, intent classification, policy selection, "
        "raw candidates, reranked chunks, compressed chunks, and timings. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Debug trace generated successfully."},
        401: {"description": "Unauthorized user."},
    },
)
async def retrieve_debug(
    query: SearchQuery,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Generate multi-stage pipeline execution trace for debugging."""
    return RetrievalService.retrieve_debug(query, user_id=str(current_user.employee_id))
