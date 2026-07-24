"""
============================================================
AI Indexing API Routes
============================================================

Module  : AI Indexing Subsystem
Purpose : Exposes REST API endpoints for case indexing, status checks,
          rebuilding, deletion, index listing, and semantic search.
"""

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status

from app.ai.indexing.background_tasks import run_background_indexing
from app.ai.indexing.index_models import (
    IndexListResponse,
    IndexMetadata,
    IndexStatus,
)
from app.ai.indexing.indexing_service import IndexingService
from app.ai.vector_store.vector_models import (
    VectorSearchRequest,
    VectorSearchResult,
)
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


# ==============================================================
# GET /ai/index — List Operational Index Metadata
# ==============================================================

@router.get(
    "",
    response_model=IndexListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Operational Index Metadata",
    description=(
        "Retrieve operational metadata and vector metrics across all indexed cases. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Index metadata list retrieved successfully."},
        401: {"description": "Unauthorized user."},
    },
)
async def list_indexes(
    current_user: User = Depends(get_current_user),
) -> IndexListResponse:
    """List operational index status across all cases."""
    return IndexingService.list_indexes()


# ==============================================================
# POST /ai/index/search — Plain Text & Vector Search
# (Must be declared before /{case_id} route)
# ==============================================================

@router.post(
    "/search",
    response_model=list[VectorSearchResult],
    status_code=status.HTTP_200_OK,
    summary="Semantic Search Over Indexed Case Vectors",
    description=(
        "Internal semantic search endpoint. Accepts plain text queries ('query') "
        "or pre-computed vectors ('query_vector') and returns matching chunks with scores. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Search completed successfully."},
        401: {"description": "Unauthorized user."},
    },
)
async def search_index(
    request: VectorSearchRequest,
    current_user: User = Depends(get_current_user),
) -> list[VectorSearchResult]:
    """Execute semantic search over indexed vectors."""
    return IndexingService.search(request)


# ==============================================================
# GET /ai/index/{case_id}/status — Get Status
# ==============================================================

@router.get(
    "/{case_id}/status",
    response_model=IndexMetadata,
    status_code=status.HTTP_200_OK,
    summary="Get Case Index Status",
    description=(
        "Retrieve indexing status and metadata for a specified case. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Index status retrieved successfully."},
        401: {"description": "Unauthorized user."},
    },
)
async def get_index_status(
    case_id: str,
    current_user: User = Depends(get_current_user),
) -> IndexMetadata:
    """Get indexing status metadata for a case."""
    return IndexingService.get_status(case_id=case_id)


# ==============================================================
# POST /ai/index/{case_id}/rebuild — Force Rebuild
# ==============================================================

@router.post(
    "/{case_id}/rebuild",
    response_model=IndexMetadata,
    status_code=status.HTTP_200_OK,
    summary="Force Rebuild Case Vector Index",
    description=(
        "Deletes old vectors and forces a complete rebuild of the vector index for a case. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Case index rebuilt successfully."},
        404: {"description": "Case not found."},
        401: {"description": "Unauthorized user."},
    },
)
async def rebuild_index(
    case_id: str,
    current_user: User = Depends(get_current_user),
) -> IndexMetadata:
    """Force rebuild case index."""
    return IndexingService.reindex_case(case_id=case_id)


# ==============================================================
# DELETE /ai/index/{case_id} — Delete Index
# ==============================================================

@router.delete(
    "/{case_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Case Vector Index",
    description=(
        "Deletes all stored vectors and metadata for a specified case. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Case index deleted successfully."},
        401: {"description": "Unauthorized user."},
    },
)
async def delete_index(
    case_id: str,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Delete case vector index."""
    IndexingService.delete_index(case_id=case_id)
    return {"success": True, "message": f"Index for case '{case_id}' deleted successfully."}


# ==============================================================
# POST /ai/index/{case_id} — Build Index
# ==============================================================

@router.post(
    "/{case_id}",
    response_model=IndexMetadata,
    status_code=status.HTTP_200_OK,
    summary="Build or Update Case Vector Index",
    description=(
        "Builds or updates vector index for a specified case. "
        "Skips re-indexing if context_hash matches existing index unless force=true. "
        "Supports optional background execution. Requires authenticated user."
    ),
    responses={
        200: {"description": "Case indexed successfully."},
        404: {"description": "Case not found."},
        401: {"description": "Unauthorized user."},
    },
)
async def index_case(
    case_id: str,
    background_tasks: BackgroundTasks,
    force: bool = Query(default=False, description="Force re-indexing even if context_hash is unchanged"),
    background: bool = Query(default=False, description="Execute indexing as a background task"),
    current_user: User = Depends(get_current_user),
) -> IndexMetadata:
    """Build or update case index."""
    if background:
        background_tasks.add_task(run_background_indexing, case_id, force)
        meta = IndexingService.get_status(case_id)
        meta.status = IndexStatus.INDEXING
        return meta

    return IndexingService.index_case(case_id=case_id, force=force)
