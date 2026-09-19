from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UsersShared:
    """This object contains information about the users whose identifiers were shared with the bot using a KeyboardButtonRequestUsers button.

Attributes:
    request_id: Identifier of the request
    users: Information about users shared with the bot
    user_ids: Identifiers of the shared users. These numbers may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting them. But they have at most 52 significant bits, so 64-bit integers or double-precision float types are safe for storing these identifiers. The bot may not have access to the users and could be unable to use these identifiers, unless the users are already known to the bot by some other means."""
    request_id: int = 0
    users: Optional[List[SharedUser]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UsersShared']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UsersShared']``).\n        "
        if data is None:
            return None
        return cls(request_id=data.get('request_id', 0), users=[SharedUser.from_dict(u) for u in data.get('users', [])] if data.get('users') else None)
