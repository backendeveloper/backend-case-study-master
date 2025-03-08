"""
HealthAI specific ledger SQLAlchemy models.
"""
from monorepo.core.db.models import BaseLedgerEntry, EnumType
from healthai.src.api.ledgers.schemas import HealthAILedgerOperation


# Create a concrete ledger entry model for HealthAI
HealthAILedgerEntryModel = BaseLedgerEntry.create_concrete_model(
    "HealthAILedgerEntryModel", 
    HealthAILedgerOperation
)