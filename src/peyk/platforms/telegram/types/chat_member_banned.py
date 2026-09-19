from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .user import User

@dataclass
class ChatMemberBanned:
    """Represents a chat member that was banned in the chat and can't return to the chat or view chat messages.

Attributes:
    status: The member's status in the chat, always 'kicked'
    user: Information about the user
    until_date: Date when restrictions will be lifted for this user; Unix time. If 0, then the user is banned forever."""
    status: str = 'kicked'
    user: Optional[User] = None
    until_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberBanned']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(status=data.get('status', 'kicked'), user=User.from_dict(data.get('user')), until_date=data.get('until_date'))
