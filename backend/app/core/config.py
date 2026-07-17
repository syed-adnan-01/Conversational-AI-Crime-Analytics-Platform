from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str

    APP_VERSION: str

    ENVIRONMENT: str

    DEBUG: bool

    HOST: str

    PORT: int

    SECRET_KEY: str

    LOG_LEVEL: str

    CATALYST_PROJECT_ID: str = ""

    CATALYST_CLIENT_ID: str = ""

    CATALYST_CLIENT_SECRET: str = ""

    DATABASE_NAME: str = ""

    NEO4J_URI: str = ""

    NEO4J_USERNAME: str = ""

    NEO4J_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()