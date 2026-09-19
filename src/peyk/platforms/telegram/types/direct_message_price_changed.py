from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class DirectMessagePriceChanged:
    """Describes a service message about a change in the price of direct messages sent to a channel chat.

Attributes:
    are_direct_messages_enabled: True, if direct messages are enabled for the channel chat; False otherwise
    direct_message_star_count: The new number of Telegram Stars that must be paid by users for each direct message sent to the channel. Does not apply to users who have been exempted by administrators. Defaults to 0."""
    is_paid_direct_messages: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['DirectMessagePriceChanged']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['DirectMessagePriceChanged']``).\n        "
        if data is None:
            return None
        return cls(is_paid_direct_messages=data.get('is_paid_direct_messages'))
