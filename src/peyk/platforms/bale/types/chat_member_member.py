from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .chat_member import ChatMember
from .user import User
@dataclass
class ChatMemberMember(ChatMember):
    """A chat member who has no additional privileges or restrictions."""

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberMember']:
        """Parse raw Bale data into ``ChatMemberMember``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ChatMemberMember]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(status='member', user=User.from_dict(data.get('user')))
