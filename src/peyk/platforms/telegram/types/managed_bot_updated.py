from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ManagedBotUpdated:
    """This object contains information about the creation, token update, or owner update of a bot that is managed by the current bot.

Attributes:
    user: User that created the bot
    bot: Information about the bot. Token of the bot can be fetched using the method getManagedBotToken."""
    id: str = ''
    user: Optional[User] = None
    token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ManagedBotUpdated']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ManagedBotUpdated']``).\n        "
        if data is None:
            return None
        return cls(id=data.get('id', ''), user=User.from_dict(data.get('user')), token=data.get('token'))
