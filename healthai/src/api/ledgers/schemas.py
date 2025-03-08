"""
HealthAI specific ledger schemas.
"""
from monorepo.core.ledgers.schemas import BaseLedgerOperation
from monorepo.core.ledgers.pydantic_schemas import create_ledger_schemas


class HealthAILedgerOperation(BaseLedgerOperation):
    """
    HealthAI specific ledger operations.
    This class inherits from BaseLedgerOperation and must implement
    all shared operations.
    """
    # Shared operations - required by the metaclass
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"


# Create Pydantic schemas for HealthAI
HealthAILedgerEntryCreate, HealthAILedgerEntryRead = create_ledger_schemas(HealthAILedgerOperation)