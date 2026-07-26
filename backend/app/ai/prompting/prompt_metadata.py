"""
Helper for building PromptMetadata, generating PRM- prompt IDs, and computing prompt fingerprints.
"""

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any

from app.ai.prompting.prompt_intents import PromptIntent
from app.ai.prompting.prompt_models import PromptMetadata, PromptPersona, PromptType
from app.ai.prompting.prompt_profiles import PromptProfile


class PromptMetadataFactory:
    """Generates unique IDs, SHA-256 prompt fingerprints, and metadata objects."""

    @staticmethod
    def generate_prompt_id() -> str:
        """Generates a standardized PRM- prefixed identifier."""
        return f"PRM-{uuid.uuid4().hex[:8]}"

    @staticmethod
    def generate_fingerprint(
        system_prompt: str,
        user_prompt: str,
        template_version: str,
        persona: str,
        profile: str,
        intent: str,
    ) -> str:
        """Computes SHA-256 fingerprint for prompt deduplication and cache validation."""
        raw_key = f"{system_prompt}|{user_prompt}|{template_version}|{persona}|{profile}|{intent}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    @classmethod
    def create_metadata(
        cls,
        system_prompt: str,
        user_prompt: str,
        prompt_type: PromptType,
        persona: PromptPersona,
        profile: PromptProfile,
        intent: PromptIntent,
        template_name: str,
        version: str,
        estimated_tokens: int,
        quality_score: float = 100.0,
        provider_hints: dict[str, Any] | None = None,
        prompt_id: str | None = None,
    ) -> PromptMetadata:
        """Constructs a complete PromptMetadata object."""
        pid = prompt_id or cls.generate_prompt_id()
        fingerprint = cls.generate_fingerprint(
            system_prompt, user_prompt, version, persona.value, profile.value, intent.value
        )
        return PromptMetadata(
            prompt_id=pid,
            prompt_fingerprint=fingerprint,
            prompt_type=prompt_type,
            persona=persona,
            profile=profile,
            intent=intent,
            template_name=template_name,
            version=version,
            estimated_tokens=estimated_tokens,
            generated_at=datetime.now(timezone.utc),
            quality_score=quality_score,
            provider_hints=provider_hints,
        )
