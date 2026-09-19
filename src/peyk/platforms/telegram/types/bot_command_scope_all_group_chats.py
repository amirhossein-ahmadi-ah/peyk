from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotCommandScopeAllGroupChats:
    """Represents the scope of bot commands, covering all group and supergroup chats.

Attributes:
    type: Scope type, must be all_group_chats"""
    type: str = 'all_group_chats'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotCommandScopeAllGroupChats']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotCommandScopeAllGroupChats']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'all_group_chats'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'type': self.type}
