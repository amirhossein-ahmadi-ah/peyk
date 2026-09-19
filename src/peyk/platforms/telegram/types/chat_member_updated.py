from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .chat import Chat
from .chat_member import parse_chat_member
from .chat_invite_link import ChatInviteLink
from .user import User

@dataclass
class ChatMemberUpdated:
    """This object represents changes in the status of a chat member.

Attributes:
    chat: Chat the user belongs to
    from: Performer of the action, which resulted in the change
    date: Date the change was done in Unix time
    old_chat_member: Previous information about the chat member
    new_chat_member: New information about the chat member
    invite_link: Chat invite link, which was used by the user to join the chat; for joining by invite link events only
    via_join_request: True, if the user joined the chat after sending a direct join request without using an invite link and being approved by an administrator
    via_chat_folder_invite_link: True, if the user joined the chat via a chat folder invite link"""
    chat: Chat
    from_: Optional[User] = None
    date: Optional[int] = None
    old_chat_member: Optional[ChatMember] = None
    new_chat_member: Optional[ChatMember] = None
    invite_link: Optional['ChatInviteLink'] = None
    via_join_request: Optional[bool] = None
    via_chat_folder_invite_link: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberUpdated']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(chat=Chat.from_dict(data.get('chat', {})), from_=User.from_dict(data.get('from')), date=data.get('date'), old_chat_member=parse_chat_member(data.get('old_chat_member')), new_chat_member=parse_chat_member(data.get('new_chat_member')), invite_link=ChatInviteLink.from_dict(data.get('invite_link')), via_join_request=data.get('via_join_request'), via_chat_folder_invite_link=data.get('via_chat_folder_invite_link'))
