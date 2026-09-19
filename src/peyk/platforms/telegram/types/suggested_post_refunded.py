from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostRefunded:
    """Describes a service message about a payment refund for a suggested post.

Attributes:
    reason: Reason for the refund. Currently, one of 'post_deleted' if the post was deleted within 24 hours of being posted or removed from scheduled messages without being posted, or 'payment_refunded' if the payer refunded their payment.
    suggested_post_message: Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    suggested_post_message: Optional[Message] = None
    price: Optional[object] = None
    reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuggestedPostRefunded']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuggestedPostRefunded']``).\n        "
        if data is None:
            return None
        return cls(suggested_post_message=Message.from_dict(data.get('suggested_post_message')), price=data.get('price'), reason=data.get('reason'))
