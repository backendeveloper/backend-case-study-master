"""
Pydantic schemas for ledger functionality.
"""
from __future__ import annotations

import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

from monorepo.core.ledgers.schemas import BaseLedgerOperation, TLedgerOperation


class LedgerEntryBase(GenericModel, Generic[TLedgerOperation]):
    """Base Pydantic model for ledger entry data."""
    operation: TLedgerOperation
    amount: Optional[int] = None
    nonce: str
    owner_id: str

    @validator('amount', pre=True, always=True)
    def set_amount_from_operation(cls, v: Optional[int], values: dict) -> int:
        """Automatically set the amount based on the operation if not provided."""
        if v is not None:
            return v

        operation = values.get('operation')
        if operation is None:
            raise ValueError('Operation is required to calculate amount')

        return operation.value_amount


class LedgerEntryCreate(LedgerEntryBase[TLedgerOperation]):
    """Model for creating a new ledger entry."""
    pass


class LedgerEntryRead(LedgerEntryBase[TLedgerOperation]):
    """Model for reading a ledger entry."""
    id: int
    created_on: datetime.datetime

    class Config:
        orm_mode = True


class LedgerBalanceResponse(BaseModel):
    """Response model for balance inquiries."""
    owner_id: str
    balance: int
    last_updated: datetime.datetime


def create_ledger_schemas(operation_enum: type[BaseLedgerOperation]):
    """
    Factory function to create concrete Pydantic schema classes for a specific app.

    Args:
        operation_enum: The enum class to use for operations

    Returns:
        Tuple of (LedgerEntryCreate, LedgerEntryRead) classes
    """

    class ConcreteLedgerEntryCreate(LedgerEntryCreate[operation_enum]):
        pass

    class ConcreteLedgerEntryRead(LedgerEntryRead[operation_enum]):
        pass

    return ConcreteLedgerEntryCreate, ConcreteLedgerEntryRead