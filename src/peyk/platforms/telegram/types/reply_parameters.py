from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .message_entity import MessageEntity

@dataclass
class ReplyParameters:
    """Describes reply parameters for the message that is being sent.

Attributes:
    message_id: Identifier of the message that will be replied to in the current chat, or in the chat chat_id if it is specified. Required if ephemeral_message_id isn't specified.
    chat_id: If the message to be replied to is from a different chat, unique identifier for the chat or username of the bot, supergroup or channel in the format @username. Not supported for messages sent on behalf of a business account, messages from channel direct messages chats and ephemeral messages.
    allow_sending_without_reply: Pass True if the message should be sent even if the specified message to be replied to is not found. Always False for replies in another chat or forum topic, and sent ephemeral messages. Always True for messages sent on behalf of a business account.
    quote: Quoted part of the message to be replied to; 0-1024 characters after entities parsing. The quote must be an exact substring of the message to be replied to, including bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities. The message will fail to send if the quote isn't found in the original message. Ignored for ephemeral messages.
    quote_parse_mode: Mode for parsing entities in the quote. See formatting options for more details.
    quote_entities: A JSON-serialized list of special entities that appear in the quote. It can be specified instead of quote_parse_mode.
    quote_position: Position of the quote in the original message in UTF-16 code units
    checklist_task_id: Identifier of the specific checklist task to be replied to
    poll_option_id: Persistent identifier of the specific poll option to be replied to
    ephemeral_message_id: Identifier of the incoming ephemeral message that will be replied to in the current chat. A reply to an ephemeral message must itself be an ephemeral message. An ephemeral message may only be replied to within 15 seconds of being sent. Required if message_id isn't specified."""
    message_id: Optional[int] = None
    chat_id: Optional[object] = None
    quote: Optional[str] = None
    quote_parse_mode: Optional[str] = None
    quote_entities: Optional[List[MessageEntity]] = None
    quote_position: Optional[int] = None
    checklist_task_id: Optional[int] = None
    allow_sending_without_reply: Optional[bool] = None
    ephemeral_message_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ReplyParameters']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(message_id=data.get('message_id'), chat_id=data.get('chat_id'), quote=data.get('quote'), quote_parse_mode=data.get('quote_parse_mode'), quote_entities=MessageEntity.list_from(data.get('quote_entities')), quote_position=data.get('quote_position'), checklist_task_id=data.get('checklist_task_id'), allow_sending_without_reply=data.get('allow_sending_without_reply'), ephemeral_message_id=data.get('ephemeral_message_id'))

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.

Returns:
    A JSON-compatible mapping representing this value."""
        body: Dict[str, object] = {}
        if self.message_id is not None:
            body['message_id'] = self.message_id
        if self.chat_id is not None:
            body['chat_id'] = self.chat_id
        if self.quote is not None:
            body['quote'] = self.quote
        if self.quote_parse_mode is not None:
            body['quote_parse_mode'] = self.quote_parse_mode
        if self.quote_entities is not None:
            body['quote_entities'] = [e.to_dict() for e in self.quote_entities]
        if self.quote_position is not None:
            body['quote_position'] = self.quote_position
        if self.checklist_task_id is not None:
            body['checklist_task_id'] = self.checklist_task_id
        if self.allow_sending_without_reply is not None:
            body['allow_sending_without_reply'] = self.allow_sending_without_reply
        if self.ephemeral_message_id is not None:
            body['ephemeral_message_id'] = self.ephemeral_message_id
        return body
