from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PaidMessagePriceChanged:
    """Describes a service message about a change in the price of paid messages within a chat.

Attributes:
    paid_message_star_count: The new number of Telegram Stars that must be paid by non-administrator users of the supergroup chat for each sent message"""
    paid_message_star_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PaidMessagePriceChanged']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PaidMessagePriceChanged']``).\n        "
        if data is None:
            return None
        return cls(paid_message_star_count=data.get('paid_message_star_count'))
