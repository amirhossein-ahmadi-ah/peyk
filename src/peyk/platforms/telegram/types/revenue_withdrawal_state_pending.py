from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RevenueWithdrawalStatePending:
    """The withdrawal is in progress.

Attributes:
    type: Type of the state, always 'pending'"""
    type: str = 'pending'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['RevenueWithdrawalStatePending']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['RevenueWithdrawalStatePending']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'pending'))
