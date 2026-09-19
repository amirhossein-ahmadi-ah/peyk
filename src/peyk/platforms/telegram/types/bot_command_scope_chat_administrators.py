from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotCommandScopeChatAdministrators:
    """Represents the scope of bot commands, covering all administrators of a specific group or supergroup chat.

Attributes:
    type: Scope type, must be chat_administrators
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username. Channel direct messages chats and channel chats aren't supported."""
    type: str = 'chat_administrators'
    chat_id: Union[int, str] = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotCommandScopeChatAdministrators']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotCommandScopeChatAdministrators']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'chat_administrators'), chat_id=data.get('chat_id', 0))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'type': self.type, 'chat_id': self.chat_id}
