from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .user import User

@dataclass
class ChatMemberOwner:
    """Represents a chat member that owns the chat and has all administrator privileges.

Attributes:
    status: The member's status in the chat, always 'creator'
    user: Information about the user
    is_anonymous: True, if the user's presence in the chat is hidden
    custom_title: Custom title for this user"""
    status: str = 'creator'
    user: Optional[User] = None
    is_anonymous: Optional[bool] = None
    custom_title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberOwner']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(status=data.get('status', 'creator'), user=User.from_dict(data.get('user')), is_anonymous=data.get('is_anonymous'), custom_title=data.get('custom_title'))
