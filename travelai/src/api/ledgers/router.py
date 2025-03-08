"""
API endpoints for TravelAI ledger functionality.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from travelai.src.api.db import get_db
from travelai.src.api.ledgers.models import TravelAILedgerEntryModel
from travelai.src.api.ledgers.schemas import (
    TravelAILedgerOperation,
    TravelAILedgerEntryCreate,
    TravelAILedgerEntryRead
)
from monorepo.core.ledgers.services.base_ledger_service import create_ledger_service
from monorepo.core.ledgers.pydantic_schemas import LedgerBalanceResponse

router = APIRouter(prefix="/ledger", tags=["ledger"])

# Create a concrete ledger service for TravelAI
TravelAILedgerService = create_ledger_service(TravelAILedgerEntryModel, TravelAILedgerOperation)
ledger_service = TravelAILedgerService()


@router.get(
    "/{owner_id}",
    response_model=LedgerBalanceResponse,
    summary="Get owner balance",
    description="Returns the current balance for the specified owner"
)
async def get_balance(
        owner_id: str,
        db: AsyncSession = Depends(get_db)
):
    """
    Get the current balance for an owner.

    Args:
        owner_id: ID of the owner
        db: Database session

    Returns:
        Current balance information
    """
    return await ledger_service.get_balance(db, owner_id)


@router.post(
    "/",
    response_model=TravelAILedgerEntryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add ledger entry",
    description="Creates a new ledger entry for the specified owner"
)
async def add_ledger_entry(
        entry: TravelAILedgerEntryCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    Add a new ledger entry.

    Args:
        entry: Ledger entry data
        db: Database session

    Returns:
        The created ledger entry
    """
    return await ledger_service.add_ledger_entry(
        db=db,
        owner_id=entry.owner_id,
        operation=entry.operation,
        nonce=entry.nonce
    )