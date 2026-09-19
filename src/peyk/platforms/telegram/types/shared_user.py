from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SharedUser:
    """This object contains information about a user that was shared with the bot using a KeyboardButtonRequestUsers button.

Attributes:
    user_id: Identifier of the shared user. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so 64-bit integers or double-precision float types are safe for storing these identifiers. The bot may not have access to the user and could be unable to use this identifier, unless the user is already known to the bot by some other means.
    first_name: First name of the user, if the name was requested by the bot
    last_name: Last name of the user, if the name was requested by the bot
    username: Username of the user, if the username was requested by the bot
    photo: Available sizes of the chat photo, if the photo was requested by the bot"""
    user_id: int = 0
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SharedUser']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SharedUser']``).\n        "
        if data is None:
            return None
        return cls(user_id=data.get('user_id', 0), first_name=data.get('first_name'), last_name=data.get('last_name'), username=data.get('username'), photo=PhotoSize.list_from(data.get('photo')))
