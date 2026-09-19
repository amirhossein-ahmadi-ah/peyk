from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MessageOriginChat:
    """The message was originally sent on behalf of a chat to a group chat.

Attributes:
    type: Type of the message origin, always 'chat'
    date: Date the message was sent originally in Unix time
    sender_chat: Chat that sent the message originally
    author_signature: For messages originally sent by an anonymous chat administrator, original message author signature"""
    type: str = 'chat'
    date: int = 0
    sender_chat: Optional[Chat] = None
    author_signature: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageOriginChat']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MessageOriginChat']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'chat'), date=data.get('date', 0), sender_chat=Chat.from_dict(data.get('sender_chat')), author_signature=data.get('author_signature'))
