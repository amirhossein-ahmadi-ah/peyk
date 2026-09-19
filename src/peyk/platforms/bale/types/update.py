from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional
from .callback_query import CallbackQuery
from .message import Message
from .pre_checkout_query import PreCheckoutQuery

@dataclass
class Update:
    """Represent the Bale Bot API ``Update`` object.

Preserves the existing dataclass fields and parsing behavior."""
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Update':
        """Parse raw Bale data into ``Update``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Update]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        return cls(update_id=data['update_id'], message=Message.from_dict(data.get('message')), edited_message=Message.from_dict(data.get('edited_message')), callback_query=CallbackQuery.from_dict(data.get('callback_query')), pre_checkout_query=PreCheckoutQuery.from_dict(data.get('pre_checkout_query')))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> List['Update']:
        """Performs the list from result operation for the Bale client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
        "Parse the array `getUpdates` returns from a raw `result` list.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``List['Update']``).\n        "
        return [cls.from_dict(item) for item in data or []]
