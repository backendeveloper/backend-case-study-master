"""
TravelAI specific ledger schemas.
"""
from monorepo.core.ledgers.schemas import BaseLedgerOperation
from monorepo.core.ledgers.pydantic_schemas import create_ledger_schemas


class TravelAILedgerOperation(BaseLedgerOperation):
    """
    TravelAI specific ledger operations.
    This class inherits from BaseLedgerOperation and must implement
    all shared operations.
    """
    # Shared operations - required by the metaclass
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    # App-specific operations
    BOOKING_REWARD = "BOOKING_REWARD"
    LOYALTY_BONUS = "LOYALTY_BONUS"


# Create Pydantic schemas for TravelAI
TravelAILedgerEntryCreate, TravelAILedgerEntryRead = create_ledger_schemas(TravelAILedgerOperation)