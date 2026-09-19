from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MessageOriginChannel:
    """The message was originally sent to a channel chat.

Attributes:
    type: Type of the message origin, always 'channel'
    date: Date the message was sent originally in Unix time
    chat: Channel chat to which the message was originally sent
    message_id: Unique message identifier inside the chat
    author_signature: Signature of the original post author"""
    type: str = 'channel'
    date: int = 0
    chat: Optional[Chat] = None
    message_id: Optional[int] = None
    author_signature: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageOriginChannel']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MessageOriginChannel']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'channel'), date=data.get('date', 0), chat=Chat.from_dict(data.get('chat')), message_id=data.get('message_id'), author_signature=data.get('author_signature'))
