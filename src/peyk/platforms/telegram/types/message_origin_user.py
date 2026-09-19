from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MessageOriginUser:
    """The message was originally sent by a known user.

Attributes:
    type: Type of the message origin, always 'user'
    date: Date the message was sent originally in Unix time
    sender_user: User that sent the message originally"""
    type: str = 'user'
    date: int = 0
    sender_user: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageOriginUser']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MessageOriginUser']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'user'), date=data.get('date', 0), sender_user=User.from_dict(data.get('sender_user')))
