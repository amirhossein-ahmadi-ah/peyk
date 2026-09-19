from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RevenueWithdrawalStateSucceeded:
    """The withdrawal succeeded.

Attributes:
    type: Type of the state, always 'succeeded'
    date: Date the withdrawal was completed in Unix time
    url: An HTTPS URL that can be used to see transaction details"""
    type: str = 'succeeded'
    date: int = 0
    url: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['RevenueWithdrawalStateSucceeded']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['RevenueWithdrawalStateSucceeded']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'succeeded'), date=data.get('date', 0), url=data.get('url', ''))
