"""
TravelAI specific ledger SQLAlchemy models.
"""
from monorepo.core.db.models import BaseLedgerEntry, EnumType
from travelai.src.api.ledgers.schemas import TravelAILedgerOperation


# Create a concrete ledger entry model for TravelAI
TravelAILedgerEntryModel = BaseLedgerEntry.create_concrete_model(
    "TravelAILedgerEntryModel", 
    TravelAILedgerOperation
)