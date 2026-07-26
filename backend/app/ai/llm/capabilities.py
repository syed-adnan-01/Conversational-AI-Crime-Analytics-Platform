"""
Provider Capabilities Model.
Defines explicit feature support per LLM provider to eliminate hardcoded code branches.
"""

from pydantic import BaseModel, ConfigDict, Field


class ProviderCapabilities(BaseModel):
    """Capability matrix for an LLM Provider."""
    model_config = ConfigDict(from_attributes=True)

    provider_name: str
    streaming: bool = True
    json_mode: bool = True
    tool_calling: bool = True
    image_input: bool = False
    multimodal: bool = False
    max_context_window: int = 1048576
    structured_output: bool = True
