"""
Configuration for HealthAI application.
"""
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """
    Application settings.
    """
    APP_NAME: str = "HealthAI"
    DEBUG: bool = False
    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/healthai"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()