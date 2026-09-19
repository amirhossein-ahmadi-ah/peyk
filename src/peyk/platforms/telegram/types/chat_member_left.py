from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .user import User

@dataclass
class ChatMemberLeft:
    """Represents a chat member that isn't currently a member of the chat, but may join it themselves.

Attributes:
    status: The member's status in the chat, always 'left'
    user: Information about the user"""
    status: str = 'left'
    user: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberLeft']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(status=data.get('status', 'left'), user=User.from_dict(data.get('user')))
