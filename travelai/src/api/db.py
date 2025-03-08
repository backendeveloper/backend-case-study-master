"""
Database configuration for TravelAI.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from travelai.src.api.config import settings


# Create database engine
engine = create_async_engine(
    str(settings.DATABASE_URL),  # PostgresDsn'yi string'e dönüştür
    echo=settings.DEBUG,
    future=True  # Use SQLAlchemy 2.0 style
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# Dependency for FastAPI endpoints
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()