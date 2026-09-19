from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostDeclined:
    """Describes a service message about the rejection of a suggested post.

Attributes:
    suggested_post_message: Message containing the suggested post. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply.
    comment: Comment with which the post was declined"""
    suggested_post_message: Optional[Message] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuggestedPostDeclined']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuggestedPostDeclined']``).\n        "
        if data is None:
            return None
        return cls(suggested_post_message=Message.from_dict(data.get('suggested_post_message')), comment=data.get('comment'))
