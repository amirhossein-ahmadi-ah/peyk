from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class CommunityChatAdded:
    """Describes a service message about a chat being added to a community.

Attributes:
    community: The new community to which the chat belongs"""
    chat_id: int = 0
    community: Optional[Community] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['CommunityChatAdded']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['CommunityChatAdded']``).\n        "
        if data is None:
            return None
        return cls(chat_id=data.get('chat_id', 0), community=Community.from_dict(data.get('community')))
