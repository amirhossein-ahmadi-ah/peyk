from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ManagedBotCreated:
    """This object contains information about the bot that was created to be managed by the current bot.

Attributes:
    bot: Information about the bot. The bot's token can be fetched using the method getManagedBotToken."""
    id: str = ''
    user: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ManagedBotCreated']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ManagedBotCreated']``).\n        "
        if data is None:
            return None
        return cls(id=data.get('id', ''), user=User.from_dict(data.get('user')))
