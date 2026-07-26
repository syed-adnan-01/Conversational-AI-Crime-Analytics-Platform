"""
FastAPI Router for Enterprise LLM Gateway and AI Orchestrator.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.ai.llm.llm_models import LLMRequest, LLMResponse
from app.ai.llm.llm_service import LLMService
from app.ai.orchestrator.ai_orchestrator import AIOrchestrator
from app.ai.orchestrator.workflow import OrchestrationRequest, OrchestrationResult

router = APIRouter()


@router.post("/generate", response_model=LLMResponse, summary="Generate LLM Output")
def generate_llm(
    request: LLMRequest,
    current_user: User = Depends(get_current_user),
) -> LLMResponse:
    """Invokes LLM provider with caching, retry resiliency, safety validation, and output parsing."""
    try:
        return LLMService.generate(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM Generation failed: {str(e)}",
        ) from e


@router.post("/stream", summary="Stream LLM Output (SSE)")
async def stream_llm(
    request: LLMRequest,
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    """Returns real-time Server-Sent Events (SSE) stream of token chunks."""
    request.stream = True
    return StreamingResponse(
        LLMService.generate_stream_sse(request),
        media_type="text/event-stream",
    )


@router.post("/chat", response_model=OrchestrationResult, summary="Execute AI Orchestrator End-to-End Chat")
def orchestrate_chat(
    request: OrchestrationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrchestrationResult:
    """Executes full pipeline: Retrieval -> Prompt Engine -> LLM Gateway."""
    try:
        return AIOrchestrator.run(db=db, request=request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Orchestration failed: {str(e)}",
        ) from e


@router.get("/providers", response_model=List[str], summary="List Registered Providers")
def list_providers(
    current_user: User = Depends(get_current_user),
) -> List[str]:
    """Returns names of registered LLM providers."""
    return LLMService.get_providers()


@router.get("/capabilities", response_model=Dict[str, Any], summary="Get Provider Capabilities Matrix")
def get_capabilities(
    provider: Optional[str] = Query(None, description="Optional provider identifier (quickml, gemini, etc.)"),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Returns capability matrix and model details for requested or active provider."""
    return LLMService.get_capabilities(provider)


@router.get("/models", response_model=Dict[str, Any], summary="Get Provider Model Info")
def get_models(
    provider: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Returns metadata on available provider models."""
    return LLMService.get_capabilities(provider).get("model_info", {})


@router.get("/health", response_model=Dict[str, str], summary="LLM Gateway Health Check")
def health_check() -> Dict[str, str]:
    """Returns system status of LLM Gateway."""
    return {"status": "HEALTHY", "active_provider": LLMService.get_capabilities().get("provider", "unknown")}


@router.get("/metrics", response_model=Dict[str, Any], summary="Get Gateway Metrics")
def get_metrics(
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Returns snapshot of operational metrics (tokens, latency, cost, cache hit rate)."""
    return LLMService.get_metrics()


@router.delete("/cache", response_model=Dict[str, str], summary="Clear Prompt Response Cache")
def clear_cache(
    current_user: User = Depends(get_current_user),
) -> Dict[str, str]:
    """Clears in-memory prompt response cache."""
    LLMService.clear_cache()
    return {"message": "LLM response cache cleared successfully"}
