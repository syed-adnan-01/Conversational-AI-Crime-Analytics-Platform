"""
============================================================
AI Context API Routes
============================================================

Module  : AI Context Builder
Purpose : Exposes REST API endpoints for accessing AI Investigation
          Context in JSON, Markdown, Text, and Summary formats.
"""

from fastapi import APIRouter, Depends, Query, Response, status

from app.ai.context.context_models import (
    ContextSummary,
    InvestigationContext,
)
from app.ai.services.context_service import ContextService
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


# ==============================================================
# GET /ai/context/{case_id}/summary — Lightweight Summary
# ==============================================================

@router.get(
    "/{case_id}/summary",
    response_model=ContextSummary,
    status_code=status.HTTP_200_OK,
    summary="Get AI Context Summary",
    description=(
        "Retrieve lightweight summary information for a case. "
        "Useful for dashboards, mobile UI, and fast AI routing. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Context summary retrieved successfully."},
        404: {"description": "Case not found."},
        401: {"description": "Unauthorized user."},
    },
)
async def get_context_summary(
    case_id: str,
    current_user: User = Depends(get_current_user),
) -> ContextSummary:
    """Get lightweight context summary."""
    return ContextService.get_summary(case_id)


# ==============================================================
# GET /ai/context/{case_id} — Full / Level-based Context JSON
# ==============================================================

@router.get(
    "/{case_id}",
    response_model=InvestigationContext,
    status_code=status.HTTP_200_OK,
    summary="Get Unified AI Investigation Context",
    description=(
        "Retrieve the complete unified AI context for an investigation. "
        "Aggregates Case, Complainant, Victims, Accused, Witnesses, Sections, "
        "Evidence, Arrests, Chargesheets, Court Proceedings, Officers, and Timeline. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Investigation context retrieved successfully."},
        404: {"description": "Case not found."},
        401: {"description": "Unauthorized user."},
    },
)
async def get_investigation_context(
    case_id: str,
    level: str = Query(
        default="standard",
        description="Detail level: 'summary', 'standard', or 'detailed'",
    ),
    current_user: User = Depends(get_current_user),
) -> InvestigationContext:
    """Get full or level-filtered investigation context object."""
    context = ContextService.build_context(case_id)
    return context


# ==============================================================
# GET /ai/context/{case_id}/markdown — LLM Prompt Markdown
# ==============================================================

@router.get(
    "/{case_id}/markdown",
    response_class=Response,
    status_code=status.HTTP_200_OK,
    summary="Get Investigation Context as Markdown Report",
    description=(
        "Returns the investigation context formatted as structured Markdown, "
        "optimized for LLM system prompts and context windows. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Markdown report generated successfully."},
        404: {"description": "Case not found."},
        401: {"description": "Unauthorized user."},
    },
)
async def get_context_markdown(
    case_id: str,
    level: str = Query(
        default="standard",
        description="Detail level: 'summary', 'standard', or 'detailed'",
    ),
    current_user: User = Depends(get_current_user),
) -> Response:
    """Get Markdown formatted context report."""
    markdown_content = ContextService.get_markdown(case_id, level=level)
    return Response(content=markdown_content, media_type="text/markdown")


# ==============================================================
# GET /ai/context/{case_id}/text — Vector Embedding Text
# ==============================================================

@router.get(
    "/{case_id}/text",
    response_class=Response,
    status_code=status.HTTP_200_OK,
    summary="Get Investigation Context as Plain Text",
    description=(
        "Returns the investigation context formatted as dense plain text, "
        "optimized for vector embedding generation and semantic indexing. "
        "Requires authenticated user."
    ),
    responses={
        200: {"description": "Plain text context generated successfully."},
        404: {"description": "Case not found."},
        401: {"description": "Unauthorized user."},
    },
)
async def get_context_text(
    case_id: str,
    level: str = Query(
        default="standard",
        description="Detail level: 'summary', 'standard', or 'detailed'",
    ),
    current_user: User = Depends(get_current_user),
) -> Response:
    """Get plain text formatted context."""
    text_content = ContextService.get_text(case_id, level=level)
    return Response(content=text_content, media_type="text/plain")
