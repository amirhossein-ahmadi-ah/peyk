from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .chat_member import ChatMember
from .user import User
@dataclass
class ChatMemberAdministrator(ChatMember):
    """A chat member who has some additional administrator privileges."""
    can_delete_messages: Optional[bool] = None
    can_manage_video_chats: Optional[bool] = None
    can_restrict_members: Optional[bool] = None
    can_promote_members: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_post_stories: Optional[bool] = None
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberAdministrator']:
        """Parse raw Bale data into ``ChatMemberAdministrator``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ChatMemberAdministrator]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(status='administrator', user=User.from_dict(data.get('user')), can_delete_messages=data.get('can_delete_messages'), can_manage_video_chats=data.get('can_manage_video_chats'), can_restrict_members=data.get('can_restrict_members'), can_promote_members=data.get('can_promote_members'), can_change_info=data.get('can_change_info'), can_invite_users=data.get('can_invite_users'), can_post_stories=data.get('can_post_stories'), can_post_messages=data.get('can_post_messages'), can_edit_messages=data.get('can_edit_messages'), can_pin_messages=data.get('can_pin_messages'))
