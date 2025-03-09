"""
Base ledger service for shared functionality across all applications.
"""
from __future__ import annotations

import datetime
from typing import Generic, Optional, Type, TypeVar

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.db.models import BaseLedgerEntry
from monorepo.core.ledgers.schemas import BaseLedgerOperation, TLedgerOperation
from monorepo.core.ledgers.pydantic_schemas import LedgerBalanceResponse, LedgerEntryRead

# Define type variables before using them
TLedgerEntry = TypeVar('TLedgerEntry', bound=BaseLedgerEntry)


class BaseLedgerService(Generic[TLedgerEntry, TLedgerOperation]):
    """
    Base ledger service with shared functionality.
    """

    def __init__(self, repository: LedgerRepository[TLedgerEntry, TLedgerOperation]):
        """
        Initialize the service.

        Args:
            repository: The ledger repository
        """
        self.repository = repository

    async def add_ledger_entry(
            self,
            db: AsyncSession,
            owner_id: str,
            operation: TLedgerOperation,
            nonce: str
    ) -> LedgerEntryRead:
        """
        Add a new ledger entry.

        Args:
            db: Database session
            owner_id: ID of the owner
            operation: The ledger operation
            nonce: Unique identifier to prevent duplicate transactions

        Returns:
            The created ledger entry

        Raises:
            HTTPException: If insufficient balance or duplicate nonce
        """
        # Check for duplicate transaction
        if await self.repository.check_nonce_exists(db, nonce):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate transaction detected"
            )

        # Check for sufficient balance
        has_balance = await self.repository.has_sufficient_balance(db, owner_id, operation)
        if not has_balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance for this operation"
            )

        # Create entry
        entry = await self.repository.create_entry(db, owner_id, operation, nonce)

        # Convert to Pydantic model and return
        return LedgerEntryRead(
            id=entry.id,
            operation=entry.operation,
            amount=entry.amount,
            nonce=entry.nonce,
            owner_id=entry.owner_id,
            created_on=entry.created_on
        )

    async def get_balance(self, db: AsyncSession, owner_id: str) -> LedgerBalanceResponse:
        """
        Get the current balance for an owner.

        Args:
            db: Database session
            owner_id: ID of the owner

        Returns:
            Current balance
        """
        balance = await self.repository.get_owner_balance(db, owner_id)

        return LedgerBalanceResponse(
            owner_id=owner_id,
            balance=balance,
            last_updated=datetime.datetime.utcnow()
        )


TLedgerEntry = TypeVar('TLedgerEntry', bound=BaseLedgerEntry)


def create_ledger_service(
        model: Type[BaseLedgerEntry],
        operation_enum: Type[BaseLedgerOperation]
) -> Type[BaseLedgerService]:
    """
    Factory function to create a concrete ledger service for a specific application.

    Args:
        model: The SQLAlchemy model class
        operation_enum: The enum class for operations

    Returns:
        A concrete ledger service class
    """
    ledger_repository = LedgerRepository[model, operation_enum](model)

    class ConcreteLedgerService(BaseLedgerService[model, operation_enum]):
        def __init__(self):
            super().__init__(ledger_repository)

    return ConcreteLedgerService