"""
Configuration settings for AI Copilot.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CopilotConfig(BaseSettings):
    """Configuration settings for AI Copilot engine, memory, and planner."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SUMMARY_THRESHOLD: int = Field(10, description="Message turn count triggering auto-summarization")
    MEMORY_LIMIT: int = Field(100, description="Maximum stored message turns per session")
    SESSION_TIMEOUT: float = Field(3600.0, description="Session timeout in seconds")
    MAX_MESSAGES: int = Field(50, description="Maximum messages returned in history endpoint")

    AUTO_SUMMARIZE: bool = Field(True, description="Enable automatic conversation summarization")
    ENABLE_MEMORY: bool = Field(True, description="Enable three-tier memory manager")
    ENABLE_PLANNER: bool = Field(True, description="Enable intelligent CopilotPlanner")
    ENABLE_PLUGINS: bool = Field(True, description="Enable Copilot plugin lifecycle execution")
    ENABLE_CACHE: bool = Field(True, description="Enable response caching")


copilot_config = CopilotConfig()
