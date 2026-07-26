"""
Workflow Data Models for AI Orchestrator.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.ai.llm.llm_models import LLMResponse
from app.ai.prompting.prompt_models import PromptResponse, PromptPersona


class OrchestrationRequest(BaseModel):
    """Input request for the AI Orchestrator end-to-end pipeline."""
    model_config = ConfigDict(from_attributes=True)

    case_id: str = Field(..., description="Target Case Master ID")
    query: str = Field(..., description="User query or analysis directive")
    persona: PromptPersona = Field(PromptPersona.INVESTIGATOR, description="AI Persona profile")
    provider: Optional[str] = Field(None, description="Optional LLM provider override (quickml, gemini, etc.)")
    conversation_id: Optional[str] = Field(None, description="Multi-turn conversation session ID")
    output_schema: Optional[str] = Field(None, description="Target Pydantic schema for structured output")


class OrchestrationResult(BaseModel):
    """Output result returned by the AI Orchestrator pipeline."""
    model_config = ConfigDict(from_attributes=True)

    orchestration_id: str
    case_id: str
    query: str
    prompt_response: PromptResponse
    llm_response: LLMResponse
    parsed_output: Optional[Dict[str, Any]] = None
    execution_time_ms: float = 0.0
