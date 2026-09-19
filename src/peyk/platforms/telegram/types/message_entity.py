from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .user import User

@dataclass
class MessageEntity:
    """This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.

Attributes:
    type: Type of the entity. Currently, can be 'mention' (@username), 'hashtag' (#hashtag or #hashtag@chatusername), 'cashtag' ($USD or $USD@chatusername), 'bot_command' (/start@jobs_bot), 'url' (https://telegram.org), 'email' (do-not-reply@telegram.org), 'phone_number' (+1-212-555-0123), 'bold' (bold text), 'italic' (italic text), 'underline' (underlined text), 'strikethrough' (strikethrough text), 'spoiler' (spoiler message), 'blockquote' (block quotation), 'expandable_blockquote' (collapsed-by-default block quotation), 'code' (monowidth string), 'pre' (monowidth block), 'text_link' (for clickable text URLs), 'text_mention' (for users without usernames), 'custom_emoji' (for inline custom emoji stickers), or 'date_time' (for formatted date and time).
    offset: Offset in UTF-16 code units to the start of the entity
    length: Length of the entity in UTF-16 code units
    url: For 'text_link' only, URL that will be opened after user taps on the text
    user: For 'text_mention' only, the mentioned user
    language: For 'pre' only, the programming language of the entity text
    custom_emoji_id: For 'custom_emoji' only, unique identifier of the custom emoji. Use getCustomEmojiStickers to get full information about the sticker.
    unix_time: For 'date_time' only, the Unix time associated with the entity
    date_time_format: For 'date_time' only, the string that defines the formatting of the date and time. See date-time entity formatting for more details."""
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageEntity']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(type=data.get('type', ''), offset=data.get('offset', 0), length=data.get('length', 0), url=data.get('url'), user=User.from_dict(data.get('user')), language=data.get('language'), custom_emoji_id=data.get('custom_emoji_id'))

    @classmethod
    def list_from(cls, data: Optional[List[dict]]) -> Optional[List['MessageEntity']]:
        """Parse a Telegram API result list into this type.

Args:
    data: Raw result list, or ``None``.

Returns:
    Parsed type instances."""
        if data is None:
            return None
        return [cls.from_dict(item) for item in data]

    def to_dict(self) -> Dict[str, object]:
        """Serialize for outgoing request bodies (T2: send/edit params).
        
        Returns:
            The operation result (``Dict[str, object]``).
        """
        body: Dict[str, object] = {'type': self.type, 'offset': self.offset, 'length': self.length}
        if self.url is not None:
            body['url'] = self.url
        if self.user is not None:
            body['user'] = {'id': self.user.id, 'is_bot': self.user.is_bot, 'first_name': self.user.first_name}
            if self.user.last_name is not None:
                body['user']['last_name'] = self.user.last_name
            if self.user.username is not None:
                body['user']['username'] = self.user.username
        if self.language is not None:
            body['language'] = self.language
        if self.custom_emoji_id is not None:
            body['custom_emoji_id'] = self.custom_emoji_id
        return body
