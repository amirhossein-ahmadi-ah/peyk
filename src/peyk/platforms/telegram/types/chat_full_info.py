from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .chat_photo import ChatPhoto
from .message import Message

@dataclass
class ChatFullInfo:
    """This object contains full information about a chat.

Attributes:
    id: Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    type: Type of the chat, can be either 'private', 'group', 'supergroup' or 'channel'
    accent_color_id: Identifier of the accent color for the chat name and backgrounds of the chat photo, reply header, and link preview. See accent colors for more details.
    max_reaction_count: The maximum number of reactions that can be set on a message in the chat
    accepted_gift_types: Information about types of gifts that are accepted by the chat or by the corresponding user for private chats
    title: Title, for supergroups, channels and group chats
    username: Username, for private chats, supergroups and channels if available
    first_name: First name of the other party in a private chat
    last_name: Last name of the other party in a private chat
    is_forum: True, if the supergroup chat is a forum (has topics enabled)
    is_direct_messages: True, if the chat is the direct messages chat of a channel
    photo: Chat photo
    active_usernames: If non-empty, the list of all active chat usernames; for private chats, supergroups and channels
    birthdate: For private chats, the date of birth of the user
    business_intro: For private chats with business accounts, the intro of the business
    business_location: For private chats with business accounts, the location of the business
    business_opening_hours: For private chats with business accounts, the opening hours of the business
    personal_chat: For private chats, the personal channel of the user
    parent_chat: Information about the corresponding channel chat; for direct messages chats only
    available_reactions: List of available reactions allowed in the chat. If omitted, then all emoji reactions are allowed.
    background_custom_emoji_id: Custom emoji identifier of the emoji chosen by the chat for the reply header and link preview background
    profile_accent_color_id: Identifier of the accent color for the chat's profile background. See profile accent colors for more details.
    profile_background_custom_emoji_id: Custom emoji identifier of the emoji chosen by the chat for its profile background
    emoji_status_custom_emoji_id: Custom emoji identifier of the emoji status of the chat or the other party in a private chat
    emoji_status_expiration_date: Expiration date of the emoji status of the chat or the other party in a private chat, in Unix time, if any
    bio: Bio of the other party in a private chat
    has_private_forwards: True, if privacy settings of the other party in the private chat allows to use tg://user?id= links only in chats with the user
    has_restricted_voice_and_video_messages: True, if the privacy settings of the other party restrict sending voice and video note messages in the private chat
    join_to_send_messages: True, if users need to join the supergroup before they can send messages
    join_by_request: True, if all users directly joining the supergroup without using an invite link need to be approved by supergroup administrators
    description: Description, for groups, supergroups and channel chats
    invite_link: Primary invite link, for groups, supergroups and channel chats
    pinned_message: The most recent pinned message (by sending date)
    permissions: Default chat member permissions, for groups and supergroups
    can_send_paid_media: True, if paid media messages can be sent or forwarded to the channel chat. The field is available only for channel chats.
    slow_mode_delay: For supergroups, the minimum allowed delay between consecutive messages sent by each unprivileged user; in seconds
    unrestrict_boost_count: For supergroups, the minimum number of boosts that a non-administrator user needs to add in order to ignore slow mode and chat permissions
    message_auto_delete_time: The time after which all messages sent to the chat will be automatically deleted; in seconds
    has_aggressive_anti_spam_enabled: True, if aggressive anti-spam checks are enabled in the supergroup. The field is only available to chat administrators.
    has_hidden_members: True, if non-administrators can only get the list of bots and administrators in the chat
    has_protected_content: True, if messages from the chat can't be forwarded to other chats
    has_visible_history: True, if new chat members will have access to old messages; available only to chat administrators
    sticker_set_name: For supergroups, name of the group sticker set
    can_set_sticker_set: True, if the bot can change the group sticker set
    custom_emoji_sticker_set_name: For supergroups, the name of the group's custom emoji sticker set. Custom emoji from this set can be used by all users and bots in the group.
    linked_chat_id: Unique identifier for the linked chat, i.e. the discussion group identifier for a channel and vice versa; for supergroups and channel chats. This identifier may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
    location: For supergroups, the location to which the supergroup is connected
    rating: For private chats, the rating of the user if any
    first_profile_audio: For private chats, the first audio added to the profile of the user
    unique_gift_colors: The color scheme based on a unique gift that must be used for the chat's name, message replies and link previews
    paid_message_star_count: The number of Telegram Stars a general user has to pay to send a message to the chat
    guard_bot: The bot that processes join request queries in the chat. The field is only available to chat administrators.
    community: The Community to which the chat belongs
    can_send_gift: True, if gifts can be sent to the chat"""
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None
    accent_color_id: Optional[int] = None
    max_reaction_count: Optional[int] = None
    photo: Optional[ChatPhoto] = None
    active_usernames: Optional[List[str]] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None
    permissions: Optional[object] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_protected_content: Optional[bool] = None
    has_visible_history: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[object] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatFullInfo']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(id=data['id'], type=data.get('type', ''), title=data.get('title'), username=data.get('username'), first_name=data.get('first_name'), last_name=data.get('last_name'), is_forum=data.get('is_forum'), accent_color_id=data.get('accent_color_id'), max_reaction_count=data.get('max_reaction_count'), photo=ChatPhoto.from_dict(data.get('photo')), active_usernames=data.get('active_usernames'), description=data.get('description'), invite_link=data.get('invite_link'), pinned_message=Message.from_dict(data.get('pinned_message')), permissions=data.get('permissions'), slow_mode_delay=data.get('slow_mode_delay'), message_auto_delete_time=data.get('message_auto_delete_time'), has_protected_content=data.get('has_protected_content'), has_visible_history=data.get('has_visible_history'), sticker_set_name=data.get('sticker_set_name'), can_set_sticker_set=data.get('can_set_sticker_set'), linked_chat_id=data.get('linked_chat_id'), location=data.get('location'))
