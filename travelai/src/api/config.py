"""
Configuration for TravelAI application.
"""
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    """
    Application settings.
    """
    APP_NAME: str = "TravelAI"
    DEBUG: bool = False
    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/travelai"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

    @property
    def database_url_str(self) -> str:
        """Return database URL as string for SQLAlchemy"""
        return str(self.DATABASE_URL)


# Create settings instance
settings = Settings()