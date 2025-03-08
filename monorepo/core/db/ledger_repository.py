"""
Repository layer for ledger database operations.
"""
from __future__ import annotations

import datetime
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import func, select, and_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from monorepo.core.db.models import BaseLedgerEntry
from monorepo.core.ledgers.schemas import BaseLedgerOperation, TLedgerOperation

TLedgerEntry = TypeVar('TLedgerEntry', bound=BaseLedgerEntry)


class LedgerRepository(Generic[TLedgerEntry, TLedgerOperation]):
    """
    Repository for ledger database operations.
    This class provides a generic interface for ledger operations.
    """

    def __init__(self, model: Type[TLedgerEntry]):
        """
        Initialize the repository.

        Args:
            model: The SQLAlchemy model class to use
        """
        self.model = model

    async def create_entry(self, db: AsyncSession, owner_id: str, operation: TLedgerOperation,
                           nonce: str) -> TLedgerEntry:
        """
        Create a new ledger entry.

        Args:
            db: Database session
            owner_id: ID of the owner
            operation: The ledger operation
            nonce: Unique identifier to prevent duplicate transactions

        Returns:
            The created ledger entry
        """
        # Check if the nonce already exists
        stmt = select(exists().where(self.model.nonce == nonce))
        result = await db.execute(stmt)
        if result.scalar():
            raise ValueError(f"Duplicate transaction with nonce: {nonce}")

        # Create new entry
        amount = operation.value_amount
        entry = self.model(
            owner_id=owner_id,
            operation=operation,
            amount=amount,
            nonce=nonce,
            created_on=datetime.datetime.utcnow()
        )

        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry

    async def get_entries_by_owner(self, db: AsyncSession, owner_id: str) -> List[TLedgerEntry]:
        """
        Get all ledger entries for an owner.

        Args:
            db: Database session
            owner_id: ID of the owner

        Returns:
            List of ledger entries
        """
        stmt = select(self.model).where(self.model.owner_id == owner_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_owner_balance(self, db: AsyncSession, owner_id: str) -> int:
        """
        Calculate the current balance for an owner.

        Args:
            db: Database session
            owner_id: ID of the owner

        Returns:
            Current balance
        """
        stmt = select(func.sum(self.model.amount)).where(self.model.owner_id == owner_id)
        result = await db.execute(stmt)
        balance = result.scalar() or 0
        return balance

    async def has_sufficient_balance(self, db: AsyncSession, owner_id: str, operation: TLedgerOperation) -> bool:
        """
        Check if the owner has sufficient balance for the operation.

        Args:
            db: Database session
            owner_id: ID of the owner
            operation: The ledger operation

        Returns:
            True if sufficient balance, False otherwise
        """
        amount = operation.value_amount
        if amount >= 0:
            return True

        balance = await self.get_owner_balance(db, owner_id)
        return balance + amount >= 0  # Check if balance after operation would still be >= 0

    async def check_nonce_exists(self, db: AsyncSession, nonce: str) -> bool:
        """
        Check if a nonce already exists to prevent duplicate transactions.

        Args:
            db: Database session
            nonce: The nonce to check

        Returns:
            True if nonce exists, False otherwise
        """
        stmt = select(exists().where(self.model.nonce == nonce))
        result = await db.execute(stmt)
        return result.scalar()