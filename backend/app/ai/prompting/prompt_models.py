"""
Pydantic Data Models and Enums for the Prompt Engine.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.ai.prompting.prompt_intents import PromptIntent
from app.ai.prompting.prompt_profiles import PromptProfile
from app.ai.prompting.prompt_sections import PromptSection
from app.ai.retrieval.retrieval_models import RetrievalContext


class PromptType(str, Enum):
    """Supported prompt task types."""
    SUMMARY = "summary"
    LEGAL_ANALYSIS = "legal_analysis"
    CASE_ANALYSIS = "case_analysis"
    TIMELINE = "timeline"
    CHARGESHEET = "chargesheet"
    REPORT = "report"
    QUESTION_ANSWERING = "question_answering"
    NEXT_STEPS = "next_steps"
    EVIDENCE_ANALYSIS = "evidence_analysis"


class PromptPersona(str, Enum):
    """AI Personas with distinct domain perspectives."""
    INVESTIGATOR = "investigator"
    LEGAL_EXPERT = "legal_expert"
    ANALYST = "analyst"
    SUPERVISOR = "supervisor"


class ConversationTurn(BaseModel):
    """Represents a single turn in a multi-turn conversation context."""
    model_config = ConfigDict(from_attributes=True)

    role: str = Field(..., description="Role of the turn participant e.g. user, assistant, system")
    content: str = Field(..., description="Text content of the conversation turn")
    timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptVersion(BaseModel):
    """Metadata describing a prompt template asset version."""
    model_config = ConfigDict(from_attributes=True)

    version: str = "1.0.0"
    supported_models: list[str] = Field(
        default_factory=lambda: ["gemini-2.5-pro", "gemini-2.5-flash", "quickml", "openai", "claude"]
    )
    min_llm_version: Optional[str] = None
    deprecated: bool = False
    description: str = "Standard prompt template version"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptMetadata(BaseModel):
    """Metadata embedded into every built PromptResponse."""
    model_config = ConfigDict(from_attributes=True)

    prompt_id: str
    prompt_fingerprint: str
    prompt_type: PromptType
    persona: PromptPersona
    profile: PromptProfile
    intent: PromptIntent
    template_name: str
    version: str
    estimated_tokens: int
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    quality_score: float = 100.0
    provider_hints: Optional[dict[str, Any]] = None


class PromptRequest(BaseModel):
    """API Request model for building prompts."""
    model_config = ConfigDict(from_attributes=True)

    query: Optional[str] = Field(None, description="User question or query string")
    retrieval_context: Optional[RetrievalContext] = Field(None, description="Retrieved context object from RAG engine")
    prompt_type: PromptType = Field(PromptType.QUESTION_ANSWERING, description="Task prompt category")
    persona: PromptPersona = Field(PromptPersona.INVESTIGATOR, description="AI Persona role")
    profile: PromptProfile = Field(PromptProfile.POLICE_INVESTIGATION, description="Workflow objective profile")
    intent: PromptIntent = Field(PromptIntent.QUESTION, description="Task intent")
    requested_sections: Optional[list[PromptSection]] = Field(None, description="Optional selective sections")
    conversation_id: Optional[str] = Field(None, description="Optional ID for multi-turn conversation tracking")
    history: Optional[list[ConversationTurn]] = Field(None, description="Optional previous conversation turns")
    output_format: Optional[str] = Field("text", description="Target output format: text or json")
    version: Optional[str] = Field("1.0.0", description="Target template version string")
    max_token_budget: Optional[int] = Field(4096, description="Token budget ceiling for prompt assembly")
    language: str = Field("en", description="Target language code e.g. en, kn, hi")
    locale: str = Field("en_IN", description="Target locale string e.g. en_IN")
    provider_name: str = Field("gemini", description="Target LLM provider profile name")
    provider_hints: Optional[dict[str, Any]] = Field(None, description="Optional LLM Gateway parameter hints")
    tools: Optional[list[dict[str, Any]]] = Field(None, description="Reserved for tool/function calling definitions")
    tool_instructions: Optional[str] = Field(None, description="Reserved for tool execution instructions")
    available_functions: Optional[list[str]] = Field(None, description="Reserved for function names list")


class PromptResponse(BaseModel):
    """Complete built prompt output ready for downstream LLM gateway consumption."""
    model_config = ConfigDict(from_attributes=True)

    system_prompt: str
    user_prompt: str
    metadata: PromptMetadata
    debug: Optional[dict[str, Any]] = None
    trace: Optional[dict[str, Any]] = None
