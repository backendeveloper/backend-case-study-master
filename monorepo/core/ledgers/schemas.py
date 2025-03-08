"""
Core ledger schemas for shared functionality across all applications.
"""
from __future__ import annotations

import enum
from typing import Any, Dict, Set, Type, TypeVar, cast


class LedgerOperationMeta(enum.EnumMeta):
    """
    Custom metaclass for LedgerOperation to ensure required operations are present.
    """

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        # Skip validation for BaseLedgerOperation itself
        if name == "BaseLedgerOperation" or not bases:
            return super().__new__(mcs, name, bases, namespace)

        # Ensure all required operations are present
        required_operations = set(SharedLedgerOperation._member_names_)

        # Extract operations defined in the new enum
        defined_operations = {key for key in namespace if not key.startswith('_')}

        # Check if all required operations are defined
        missing_operations = required_operations - defined_operations
        if missing_operations:
            raise TypeError(
                f"LedgerOperation class '{name}' must define all shared operations: "
                f"Missing {', '.join(missing_operations)}"
            )

        return super().__new__(mcs, name, bases, namespace)


class BaseLedgerOperation(enum.Enum, metaclass=LedgerOperationMeta):
    """
    Base enum for all ledger operations.
    This class serves as a base for shared and application-specific operations.
    """

    @classmethod
    def get_operation_value(cls, operation_name: str) -> int:
        """
        Get the configured value for a ledger operation.

        Args:
            operation_name: The name of the operation to look up

        Returns:
            The value associated with the operation
        """
        from monorepo.core.ledgers.config import LEDGER_OPERATION_CONFIG
        return LEDGER_OPERATION_CONFIG.get(operation_name, 0)

    @classmethod
    def get_all_operations(cls) -> Set[str]:
        """
        Get all operation names as a set.

        Returns:
            Set of all operation names
        """
        return set(item.name for item in cls)

    @property
    def value_amount(self) -> int:
        """
        Returns the configured value amount for this operation.

        Returns:
            Integer amount associated with this operation
        """
        return self.__class__.get_operation_value(self.name)


class SharedLedgerOperation(enum.Enum):
    """
    Shared ledger operations that all applications must implement.
    """
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

TLedgerOperation = TypeVar('TLedgerOperation', bound=BaseLedgerOperation)
