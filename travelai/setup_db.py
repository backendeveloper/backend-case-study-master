"""
Database setup script for TravelAI.
This script creates all tables and initializes the database.
"""
import sys
import os
# Ana proje dizinini Python path'ine ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine

from monorepo.core.db.models import Base
from travelai.src.api.ledgers.models import TravelAILedgerEntryModel
from travelai.src.api.config import settings


async def setup_database():
    """
    Set up the database by creating all tables.
    """
    print(f"Setting up database at {settings.DATABASE_URL}")

    # Create engine
    engine = create_async_engine(
        settings.database_url_str,  # Use the string method
        echo=True,
    )

    async with engine.begin() as conn:
        # Drop all tables if they exist
        if len(sys.argv) > 1 and sys.argv[1] == "--drop":
            print("Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("Database setup complete.")


if __name__ == "__main__":
    asyncio.run(setup_database())