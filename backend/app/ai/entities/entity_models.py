"""Provider-neutral entities used by the Crime Knowledge Graph."""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    CASE = "Case"; VICTIM = "Victim"; WITNESS = "Witness"; ACCUSED = "Accused"
    OFFICER = "Officer"; EVIDENCE = "Evidence"; COURT = "Court"; TIMELINE = "Timeline"
    CHARGESHEET = "Chargesheet"; ACT = "Act"; SECTION = "Section"; VEHICLE = "Vehicle"
    WEAPON = "Weapon"; ADDRESS = "Address"; PHONE = "Phone"; EMAIL = "Email"
    ORGANIZATION = "Organization"; DOCUMENT = "Document"


class EntityAlias(BaseModel):
    value: str
    source: str = "record"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EntityRecord(BaseModel):
    id: str
    entity_type: EntityType
    label: str
    source_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    aliases: list[EntityAlias] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
