"""
Configuration for ledger operations.
"""
from typing import Dict

# Configuration for ledger operations and their associated credit values
LEDGER_OPERATION_CONFIG: Dict[str, int] = {
    # Shared operations
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,

    # App-specific operations - These should be defined by each application
    # but are included here for reference
    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
}