from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotCommandScopeAllPrivateChats:
    """Represents the scope of bot commands, covering all private chats.

Attributes:
    type: Scope type, must be all_private_chats"""
    type: str = 'all_private_chats'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotCommandScopeAllPrivateChats']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotCommandScopeAllPrivateChats']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'all_private_chats'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'type': self.type}
