from setuptools import setup, find_packages

setup(
    name="shared-ledger-system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.11.0",
        "asyncpg>=0.28.0",
        "pydantic>=2.0.0",
        "psycopg2-binary>=2.9.6",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.10",
)