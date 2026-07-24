"""
============================================================
AI Layer Settings Configuration
============================================================

Module  : AI Intelligence Layer
Purpose : Configurable settings for Embedding Providers, Vector Stores,
          Chunk Strategies, and Token parameters.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AIConfig(BaseSettings):
    """
    Configuration settings for AI Embedding & Vector Indexing subsystems.
    Providers and strategies can be swapped without code changes.
    """
    EMBEDDING_PROVIDER: str = "mock"  # "gemini" | "mock"
    VECTOR_STORE_PROVIDER: str = "mock"  # "chromadb" | "mock"
    CHUNK_STRATEGY: str = "section"  # "section" | "semantic"
    
    # Token Window Parameters
    MAX_CHUNK_TOKENS: int = 512
    CHUNK_OVERLAP_TOKENS: int = 64
    
    # Provider Specific Credentials & Parameters
    GEMINI_API_KEY: str = ""
    EMBEDDING_MODEL_NAME: str = "text-embedding-004"
    EMBEDDING_DIMENSIONS: int = 768
    CHROMA_PERSIST_DIR: str = "./data/chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_ai_config() -> AIConfig:
    return AIConfig()


ai_config = get_ai_config()
