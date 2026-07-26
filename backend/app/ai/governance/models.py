from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field
class GovernancePolicy(BaseModel): policy_id: str; name: str; enabled: bool = True; blocked_terms: list[str] = Field(default_factory=list); allowed_roles: list[str] = Field(default_factory=list); classifications: list[str] = Field(default_factory=list); require_approval: bool = False
class GovernanceRequest(BaseModel): user_id: str; role: str; prompt: str = ''; response: str = ''; provider: str | None = None; model: str | None = None; classification: str = 'Internal'; metadata: dict[str, Any] = Field(default_factory=dict)
class ComplianceResult(BaseModel): compliant: bool; decisions: list[str] = Field(default_factory=list); approval_required: bool = False
class RetentionRecord(BaseModel): resource_id: str; retain_until: datetime; created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
