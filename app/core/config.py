import os
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file() -> str:
    """Get the appropriate .env file based on the ENV environment variable."""
    env = os.getenv("ENV", "development").lower()
    env_file = f".env.{env}"

    # Si el archivo específico no existe, usar .env por defecto
    if not os.path.exists(env_file):
        return ".env"

    return env_file


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = Field(default="FastAPI Template", alias="APP_NAME")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_url: str = Field(
        default="postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_db",
        alias="DATABASE_URL",
    )

    cors_origins: list[str] = Field(
        default=["http://localhost:3000"], alias="CORS_ORIGINS"
    )

    version: str = Field(default="0.1.0", alias="VERSION")

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v: Any) -> bool:
        """Parse debug value from string or bool."""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return bool(v)

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
