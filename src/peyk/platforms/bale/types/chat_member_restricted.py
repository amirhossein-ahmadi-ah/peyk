from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .chat_member import ChatMember
from .user import User
@dataclass
class ChatMemberRestricted(ChatMember):
    """A chat member who is under certain restrictions in the chat."""
    is_member: Optional[bool] = None
    can_send_messages: Optional[bool] = None
    can_send_audios: Optional[bool] = None
    can_send_documents: Optional[bool] = None
    can_send_photos: Optional[bool] = None
    can_send_videos: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberRestricted']:
        """Parse raw Bale data into ``ChatMemberRestricted``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ChatMemberRestricted]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(status='restricted', user=User.from_dict(data.get('user')), is_member=data.get('is_member'), can_send_messages=data.get('can_send_messages'), can_send_audios=data.get('can_send_audios'), can_send_documents=data.get('can_send_documents'), can_send_photos=data.get('can_send_photos'), can_send_videos=data.get('can_send_videos'), can_change_info=data.get('can_change_info'), can_invite_users=data.get('can_invite_users'), can_pin_messages=data.get('can_pin_messages'))
