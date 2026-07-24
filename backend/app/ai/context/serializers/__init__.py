"""
============================================================
Context Serializers Package & Facade
============================================================

Module  : AI Context Builder
Purpose : Exports serializer strategy implementations and unified
          InvestigationContextSerializer facade.
"""

from typing import Union

from app.ai.context.context_models import DetailLevel, InvestigationContext
from app.ai.context.serializers.base import BaseSerializer
from app.ai.context.serializers.json_serializer import JSONSerializer
from app.ai.context.serializers.markdown_serializer import MarkdownSerializer
from app.ai.context.serializers.text_serializer import TextSerializer


def _parse_level(level: Union[DetailLevel, str]) -> DetailLevel:
    if isinstance(level, DetailLevel):
        return level
    try:
        return DetailLevel(level.lower())
    except Exception:
        return DetailLevel.STANDARD


class InvestigationContextSerializer:
    """
    Facade providing simple static entry points for serializing InvestigationContext.
    """

    _json_serializer = JSONSerializer()
    _markdown_serializer = MarkdownSerializer()
    _text_serializer = TextSerializer()

    @classmethod
    def to_json(
        cls,
        context: InvestigationContext,
        level: Union[DetailLevel, str] = DetailLevel.STANDARD,
    ) -> str:
        """Serialize context to JSON string."""
        lvl = _parse_level(level)
        return cls._json_serializer.serialize(context, lvl)

    @classmethod
    def to_markdown(
        cls,
        context: InvestigationContext,
        level: Union[DetailLevel, str] = DetailLevel.STANDARD,
    ) -> str:
        """Serialize context to Markdown report string."""
        lvl = _parse_level(level)
        return cls._markdown_serializer.serialize(context, lvl)

    @classmethod
    def to_text(
        cls,
        context: InvestigationContext,
        level: Union[DetailLevel, str] = DetailLevel.STANDARD,
    ) -> str:
        """Serialize context to plain text embedding string."""
        lvl = _parse_level(level)
        return cls._text_serializer.serialize(context, lvl)


__all__ = [
    "BaseSerializer",
    "JSONSerializer",
    "MarkdownSerializer",
    "TextSerializer",
    "InvestigationContextSerializer",
]
