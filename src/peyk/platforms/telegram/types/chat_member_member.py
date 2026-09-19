from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .user import User

@dataclass
class ChatMemberMember:
    """Represents a chat member that has no additional privileges or restrictions.

Attributes:
    status: The member's status in the chat, always 'member'
    user: Information about the user
    tag: Tag of the member
    until_date: Date when the user's subscription will expire; Unix time"""
    status: str = 'member'
    user: Optional[User] = None
    tag: Optional[str] = None
    until_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberMember']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(status=data.get('status', 'member'), user=User.from_dict(data.get('user')), tag=data.get('tag'), until_date=data.get('until_date'))
