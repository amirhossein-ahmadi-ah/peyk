from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatPermissions:
    """Describes actions that a non-administrator user is allowed to take in a chat.

Attributes:
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
    can_react_to_messages: True, if the user is allowed to react to messages. If omitted, defaults to the value of can_send_messages.
    can_edit_tag: True, if the user is allowed to edit their own tag. If omitted, defaults to the value of can_pin_messages.
    can_change_info: True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups.
    can_invite_users: True, if the user is allowed to invite new users to the chat
    can_pin_messages: True, if the user is allowed to pin messages. Ignored in public supergroups.
    can_manage_topics: True, if the user is allowed to create forum topics. If omitted, defaults to the value of can_pin_messages."""
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

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatPermissions']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(**{f: data.get(f) for f in ('can_send_messages', 'can_send_audios', 'can_send_documents', 'can_send_photos', 'can_send_videos', 'can_send_video_notes', 'can_send_voice_notes', 'can_send_polls', 'can_send_other_messages', 'can_add_web_page_previews', 'can_react_to_messages', 'can_edit_tag', 'can_change_info', 'can_invite_users', 'can_pin_messages', 'can_manage_topics')})

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.

Returns:
    A JSON-compatible mapping representing this value."""
        return {f: v for f in ('can_send_messages', 'can_send_audios', 'can_send_documents', 'can_send_photos', 'can_send_videos', 'can_send_video_notes', 'can_send_voice_notes', 'can_send_polls', 'can_send_other_messages', 'can_add_web_page_previews', 'can_react_to_messages', 'can_edit_tag', 'can_change_info', 'can_invite_users', 'can_pin_messages', 'can_manage_topics') if (v := getattr(self, f)) is not None}
