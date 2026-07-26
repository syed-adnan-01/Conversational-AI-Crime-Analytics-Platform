from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field
class DataClassification(str, Enum): PUBLIC='Public'; INTERNAL='Internal'; CONFIDENTIAL='Confidential'; RESTRICTED='Restricted'; HIGHLY_SENSITIVE='Highly Sensitive'
class MaskingLevel(str, Enum): NONE='none'; PARTIAL='partial'; FULL='full'
class SecurityRequest(BaseModel): user_id: str; role: str; endpoint: str; text: str = ''; ip_address: str | None = None; classification: DataClassification = DataClassification.INTERNAL; provider: str | None = None
class PolicyDecision(BaseModel): allowed: bool; reasons: list[str] = Field(default_factory=list); masked_text: str | None = None
class AuditEntry(BaseModel): audit_id: str = Field(default_factory=lambda: f'audit-{uuid4().hex}'); user_id: str; role: str; endpoint: str; provider: str | None = None; prompt_hash: str | None = None; response_hash: str | None = None; decision_ids: list[str] = Field(default_factory=list); retrieval_ids: list[str] = Field(default_factory=list); agent_ids: list[str] = Field(default_factory=list); policy_decisions: list[str] = Field(default_factory=list); created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)); previous_hash: str = ''; entry_hash: str = ''
class SecurityMetrics(BaseModel): requests: int = 0; denied: int = 0; pii_detections: int = 0; rate_limited: int = 0
