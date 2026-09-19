from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .chat_member import ChatMember
from .user import User
@dataclass
class ChatMemberOwner(ChatMember):
    """A chat member who owns the chat and has all administrator privileges."""

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberOwner']:
        """Parse raw Bale data into ``ChatMemberOwner``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ChatMemberOwner]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(status='creator', user=User.from_dict(data.get('user')))
