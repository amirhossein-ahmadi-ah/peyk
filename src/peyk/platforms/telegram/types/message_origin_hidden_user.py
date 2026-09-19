from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MessageOriginHiddenUser:
    """The message was originally sent by an unknown user.

Attributes:
    type: Type of the message origin, always 'hidden_user'
    date: Date the message was sent originally in Unix time
    sender_user_name: Name of the user that sent the message originally"""
    type: str = 'hidden_user'
    date: int = 0
    sender_user_name: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageOriginHiddenUser']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MessageOriginHiddenUser']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'hidden_user'), date=data.get('date', 0), sender_user_name=data.get('sender_user_name', ''))
