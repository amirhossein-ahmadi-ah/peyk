from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BusinessConnection:
    """Describes the connection of the bot with a business account.

Attributes:
    id: Unique identifier of the business connection
    user: Business account user that created the business connection
    user_chat_id: Identifier of a private chat with the user who created the business connection. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
    date: Date the connection was established in Unix time
    is_enabled: True, if the connection is active
    rights: Rights of the business bot
    can_reply: True, if the bot can act on behalf of the business account in chats that were active in the last 24 hours"""
    id: str
    user: User
    user_chat_id: int
    date: int
    is_enabled: bool
    rights: Optional[BusinessBotRights] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BusinessConnection']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BusinessConnection']``).\n        "
        if data is None:
            return None
        return cls(id=_parse_api_value('String', data.get('id')), user=_parse_api_value('User', data.get('user')), user_chat_id=_parse_api_value('Integer', data.get('user_chat_id')), date=_parse_api_value('Integer', data.get('date')), is_enabled=_parse_api_value('Boolean', data.get('is_enabled')), rights=_parse_api_value('BusinessBotRights', data.get('rights')))
