from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostApprovalFailed:
    """Describes a service message about the failed approval of a suggested post. Currently, only caused by insufficient user funds at the time of approval.

Attributes:
    price: Expected price of the post
    suggested_post_message: Message containing the suggested post whose approval has failed. Note that the Message object in this field will not contain the reply_to_message field even if it itself is a reply."""
    suggested_post_message: Optional[Message] = None
    price: Optional[object] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuggestedPostApprovalFailed']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuggestedPostApprovalFailed']``).\n        "
        if data is None:
            return None
        return cls(suggested_post_message=Message.from_dict(data.get('suggested_post_message')), price=data.get('price'))
