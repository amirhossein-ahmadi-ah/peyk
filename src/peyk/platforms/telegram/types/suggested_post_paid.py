from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostPaid:
    """Describes a service message about a successful payment for a suggested post.

Attributes:
    currency: Currency in which the payment was made. Currently, one of 'XTR' for Telegram Stars or 'TON' for TON grams.
    suggested_post_message: Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply.
    amount: The amount of the currency that was received by the channel in nanograms; for payments in TON grams only
    star_amount: The amount of Telegram Stars that was received by the channel; for payments in Telegram Stars only"""
    suggested_post_message: Optional[Message] = None
    price: Optional[object] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuggestedPostPaid']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuggestedPostPaid']``).\n        "
        if data is None:
            return None
        return cls(suggested_post_message=Message.from_dict(data.get('suggested_post_message')), price=data.get('price'))
