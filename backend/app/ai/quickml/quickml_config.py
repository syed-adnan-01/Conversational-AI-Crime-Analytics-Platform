"""Configuration for Zoho Catalyst QuickML integration."""

from __future__ import annotations

import os
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class QuickMLConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    CATALYST_PROJECT_ID: str = Field(default_factory=lambda: os.getenv("CATALYST_PROJECT_ID", ""))
    CATALYST_ORG_ID: str = Field(default_factory=lambda: os.getenv("CATALYST_ORG_ID", ""))
    ZOHO_ACCESS_TOKEN: str = Field(default_factory=lambda: os.getenv("ZOHO_ACCESS_TOKEN", ""))
    QUICKML_DOC_IDS: List[str] = Field(default_factory=list)
    QUICKML_TIMEOUT: float = Field(default_factory=lambda: float(os.getenv("QUICKML_TIMEOUT", "30")))
    QUICKML_MAX_RETRIES: int = Field(default_factory=lambda: int(os.getenv("QUICKML_MAX_RETRIES", "3")))

    @field_validator("QUICKML_DOC_IDS", mode="before")
    @classmethod
    def _parse_doc_ids(cls, value: object) -> list[str]:
        if value is None:
            raw = os.getenv("QUICKML_DOC_IDS", "")
            value = raw
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, (list, tuple, set)):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    @property
    def is_configured(self) -> bool:
        return bool(self.CATALYST_PROJECT_ID and self.CATALYST_ORG_ID and self.ZOHO_ACCESS_TOKEN and self.QUICKML_DOC_IDS)


quickml_config = QuickMLConfig()