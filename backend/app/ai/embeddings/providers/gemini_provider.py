"""
============================================================
Gemini Embedding Provider
============================================================

Module  : AI Embeddings Layer
Purpose : Provider implementation using Google Gemini text-embedding-004 model.
"""

from typing import Optional
from app.ai.config import ai_config
from app.ai.embeddings.exceptions import EmbeddingProviderException
from app.ai.embeddings.providers.base import EmbeddingProvider
from app.ai.embeddings.providers.mock_provider import MockEmbeddingProvider


class GeminiEmbeddingProvider(EmbeddingProvider):
    """
    Embedding Provider using Google Gemini API (model: text-embedding-004).
    Fallback to MockEmbeddingProvider if API key is not configured or offline.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = ai_config.EMBEDDING_MODEL_NAME,
        dims: int = ai_config.EMBEDDING_DIMENSIONS,
    ):
        self.api_key = api_key or ai_config.GEMINI_API_KEY
        self.model_name = model_name
        self._dims = dims
        self._fallback_provider = MockEmbeddingProvider(dims=dims)

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def dimensions(self) -> int:
        return self._dims

    def embed_text(self, text: str) -> list[float]:
        if not self.api_key:
            # Graceful fallback when API key is missing
            return self._fallback_provider.embed_text(text)

        try:
            # HTTP/SDK call to Gemini embedding endpoint
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:embedContent?key={self.api_key}"
            payload = {
                "model": f"models/{self.model_name}",
                "content": {"parts": [{"text": text}]},
            }
            res = httpx.post(url, json=payload, timeout=10.0)
            if res.status_code == 200:
                data = res.json()
                return data["embedding"]["values"]
            else:
                return self._fallback_provider.embed_text(text)
        except Exception:
            return self._fallback_provider.embed_text(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]
