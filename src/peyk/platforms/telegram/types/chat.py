from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Chat:
    """This object represents a chat.

Attributes:
    id: Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    type: Type of the chat, can be either 'private', 'group', 'supergroup' or 'channel'
    title: Title, for supergroups, channels and group chats
    username: Username, for private chats, supergroups and channels if available
    first_name: First name of the other party in a private chat
    last_name: Last name of the other party in a private chat
    is_forum: True, if the supergroup chat is a forum (has topics enabled)
    is_direct_messages: True, if the chat is the direct messages chat of a channel
    accent_color_id: Identifier of the accent color for the chat name and backgrounds of the chat photo, reply header, and link preview. See accent colors for more details. Returned only in getChat. Always returned in getChat.
    active_usernames: If non-empty, the list of all active chat usernames; for private chats, supergroups and channels. Returned only in getChat.
    available_reactions: List of available reactions allowed in the chat. If omitted, then all emoji reactions are allowed. Returned only in getChat.
    background_custom_emoji_id: Custom emoji identifier of emoji chosen by the chat for the reply header and link preview background. Returned only in getChat.
    bio: Bio of the other party in a private chat. Returned only in getChat.
    birthdate: For private chats, the date of birth of the user. Returned only in getChat.
    business_intro: For private chats with business accounts, the intro of the business. Returned only in getChat.
    business_location: For private chats with business accounts, the location of the business. Returned only in getChat.
    business_opening_hours: For private chats with business accounts, the opening hours of the business. Returned only in getChat.
    can_set_sticker_set: True, if the bot can change the group sticker set. Returned only in getChat.
    custom_emoji_sticker_set_name: For supergroups, the name of the group's custom emoji sticker set. Custom emoji from this set can be used by all users and bots in the group. Returned only in getChat.
    description: Description, for groups, supergroups and channel chats. Returned only in getChat.
    emoji_status_custom_emoji_id: Custom emoji identifier of the emoji status of the chat or the other party in a private chat. Returned only in getChat.
    emoji_status_expiration_date: Expiration date of the emoji status of the chat or the other party in a private chat, in Unix time, if any. Returned only in getChat.
    has_aggressive_anti_spam_enabled: True, if aggressive anti-spam checks are enabled in the supergroup. The field is only available to chat administrators. Returned only in getChat.
    has_hidden_members: True, if non-administrators can only get the list of bots and administrators in the chat. Returned only in getChat.
    has_private_forwards: True, if privacy settings of the other party in the private chat allows to use tg://user?id= links only in chats with the user. Returned only in getChat.
    has_protected_content: True, if messages from the chat can't be forwarded to other chats. Returned only in getChat.
    has_restricted_voice_and_video_messages: True, if the privacy settings of the other party restrict sending voice and video note messages in the private chat. Returned only in getChat.
    has_visible_history: True, if new chat members will have access to old messages; available only to chat administrators. Returned only in getChat.
    invite_link: Primary invite link, for groups, supergroups and channel chats. Returned only in getChat.
    join_by_request: True, if all users directly joining the supergroup need to be approved by supergroup administrators. Returned only in getChat.
    join_to_send_messages: True, if users need to join the supergroup before they can send messages. Returned only in getChat.
    linked_chat_id: Unique identifier for the linked chat, i.e. the discussion group identifier for a channel and vice versa; for supergroups and channel chats. This identifier may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier. Returned only in getChat.
    location: For supergroups, the location to which the supergroup is connected. Returned only in getChat.
    message_auto_delete_time: The time after which all messages sent to the chat will be automatically deleted; in seconds. Returned only in getChat.
    permissions: Default chat member permissions, for groups and supergroups. Returned only in getChat.
    personal_chat: For private chats, the personal channel of the user. Returned only in getChat.
    photo: Chat photo. Returned only in getChat.
    pinned_message: The most recent pinned message (by sending date). Returned only in getChat.
    profile_accent_color_id: Identifier of the accent color for the chat's profile background. See profile accent colors for more details. Returned only in getChat.
    profile_background_custom_emoji_id: Custom emoji identifier of the emoji chosen by the chat for its profile background. Returned only in getChat.
    slow_mode_delay: For supergroups, the minimum allowed delay between consecutive messages sent by each unprivileged user; in seconds. Returned only in getChat.
    sticker_set_name: For supergroups, name of group sticker set. Returned only in getChat.
    unrestrict_boost_count: For supergroups, the minimum number of boosts that a non-administrator user needs to add in order to ignore slow mode and chat permissions. Returned only in getChat."""
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Chat']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(id=data['id'], type=data.get('type', ''), title=data.get('title'), username=data.get('username'), first_name=data.get('first_name'), last_name=data.get('last_name'), is_forum=data.get('is_forum'))
