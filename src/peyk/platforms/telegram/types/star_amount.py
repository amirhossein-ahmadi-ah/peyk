from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StarAmount:
    """Describes an amount of Telegram Stars.

Attributes:
    amount: Integer amount of Telegram Stars, rounded to 0; can be negative
    nanostar_amount: The number of 1/1000000000 shares of Telegram Stars; from -999999999 to 999999999; can be negative if and only if amount is non-positive"""
    amount: int
    nanostar_amount: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StarAmount']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StarAmount']``).\n        "
        if data is None:
            return None
        return cls(amount=_parse_api_value('Integer', data.get('amount')), nanostar_amount=_parse_api_value('Integer', data.get('nanostar_amount')))
