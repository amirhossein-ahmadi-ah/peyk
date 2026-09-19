from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostApproved:
    """Describes a service message about the approval of a suggested post.

Attributes:
    send_date: Date when the post will be published
    suggested_post_message: Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply.
    price: Amount paid for the post"""
    suggested_post_message: Optional[Message] = None
    price: Optional[object] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuggestedPostApproved']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuggestedPostApproved']``).\n        "
        if data is None:
            return None
        return cls(suggested_post_message=Message.from_dict(data.get('suggested_post_message')), price=data.get('price'))
