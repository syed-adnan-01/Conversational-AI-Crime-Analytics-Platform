"""
============================================================
AI Prompt Engine API Routes
============================================================

Module  : AI Prompt Engine
Purpose : Exposes REST API endpoints for building LLM prompts,
          previewing prompts, and inspecting personas, templates, and metrics.
"""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status

from app.ai.prompting.prompt_models import (
    PromptRequest,
    PromptResponse,
    PromptVersion,
)
from app.ai.prompting.prompt_service import PromptService
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
_prompt_service = PromptService()


@router.post(
    "",
    response_model=PromptResponse,
    status_code=status.HTTP_200_OK,
    summary="Build Provider-Independent LLM Prompt",
    description="Builds an optimized, token-budgeted prompt ready for Gemini / QuickML gateway consumption.",
)
async def build_prompt(
    request: PromptRequest,
    current_user: User = Depends(get_current_user),
) -> PromptResponse:
    """Builds a complete PromptResponse object."""
    return _prompt_service.build_prompt(request)


@router.post(
    "/preview",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Preview Prompt Text and Metadata",
    description="Returns raw system prompt, user prompt, and estimated metrics without caching.",
)
async def preview_prompt(
    request: PromptRequest,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Generates raw prompt preview."""
    return _prompt_service.preview_prompt(request)


@router.get(
    "/templates",
    response_model=List[Dict[str, str]],
    status_code=status.HTTP_200_OK,
    summary="List Registered Prompt Templates",
)
async def list_templates(
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, str]]:
    """Returns registered prompt template types."""
    return _prompt_service.list_templates()


@router.get(
    "/personas",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="List Supported AI Personas",
)
async def list_personas(
    current_user: User = Depends(get_current_user),
) -> List[str]:
    """Returns supported AI Personas."""
    return _prompt_service.list_personas()


@router.get(
    "/profiles",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="List Supported Workflow Profiles",
)
async def list_profiles(
    current_user: User = Depends(get_current_user),
) -> List[str]:
    """Returns supported workflow profiles."""
    return _prompt_service.list_profiles()


@router.get(
    "/intents",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="List Supported Prompt Intents",
)
async def list_intents(
    current_user: User = Depends(get_current_user),
) -> List[str]:
    """Returns supported prompt intents."""
    return _prompt_service.list_intents()


@router.get(
    "/versions",
    response_model=List[PromptVersion],
    status_code=status.HTTP_200_OK,
    summary="List Available Template Versions",
)
async def list_versions(
    current_user: User = Depends(get_current_user),
) -> List[PromptVersion]:
    """Returns template versions and compatibility metadata."""
    return _prompt_service.list_versions()


@router.get(
    "/metrics",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get Prompt Engine Operational Metrics",
)
async def get_metrics(
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Returns prompt engine operational performance metrics."""
    return _prompt_service.get_metrics()


@router.delete(
    "/cache",
    status_code=status.HTTP_200_OK,
    summary="Clear Prompt Cache",
)
async def clear_cache(
    current_user: User = Depends(get_current_user),
) -> Dict[str, str]:
    """Clears in-memory prompt cache."""
    _prompt_service.clear_cache()
    return {"status": "success", "message": "Prompt cache cleared."}
