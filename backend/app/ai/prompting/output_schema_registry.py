"""
Registry mapping PromptType to Output Schema definitions and formatting instructions.
"""

import json
from typing import Type
from pydantic import BaseModel

from app.ai.prompting.output_schemas import (
    CaseSummaryOutput,
    ChargesheetOutput,
    EvidenceAnalysisOutput,
    InvestigationRecommendationOutput,
    LegalOpinionOutput,
    TimelineOutput,
)
from app.ai.prompting.prompt_models import PromptType


class OutputSchemaRegistry:
    """Central registry mapping PromptType to Pydantic output schemas."""

    _MAPPING: dict[PromptType, Type[BaseModel]] = {
        PromptType.SUMMARY: CaseSummaryOutput,
        PromptType.LEGAL_ANALYSIS: LegalOpinionOutput,
        PromptType.EVIDENCE_ANALYSIS: EvidenceAnalysisOutput,
        PromptType.TIMELINE: TimelineOutput,
        PromptType.CHARGESHEET: ChargesheetOutput,
        PromptType.CASE_ANALYSIS: CaseSummaryOutput,
        PromptType.NEXT_STEPS: InvestigationRecommendationOutput,
        PromptType.REPORT: CaseSummaryOutput,
    }

    @classmethod
    def get(cls, key: str | PromptType | None) -> Type[BaseModel] | None:
        """Returns the Pydantic schema class for a given PromptType or schema name string."""
        if not key:
            return None
        if isinstance(key, PromptType):
            return cls._MAPPING.get(key)
        
        # String lookup by class name or PromptType name
        key_str = str(key).upper()
        for ptype, schema_cls in cls._MAPPING.items():
            if schema_cls.__name__.upper() == key_str or ptype.name.upper() == key_str or ptype.value.upper() == key_str:
                return schema_cls
        return None

    @classmethod
    def get_schema_class(cls, prompt_type: PromptType) -> Type[BaseModel] | None:
        """Returns the Pydantic schema class for a given PromptType."""
        return cls.get(prompt_type)

    @classmethod
    def get_json_schema(cls, prompt_type: PromptType) -> dict | None:
        """Returns the JSON schema dict for a given PromptType."""
        schema_cls = cls.get_schema_class(prompt_type)
        if schema_cls:
            return schema_cls.model_json_schema()
        return None

    @classmethod
    def get_formatting_instructions(cls, prompt_type: PromptType) -> str:
        """Generates clear instructions instructing the LLM to output valid JSON matching the schema."""
        schema_dict = cls.get_json_schema(prompt_type)
        if not schema_dict:
            return "Please provide a clear, well-structured text response."

        schema_name = schema_dict.get("title", "ResponseSchema")
        schema_json = json.dumps(schema_dict, indent=2)

        return (
            f"\n\n### CRITICAL OUTPUT FORMATTING INSTRUCTIONS\n"
            f"You MUST format your final response strictly as valid JSON matching the following schema (`{schema_name}`):\n"
            f"```json\n{schema_json}\n```\n"
            f"Do not include any conversational preamble or markdown code blocks outside of the valid JSON structure."
        )
