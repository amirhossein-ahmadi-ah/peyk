from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatShared:
    """This object contains information about a chat that was shared with the bot using a KeyboardButtonRequestChat button.

Attributes:
    request_id: Identifier of the request
    chat_id: Identifier of the shared chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier. The bot may not have access to the chat and could be unable to use this identifier, unless the chat is already known to the bot by some other means.
    title: Title of the chat, if the title was requested by the bot
    username: Username of the chat, if the username was requested by the bot and available
    photo: Available sizes of the chat photo, if the photo was requested by the bot"""
    request_id: int = 0
    chat_id: int = 0
    title: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatShared']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatShared']``).\n        "
        if data is None:
            return None
        return cls(request_id=data.get('request_id', 0), chat_id=data.get('chat_id', 0), title=data.get('title'), username=data.get('username'), photo=PhotoSize.list_from(data.get('photo')))
