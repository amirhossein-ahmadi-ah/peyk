from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BusinessMessagesDeleted:
    """This object is received when messages are deleted from a connected business account.

Attributes:
    business_connection_id: Unique identifier of the business connection
    chat: Information about a chat in the business account. The bot may not have access to the chat or the corresponding user.
    message_ids: The list of identifiers of deleted messages in the chat of the business account"""
    business_connection_id: str
    chat: Chat
    message_ids: List[int]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BusinessMessagesDeleted']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BusinessMessagesDeleted']``).\n        "
        if data is None:
            return None
        return cls(business_connection_id=_parse_api_value('String', data.get('business_connection_id')), chat=_parse_api_value('Chat', data.get('chat')), message_ids=_parse_api_value('Array of Integer', data.get('message_ids')))
