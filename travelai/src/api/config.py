"""
Configuration for TravelAI application.
"""
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """
    Application settings.
    """
    APP_NAME: str = "TravelAI"
    DEBUG: bool = False
    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/travelai"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()