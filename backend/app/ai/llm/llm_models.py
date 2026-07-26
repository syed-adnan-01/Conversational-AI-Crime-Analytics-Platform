"""
Pydantic Data Models for LLM Gateway Requests, Responses, and Token Usage.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.ai.prompting.prompt_models import PromptResponse


class TokenUsage(BaseModel):
    """Token consumption metrics for an LLM execution."""
    model_config = ConfigDict(from_attributes=True)

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMRequest(BaseModel):
    """Input request model for the LLM Gateway."""
    model_config = ConfigDict(from_attributes=True)

    request_id: Optional[str] = Field(None, description="Unique Gateway request ID")
    prompt: Optional[str] = Field(None, description="User prompt string")
    system_prompt: Optional[str] = Field(None, description="Optional system instruction string")
    prompt_response: Optional[PromptResponse] = Field(None, description="Optional Phase 3.4 PromptResponse object")
    provider: Optional[str] = Field(None, description="Target provider (quickml, gemini, openai, claude, mock)")
    model: Optional[str] = Field(None, description="Target model ID")
    temperature: Optional[float] = Field(0.2, description="Sampling temperature")
    top_p: Optional[float] = Field(0.95, description="Nucleus sampling parameter")
    max_output_tokens: Optional[int] = Field(2048, description="Maximum output token ceiling")
    response_schema: Optional[str] = Field(None, description="Target Pydantic schema name for structured JSON output")
    conversation_id: Optional[str] = Field(None, description="Multi-turn conversation session ID")
    stream: bool = Field(False, description="Enable real-time streaming output")
    provider_hints: Optional[Dict[str, Any]] = Field(None, description="Provider parameter overrides")
    tools: Optional[List[Dict[str, Any]]] = Field(None, description="Function/tool definitions list")


class LLMResponse(BaseModel):
    """Complete built response model returned by the LLM Gateway."""
    model_config = ConfigDict(from_attributes=True)

    response_id: str = Field(..., description="Unique response ID")
    request_id: str = Field(..., description="Correlated request ID")
    provider: str = Field(..., description="Executing provider name")
    model: str = Field(..., description="Model version used")
    content: str = Field(..., description="Raw text response content")
    parsed_output: Optional[Dict[str, Any]] = Field(None, description="Parsed structured JSON output object")
    citations: List[str] = Field(default_factory=list, description="Document evidence citations")
    finish_reason: str = Field("STOP", description="Completion status (STOP, LENGTH, SAFETY)")
    latency_ms: float = Field(0.0, description="Execution latency in milliseconds")
    token_usage: TokenUsage = Field(default_factory=TokenUsage, description="Token consumption metrics")
    cost: float = Field(0.0, description="Estimated execution cost in USD")
    cached: bool = Field(False, description="Whether response was returned from cache")
    safety_passed: bool = Field(True, description="Whether output passed safety verification")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
