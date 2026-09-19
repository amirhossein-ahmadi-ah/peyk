from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostPrice:
    """Describes the price of a suggested post.

Attributes:
    currency: Currency in which the post will be paid. Currently, must be one of 'XTR' for Telegram Stars or 'TON' for TON grams.
    amount: The amount of the currency that will be paid for the post in the smallest units of the currency, i.e. Telegram Stars or nanograms. Currently, price in Telegram Stars must be between 5 and 100000, and price in nanograms must be between 10000000 and 10000000000000."""
    label: str = ''
    amount: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuggestedPostPrice']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuggestedPostPrice']``).\n        "
        if data is None:
            return None
        return cls(label=data.get('label', ''), amount=data.get('amount', 0))
