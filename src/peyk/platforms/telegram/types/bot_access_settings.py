from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotAccessSettings:
    """This object describes the access settings of a bot.

Attributes:
    is_access_restricted: True, if only selected users can access the bot. The bot's owner can always access it.
    added_users: The list of other users who have access to the bot if the access is restricted"""
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
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotAccessSettings']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotAccessSettings']``).\n        "
        if data is None:
            return None
        return cls(**{f: data.get(f) for f in ('can_send_messages', 'can_send_audios', 'can_send_documents', 'can_send_photos', 'can_send_videos', 'can_send_video_notes', 'can_send_voice_notes', 'can_send_polls', 'can_send_other_messages', 'can_add_web_page_previews', 'can_change_info', 'can_invite_users', 'can_pin_messages', 'can_manage_topics')})
