"""
Configuration settings for the Enterprise LLM Gateway.
"""

import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseSettings):
    """Configuration for LLM Providers and Gateway parameters."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Provider defaults (Zoho Catalyst QuickML is primary production default)
    ACTIVE_PROVIDER: str = Field("quickml", description="Default active provider: quickml, gemini, openai, claude, mock")
    DEFAULT_MODEL: str = Field("quickml-rag", description="Default model name for active provider")

    # Generation Parameters
    TEMPERATURE: float = Field(0.2, description="Default sampling temperature")
    TOP_P: float = Field(0.95, description="Default nucleus sampling parameter")
    MAX_OUTPUT_TOKENS: int = Field(2048, description="Maximum token generation ceiling")

    # Resiliency Parameters
    REQUEST_TIMEOUT: float = Field(30.0, description="Provider request timeout in seconds")
    MAX_RETRIES: int = Field(3, description="Maximum backoff retry attempts")

    # Features
    ENABLE_STREAMING: bool = Field(True, description="Global toggle for streaming responses")
    ENABLE_CACHE: bool = Field(True, description="Global toggle for response caching")

    # Provider API Keys & Endpoint URLs
    ZOHO_CATALYST_API_KEY: str = Field(
        default_factory=lambda: os.getenv("ZOHO_CATALYST_API_KEY", "mock_catalyst_key")
    )
    ZOHO_CATALYST_PROJECT_ID: str = Field(
        default_factory=lambda: os.getenv("ZOHO_CATALYST_PROJECT_ID", "crimesphere_catalyst_101")
    )
    GOOGLE_API_KEY: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY", "mock_google_key")
    )
    OPENAI_API_KEY: str = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "mock_openai_key")
    )
    ANTHROPIC_API_KEY: str = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", "mock_anthropic_key")
    )


# Singleton configuration instance
llm_config = LLMConfig()
