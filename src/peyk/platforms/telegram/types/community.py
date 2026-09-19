from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Community:
    """Represents a community (a group of chats).

Attributes:
    id: Unique identifier for this community. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    name: Name of the community"""
    id: int = 0
    title: str = ''
    bot: Optional[User] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Community']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Community']``).\n        "
        if data is None:
            return None
        return cls(id=data.get('id', 0), title=data.get('title', data.get('name', '')), bot=User.from_dict(data.get('bot')), name=data.get('name'))
