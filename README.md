# Backend Developer Case Study: Shared Ledger System

## Overview

Design and implement a shared ledger system for a monorepo containing multiple applications, focusing on code reuse and type safety.

## Background

You're working on a monorepo that contains multiple applications. Each application needs to track user credits through a ledger system. While the core ledger functionality is shared, each application has its own specific operations.

## Current Problems

- No enforcement of shared operations
- Type incompability between monorepo/core LedgerOperation and app specific LedgerOperation

## Current Implementation

```python
# In monorepo/core/ledgers/schemas.py
class LedgerOperation(enum.Enum): # This should be more generic!
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"
```

```python
# In appName/src/api/ledgers/schemas.py
class LedgerOperation(Enum):
    # Shared operations
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"
```

## Type Safety Examples

```python
# This should fail
class BadOperation(BaseLedgerOperation):
    CONTENT_CREATION = "CONTENT_CREATION"  # Missing shared operations!

# This should work
class GoodOperation(BaseLedgerOperation):
    # Required shared operations
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"
```

## Data Schema Requirements

```python
# Ledger Entry Table Schema

| Column     | Type                     | Constraints               |
|------------|--------------------------|---------------------------|
| id         | Integer                  | Primary Key               |
| operation  | Enum                     | Not Null                  |
| amount     | Integer                  | Not Null                  |
| nonce      | String                   | Not Null                  |
| owner_id   | String                   | Not Null                  |
| created_on | DateTime                 | Not Null                  |

```

### Technical Requirements

1. All applications must use the SQLAlchemy model from the monorepo core
2. All applications must use the Pydantic model from the monorepo core
3. All applications must use the same ledger logic from the monorepo core
4. BaseLedgerOperation and its subclasses must be implemented as Enums. (Tip: Since Enums are final by design (cannot be inherited), how would you architect a solution that maintains both the benefits of Enums and the need for extensibility?")
5. The monorepo core implementation must be generic enough to support new applications
6. Alembic migrations should be scoped to affected application(s) only
7. The project must be implemented using the following specified technologies:

- Python ≥ 3.10
- FastAPI
- SQLAlchemy ≥ 2.0.0
- Pydantic
- Alembic
- PostgreSQL

8. Enforce shared ledger operations implementation
9. Use proper type hints throughout
10. Implement and test the following endpoints:

```
GET /ledger/{owner_id}
- Returns: Current balance for the owner

POST /ledger
- Body: owner_id, ledger operation, nonce
- Validates sufficient balance
- Prevents duplicate transactions via nonce
```

You can use the following ledger operation configuration as a reference:

```python
LEDGER_OPERATION_CONFIG = {

    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,

    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
}
```

## Submission Guidelines

1. Submit via GitHub repository
2. Include:
   - Implementation
   - Tests
   - Documentation
   - Migration examples
3. AI tools allowed for assistance
4. Clear commit history showing implementation process

## Recommendations

1. **Environment Management**

   - Use a virtual environment for dependency isolation.

2. **Dependency Management**

   - Use a package manager to manage dependencies and environments.

3. **Code Formatting**

   - Use a code formatter to ensure consistent code style.

4. **Static Type Checking**

   - Use a type checker to enforce type safety and catch type errors early.

5. **Linting**

   - Use a linter to enforce coding standards and catch potential issues.
