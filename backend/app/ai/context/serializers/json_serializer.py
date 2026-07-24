"""
============================================================
JSON Serializer Strategy
============================================================

Module  : AI Context Builder
Purpose : Formats InvestigationContext into machine-readable JSON.
"""

import json
from datetime import datetime
from enum import Enum

from app.ai.context.context_models import DetailLevel, InvestigationContext
from app.ai.context.exceptions import AIContextSerializationException
from app.ai.context.serializers.base import BaseSerializer


class CustomJSONEncoder(json.JSONEncoder):
    """JSON Encoder for datetimes and Enums."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)


class JSONSerializer(BaseSerializer):
    """
    Serializes InvestigationContext into clean machine-readable JSON strings.
    """

    def serialize(
        self,
        context: InvestigationContext,
        level: DetailLevel = DetailLevel.STANDARD,
    ) -> str:
        try:
            if level == DetailLevel.SUMMARY:
                data = {
                    "summary": context.summary.model_dump(mode="json"),
                    "metadata": context.metadata.model_dump(mode="json"),
                }
            else:
                data = context.model_dump(mode="json")
                if level == DetailLevel.STANDARD:
                    # Omit null/empty optional AI extensions in standard view
                    for field in ("relationships", "analytics", "predictions", "documents", "embeddings", "knowledge"):
                        if field in data and data[field] is None:
                            data.pop(field, None)

            return json.dumps(data, indent=2, cls=CustomJSONEncoder)
        except Exception as exc:
            raise AIContextSerializationException("JSON", str(exc)) from exc
