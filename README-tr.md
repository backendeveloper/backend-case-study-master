# Shared Ledger System

This monorepo contains a shared ledger system implemented for multiple applications, focusing on code reuse, type safety, and clean architecture.

## Overview

The project uses a monorepo structure with a shared core module and multiple application-specific implementations. The ledger system tracks user credits across different applications while enforcing shared operations and maintaining type safety.

## Features

- Type-safe shared ledger operations across applications
- Centralized implementation to prevent code duplication
- Application-specific extensible operations
- FastAPI, SQLAlchemy 2.0, Pydantic, and PostgreSQL integration
- Docker-based database setup
- Proper async database operations

## Requirements

- Python ≥ 3.10
- Docker and Docker Compose
- PostgreSQL
- Make (optional, for using the Makefile commands)

## Quick Start

### Using Make

```bash
# Setup virtual environment and install dependencies
make setup

# Start PostgreSQL with Docker
make db-up

# Setup both applications
make setup-healthai
make setup-travelai

# Run both applications
make run-all
```

### Using the Run Script

```bash
# Make the script executable
chmod +x run.sh

# Run the script
./run.sh
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -e .

# Start PostgreSQL with Docker
chmod +x docker-entrypoint-initdb.d/create-multiple-databases.sh
docker-compose up -d

# Setup HealthAI database
cd healthai
python setup_db.py
cd ..

# Setup TravelAI database
cd travelai
python setup_db.py
cd ..

# Run HealthAI
cd healthai
uvicorn src.main:app --reload --port 8000
# In another terminal
cd travelai
uvicorn src.main:app --reload --port 8001
```

## Project Structure

```
├── monorepo/                      # Shared core functionality
│   ├── core/
│   │   ├── db/                    # Database models and repositories
│   │   │   ├── models.py          # Core SQLAlchemy models
│   │   │   └── ledger_repository.py  # Database operations
│   │   └── ledgers/               # Ledger business logic
│   │       ├── services/          # Service layer
│   │       │   └── base_ledger_service.py  # Core service logic
│   │       ├── schemas.py         # Core enum definitions
│   │       ├── pydantic_schemas.py  # Pydantic models
│   │       └── config.py          # Operation value configuration
├── healthai/                      # HealthAI application
│   ├── src/
│   │   ├── api/
│   │   │   ├── ledgers/
│   │   │   │   ├── models.py      # App-specific models
│   │   │   │   ├── router.py      # API endpoints
│   │   │   │   └── schemas.py     # App-specific operations
│   │   │   ├── config.py          # App configuration
│   │   │   └── db.py              # Database connection
│   │   └── main.py                # Application entry point
│   ├── migrations/                # Alembic migrations
│   └── setup_db.py                # Database setup script
├── travelai/                      # TravelAI application (similar structure)
├── docker-compose.yml             # Docker Compose configuration
├── Makefile                       # Build automation
├── run.sh                         # Run script
└── setup.py                       # Package setup
```

## API Usage

### Get Balance

```http
GET /ledger/{owner_id}
```

Response:
```json
{
  "owner_id": "user123",
  "balance": 42,
  "last_updated": "2023-01-01T12:00:00Z"
}
```

### Create Ledger Entry

```http
POST /ledger/
```

Request:
```json
{
  "owner_id": "user123",
  "operation": "CREDIT_ADD",
  "nonce": "unique-transaction-id-123"
}
```

Response:
```json
{
  "id": 1,
  "operation": "CREDIT_ADD",
  "amount": 10,
  "nonce": "unique-transaction-id-123",
  "owner_id": "user123",
  "created_on": "2023-01-01T12:00:00Z"
}
```

## Operation Configuration

The system uses a configuration-based approach for operation values:

```python
LEDGER_OPERATION_CONFIG = {
    # Shared operations
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,

    # App-specific operations
    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
    "BOOKING_REWARD": 5,
    "LOYALTY_BONUS": 2,
}
```

## Type Safety

The system enforces type safety by requiring all applications to implement shared operations. This is accomplished through a custom metaclass that validates enum definitions:

```python
# This will fail at runtime
class BadOperation(BaseLedgerOperation):
    # Missing required shared operations!
    CONTENT_CREATION = "CONTENT_CREATION"  

# This will work
class GoodOperation(BaseLedgerOperation):
    # Required shared operations
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"
    
    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"
```

## Contributing

1. Make sure all code has proper type hints
2. Follow the established code style
3. Add tests for new functionality
4. Update documentation for API changes