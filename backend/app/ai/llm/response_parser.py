"""
Structured Response Parser for LLM Gateway output.
Parses and validates raw text output into Pydantic models from Phase 3.4 Output Schemas.
"""

import json
import re
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel

from app.ai.llm.exceptions import ResponseValidationException
from app.ai.prompting.output_schema_registry import OutputSchemaRegistry


class StructuredResponseParser:
    """Parses raw text into JSON and validates against registered Pydantic schemas."""

    @classmethod
    def parse_and_validate(
        cls, content: str, schema_name: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Parses content string into structured JSON dict matching schema_name."""
        if not schema_name:
            return None

        schema_cls = OutputSchemaRegistry.get(schema_name)
        if not schema_cls:
            return None

        # Extract JSON substring if wrapped in markdown ```json ... ```
        json_str = cls._extract_json_string(content)

        try:
            raw_dict = json.loads(json_str)
            validated_obj = schema_cls.model_validate(raw_dict)
            return validated_obj.model_dump()
        except Exception as e:
            raise ResponseValidationException(
                f"Failed to parse and validate output for schema '{schema_name}': {str(e)}"
            ) from e

    @staticmethod
    def _extract_json_string(content: str) -> str:
        """Extracts JSON text block from markdown fences or raw string."""
        match = re.search(r"```(?:json)?\s*(\{.*\}|\[.*\])\s*```", content, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # Search for first { or [ to matching last } or ]
        first_brace = content.find("{")
        last_brace = content.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            return content[first_brace : last_brace + 1].strip()

        return content.strip()
