from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .chat import Chat

@dataclass
class InaccessibleMessage:
    """This object describes a message that was deleted or is otherwise inaccessible to the bot.

Attributes:
    chat: Chat the message belonged to
    message_id: Unique message identifier inside the chat
    date: Always 0. The field can be used to differentiate regular and inaccessible messages."""
    chat: Chat
    message_id: int
    date: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InaccessibleMessage']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(chat=Chat.from_dict(data.get('chat', {})), message_id=data['message_id'], date=data.get('date', 0))

def parse_maybe_inaccessible_message(data: Optional[dict]):
    """Provides the parse maybe inaccessible message operation for the Telegram integration.

Args:
    data: Value used by this operation."""
    'Parse a message, selecting ``InaccessibleMessage`` when ``date`` is zero.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Any``).\n    '
    if data is None:
        return None
    if data.get('date') == 0:
        return InaccessibleMessage.from_dict(data)
    from .message import Message
    return Message.from_dict(data)
