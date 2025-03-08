"""
TravelAI specific ledger schemas.
"""
from monorepo.core.ledgers.schemas import BaseLedgerOperation
from monorepo.core.ledgers.pydantic_schemas import create_ledger_schemas


class TravelAILedgerOperation(BaseLedgerOperation):
    """
    TravelAI specific ledger operations.
    This class inherits from BaseLedgerOperation and must implement