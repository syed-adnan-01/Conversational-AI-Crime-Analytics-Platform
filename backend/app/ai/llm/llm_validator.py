"""
LLM Response Gatekeeper Validator.
"""

from typing import Dict, Any, Optional
from app.ai.llm.exceptions import ResponseValidationException
from app.ai.llm.llm_models import LLMResponse
from app.ai.llm.response_parser import StructuredResponseParser
from app.ai.llm.safety import SafetyValidator


class LLMValidator:
    """Validates an LLMResponse against safety guardrails and schema specifications."""

    @classmethod
    def validate_response(
        cls, response: LLMResponse, response_schema: Optional[str] = None
    ) -> LLMResponse:
        """Applies safety checks and populates parsed_output if schema is requested."""
        # 1. Safety Validation
        is_safe, violations = SafetyValidator.validate_safety(response.content)
        if not is_safe:
            response.safety_passed = False

        # 2. Schema Validation (if schema requested)
        if response_schema:
            parsed = StructuredResponseParser.parse_and_validate(response.content, response_schema)
            response.parsed_output = parsed

        return response
