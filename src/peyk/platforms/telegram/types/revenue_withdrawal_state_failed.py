from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RevenueWithdrawalStateFailed:
    """The withdrawal failed and the transaction was refunded.

Attributes:
    type: Type of the state, always 'failed'"""
    type: str = 'failed'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['RevenueWithdrawalStateFailed']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['RevenueWithdrawalStateFailed']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'failed'))
