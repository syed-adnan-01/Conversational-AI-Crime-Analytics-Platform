"""
============================================================
AI Context Service Layer
============================================================

Module  : AI Context Builder
Purpose : Service layer facade providing build, cache hook, and
          serialization capabilities for investigation contexts.
"""

from typing import Optional, Union

from app.ai.context.context_builder import AIContextBuilder
from app.ai.context.context_models import (
    ContextSummary,
    DetailLevel,
    InvestigationContext,
)
from app.ai.context.serializers import InvestigationContextSerializer


class ContextService:
    """
    High-level Service Layer for AI Context operations.
    Supports class-level and instance-level invocations.
    """

    def __init__(self, builder=AIContextBuilder, serializer=InvestigationContextSerializer):
        self.builder = builder
        self.serializer = serializer

    # ----------------------------------------------------------
    # Cache Hook & Context Build
    # ----------------------------------------------------------

    @classmethod
    def get_cached_context(cls, case_id: str) -> Optional[InvestigationContext]:
        """
        Cache lookup hook for future caching implementation (e.g. Redis / In-Memory cache).
        Currently returns None to indicate cache miss.
        """
        return None

    @classmethod
    def build_context(cls, case_id: str) -> InvestigationContext:
        """
        Retrieve or build an InvestigationContext object for a given case_id.
        Checks cache hook first.
        """
        cached = cls.get_cached_context(case_id)
        if cached is not None:
            return cached

        return AIContextBuilder.build_context(case_id)

    @classmethod
    def get_summary(cls, case_id: str) -> ContextSummary:
        """
        Retrieve lightweight ContextSummary for a given case_id.
        """
        context = cls.build_context(case_id)
        return context.summary

    # ----------------------------------------------------------
    # Format Serializations
    # ----------------------------------------------------------

    @classmethod
    def get_json(
        cls,
        case_id: str,
        level: Union[DetailLevel, str] = DetailLevel.STANDARD,
    ) -> str:
        """
        Build context and return machine-readable JSON.
        """
        context = cls.build_context(case_id)
        return InvestigationContextSerializer.to_json(context, level)

    @classmethod
    def get_markdown(
        cls,
        case_id: str,
        level: Union[DetailLevel, str] = DetailLevel.STANDARD,
    ) -> str:
        """
        Build context and return structured Markdown report.
        """
        context = cls.build_context(case_id)
        return InvestigationContextSerializer.to_markdown(context, level)

    @classmethod
    def get_text(
        cls,
        case_id: str,
        level: Union[DetailLevel, str] = DetailLevel.STANDARD,
    ) -> str:
        """
        Build context and return dense plain text for embeddings.
        """
        context = cls.build_context(case_id)
        return InvestigationContextSerializer.to_text(context, level)
