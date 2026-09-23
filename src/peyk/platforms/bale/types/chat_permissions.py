from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Dict, Optional


@dataclass
class ChatPermissions:
    """Describe what a non-administrator member may do in a chat.

    Used as the ``permissions`` argument of ``BaleClient.restrict_chat_member``.
    Fields left as ``None`` are not sent, so the server keeps its current value.

    Attributes:
        can_send_messages: Allowed to send text messages.
        can_send_media_messages: Allowed to send media (audio, documents, photos, videos, ...).
        can_send_other_messages: Allowed to send stickers, animations, etc.
        can_add_web_page_previews: Allowed to add web page previews to messages.
        can_change_info: Allowed to change the chat title, photo and other settings.
        can_invite_users: Allowed to invite new users to the chat.
        can_pin_messages: Allowed to pin messages.
    """
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatPermissions']:
        """Parse raw Bale data into ``ChatPermissions``.

        Args:
            data: Raw API object or ``None``.

        Returns:
            Parsed object or ``None``.
        """
        if data is None:
            return None
        return cls(**{f.name: data.get(f.name) for f in fields(cls)})

    def to_dict(self) -> Dict[str, object]:
        """Serialize to the Bale request shape, omitting unset (``None``) fields."""
        return {f.name: getattr(self, f.name) for f in fields(self) if getattr(self, f.name) is not None}
