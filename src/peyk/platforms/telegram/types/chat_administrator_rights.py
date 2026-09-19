from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatAdministratorRights:
    """Represents the rights of an administrator in a chat.

Attributes:
    is_anonymous: True, if the user's presence in the chat is hidden
    can_manage_chat: True, if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege.
    can_delete_messages: True, if the administrator can delete messages of other users
    can_manage_video_chats: True, if the administrator can manage video chats
    can_restrict_members: True, if the administrator can restrict, ban or unban chat members, or access supergroup statistics
    can_promote_members: True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by the user)
    can_change_info: True, if the user is allowed to change the chat title, photo and other settings
    can_invite_users: True, if the user is allowed to invite new users to the chat
    can_post_stories: True, if the administrator can post stories to the chat
    can_edit_stories: True, if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive
    can_delete_stories: True, if the administrator can delete stories posted by other users
    can_post_messages: True, if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only
    can_edit_messages: True, if the administrator can edit messages of other users and can pin messages; for channels only
    can_pin_messages: True, if the user is allowed to pin messages; for groups and supergroups only
    can_manage_topics: True, if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only
    can_manage_direct_messages: True, if the administrator can manage direct messages of the channel and decline suggested posts; for channels only
    can_manage_tags: True, if the administrator can edit the tags of regular members; for groups and supergroups only. If omitted, defaults to the value of can_pin_messages."""
    is_anonymous: Optional[bool] = None
    can_manage_chat: Optional[bool] = None
    can_delete_messages: Optional[bool] = None
    can_manage_video_chats: Optional[bool] = None
    can_restrict_members: Optional[bool] = None
    can_promote_members: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_post_stories: Optional[bool] = None
    can_edit_stories: Optional[bool] = None
    can_delete_stories: Optional[bool] = None
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    can_manage_direct_messages: Optional[bool] = None
    can_manage_tags: Optional[bool] = None
    can_send_welcome_messages: Optional[bool] = None
    _FIELDS = ('is_anonymous', 'can_manage_chat', 'can_delete_messages', 'can_manage_video_chats', 'can_restrict_members', 'can_promote_members', 'can_change_info', 'can_invite_users', 'can_post_stories', 'can_edit_stories', 'can_delete_stories', 'can_post_messages', 'can_edit_messages', 'can_pin_messages', 'can_manage_topics', 'can_manage_direct_messages', 'can_manage_tags', 'can_send_welcome_messages')

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatAdministratorRights']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(**{f: data.get(f) for f in cls._FIELDS})

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.

Returns:
    A JSON-compatible mapping representing this value."""
        return {f: v for f in self._FIELDS if (v := getattr(self, f)) is not None}
