import logging
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("crimesphere.config")


class Settings(BaseSettings):

    # ── App ──────────────────────────────────────────────────────────────────
    APP_NAME: str = "CrimeSphere AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = int(os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT", "8000"))
    LOG_LEVEL: str = "INFO"

    # ── Security (MUST be set via AppSail env vars in production) ────────────
    SECRET_KEY: str = "insecure-default-change-in-appsail"
    JWT_SECRET_KEY: str = "insecure-default-change-in-appsail"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = ""
    DATABASE_NAME: str = ""

    # ── Zoho Catalyst ─────────────────────────────────────────────────────────
    CATALYST_PROJECT_ID: str = ""
    CATALYST_CLIENT_ID: str = ""
    CATALYST_CLIENT_SECRET: str = ""
    ZOHO_CLIENT_ID: str = ""
    ZOHO_CLIENT_SECRET: str = ""
    ZOHO_CATALYST_PROJECT_ID: str = ""
    ZOHO_CATALYST_ORG_ID: str = ""
    ZOHO_QUICKML_KB_IDS: str = ""

    # ── Neo4j (optional) ──────────────────────────────────────────────────────
    NEO4J_URI: str = ""
    NEO4J_USERNAME: str = ""
    NEO4J_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    def warn_insecure_defaults(self) -> None:
        if "insecure-default" in self.SECRET_KEY:
            logger.warning(
                "⚠️  SECRET_KEY is using the insecure default! "
                "Set SECRET_KEY in AppSail environment variables."
            )
        if "insecure-default" in self.JWT_SECRET_KEY:
            logger.warning(
                "⚠️  JWT_SECRET_KEY is using the insecure default! "
                "Set JWT_SECRET_KEY in AppSail environment variables."
            )


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.warn_insecure_defaults()
    return s


settings = get_settings()