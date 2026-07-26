from pydantic import BaseModel, Field
from .models import MaskingLevel
class SecurityConfiguration(BaseModel): masking_level: MaskingLevel = MaskingLevel.PARTIAL; user_limit: int = 60; role_limit: int = 120; ip_limit: int = 100; burst_limit: int = 15; blocked_terms: list[str] = Field(default_factory=list)
