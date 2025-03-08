"""
Core database models for ledger functionality.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic, Union

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator

from monorepo.core.ledgers.schemas import BaseLedgerOperation, TLedgerOperation


Base = declarative_base()


class EnumType(TypeDecorator):
    """
    SQLAlchemy type decorator for Enum storage.
    Stores the enum name as a string in the database.
    """
    impl = String
    cache_ok = True

    def __init__(self, enum_class: Type[BaseLedgerOperation]):
        super().__init__(50)  # Max length for enum names
        self.enum_class = enum_class

    def process_bind_param(self, value: Optional[Union[str, BaseLedgerOperation]], dialect: Any) -> Optional[str]:
        """Convert enum object to string for DB storage."""
        if value is None:
            return None
        if isinstance(value, BaseLedgerOperation):
            return value.name
        return value

    def process_result_value(self, value: Optional[str], dialect: Any) -> Optional[BaseLedgerOperation]:
        """Convert stored string back to enum object."""
        if value is None:
            return None
        return self.enum_class[value]


class BaseLedgerEntry(Base):
    """
    Base SQLAlchemy model for ledger entries.
    This is designed to be used directly by all applications.
    """
    __tablename__ = "ledger_entries"
    __abstract__ = True  # This indicates it's an abstract base class

    id = Column(Integer, primary_key=True, autoincrement=True)
    # operation type will be defined in the concrete class
    amount = Column(Integer, nullable=False)
    nonce = Column(String(100), nullable=False, unique=True)
    owner_id = Column(String(100), nullable=False, index=True)
    created_on = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self) -> str:
        return f"<LedgerEntry(id={self.id}, operation={self.operation}, amount={self.amount}, owner_id={self.owner_id})>"

    @classmethod
    def create_concrete_model(cls, name: str, operation_enum: Type[BaseLedgerOperation]) -> Type[BaseLedgerEntry]:
        """
        Create a concrete ledger entry model for a specific application.

        Args:
            name: Name of the concrete model
            operation_enum: The enum class to use for operations

        Returns:
            A concrete SQLAlchemy model class
        """
        attrs = {
            "__tablename__": "ledger_entries",
            "operation": Column(EnumType(operation_enum), nullable=False, index=True)
        }

        return type(name, (cls,), attrs)