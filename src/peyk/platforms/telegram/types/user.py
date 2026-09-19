from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class User:
    """This object represents a Telegram user or bot.

Attributes:
    id: Unique identifier for this user or bot. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
    is_bot: True, if this user is a bot
    first_name: User's or bot's first name
    last_name: User's or bot's last name
    username: User's or bot's username
    language_code: IETF language tag of the user's language
    is_premium: True, if this user is a Telegram Premium user
    added_to_attachment_menu: True, if this user added the bot to the attachment menu
    can_join_groups: True, if the bot can be invited to groups. Returned only in getMe.
    can_read_all_group_messages: True, if privacy mode is disabled for the bot. Returned only in getMe.
    supports_guest_queries: True, if the bot supports guest queries from chats it is not a member of. Returned only in getMe.
    supports_inline_queries: True, if the bot supports inline queries. Returned only in getMe.
    can_connect_to_business: True, if the bot can be connected to a user account to manage it. Returned only in getMe.
    has_main_web_app: True, if the bot has a main Web App. Returned only in getMe.
    has_topics_enabled: True, if the bot has forum topic mode enabled in private chats. Returned only in getMe.
    allows_users_to_create_topics: True, if the bot allows users to create and delete topics in private chats. Returned only in getMe.
    can_manage_bots: True, if other bots can be created to be controlled by the bot. Returned only in getMe.
    supports_join_request_queries: True, if the bot supports join request queries and can be assigned to process them. Returned only in getMe."""
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None
    can_connect_to_business: Optional[bool] = None
    has_main_web_app: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['User']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(id=data['id'], is_bot=data.get('is_bot', False), first_name=data.get('first_name', ''), last_name=data.get('last_name'), username=data.get('username'), language_code=data.get('language_code'), is_premium=data.get('is_premium'), added_to_attachment_menu=data.get('added_to_attachment_menu'), can_join_groups=data.get('can_join_groups'), can_read_all_group_messages=data.get('can_read_all_group_messages'), supports_inline_queries=data.get('supports_inline_queries'), can_connect_to_business=data.get('can_connect_to_business'), has_main_web_app=data.get('has_main_web_app'))
