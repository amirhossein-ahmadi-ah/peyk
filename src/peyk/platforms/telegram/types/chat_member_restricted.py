from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .user import User

@dataclass
class ChatMemberRestricted:
    """Represents a chat member that is under certain restrictions in the chat. Supergroups only.

Attributes:
    status: The member's status in the chat, always 'restricted'
    user: Information about the user
    is_member: True, if the user is a member of the chat at the moment of the request
    can_send_messages: True, if the user is allowed to send text messages, rich messages, contacts, giveaways, giveaway winners, invoices, locations and venues
    can_send_audios: True, if the user is allowed to send audios
    can_send_documents: True, if the user is allowed to send documents
    can_send_photos: True, if the user is allowed to send photos
    can_send_videos: True, if the user is allowed to send videos
    can_send_video_notes: True, if the user is allowed to send video notes
    can_send_voice_notes: True, if the user is allowed to send voice notes
    can_send_polls: True, if the user is allowed to send polls and checklists
    can_send_other_messages: True, if the user is allowed to send animations, games, stickers and use inline bots
    can_add_web_page_previews: True, if the user is allowed to add web page previews to their messages
    can_react_to_messages: True, if the user is allowed to react to messages
    can_edit_tag: True, if the user is allowed to edit their own tag
    can_change_info: True, if the user is allowed to change the chat title, photo and other settings
    can_invite_users: True, if the user is allowed to invite new users to the chat
    can_pin_messages: True, if the user is allowed to pin messages
    can_manage_topics: True, if the user is allowed to create forum topics
    until_date: Date when restrictions will be lifted for this user; Unix time. If 0, then the user is restricted forever.
    tag: Tag of the member"""
    status: str = 'restricted'
    user: Optional[User] = None
    tag: Optional[str] = None
    is_member: Optional[bool] = None
    can_send_messages: Optional[bool] = None
    can_send_audios: Optional[bool] = None
    can_send_documents: Optional[bool] = None
    can_send_photos: Optional[bool] = None
    can_send_videos: Optional[bool] = None
    can_send_video_notes: Optional[bool] = None
    can_send_voice_notes: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_react_to_messages: Optional[bool] = None
    can_edit_tag: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    until_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatMemberRestricted']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(status=data.get('status', 'restricted'), user=User.from_dict(data.get('user')), tag=data.get('tag'), is_member=data.get('is_member'), can_send_messages=data.get('can_send_messages'), can_send_audios=data.get('can_send_audios'), can_send_documents=data.get('can_send_documents'), can_send_photos=data.get('can_send_photos'), can_send_videos=data.get('can_send_videos'), can_send_video_notes=data.get('can_send_video_notes'), can_send_voice_notes=data.get('can_send_voice_notes'), can_send_polls=data.get('can_send_polls'), can_send_other_messages=data.get('can_send_other_messages'), can_add_web_page_previews=data.get('can_add_web_page_previews'), can_react_to_messages=data.get('can_react_to_messages'), can_edit_tag=data.get('can_edit_tag'), can_change_info=data.get('can_change_info'), can_invite_users=data.get('can_invite_users'), can_pin_messages=data.get('can_pin_messages'), can_manage_topics=data.get('can_manage_topics'), until_date=data.get('until_date'))
