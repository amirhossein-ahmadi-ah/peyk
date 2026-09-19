from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional
from .user import User

@dataclass
class ChatMember:
    """Base for chat-member subtypes.

    Bale documents four subtypes: ChatMemberOwner, ChatMemberAdministrator,
    ChatMemberMember, ChatMemberRestricted. Dispatch on the `status` field.
    """
    status: str
    user: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMember']:
        """Parse raw Bale data into ``ChatMember``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ChatMember]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        from .chat_member_restricted import ChatMemberRestricted
        from .chat_member_owner import ChatMemberOwner
        from .chat_member_member import ChatMemberMember
        from .chat_member_administrator import ChatMemberAdministrator
        if data is None:
            return None
        status = data.get('status', '')
        if status == 'creator':
            return ChatMemberOwner.from_dict(data)
        elif status == 'administrator':
            return ChatMemberAdministrator.from_dict(data)
        elif status == 'member':
            return ChatMemberMember.from_dict(data)
        elif status == 'restricted':
            return ChatMemberRestricted.from_dict(data)
        return cls(status=status, user=User.from_dict(data.get('user')))
