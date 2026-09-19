from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultVoice:
    """Represents a link to a voice recording in an .OGG container encoded with OPUS. By default, this voice recording will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the the voice message.

Attributes:
    type: Type of the result, must be voice
    id: Unique identifier for this result, 1-64 bytes
    voice_url: A valid URL for the voice recording
    title: Recording title
    caption: Caption, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the voice message caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    voice_duration: Recording duration in seconds
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the voice recording"""
    id: str
    voice_url: str
    title: str
    type: str = 'voice'
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]] = None
    voice_duration: Optional[int] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'voice_url': self.voice_url, 'title': self.title}
        if self.caption is not None:
            body['caption'] = self.caption
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        entities = _serialize_entities(self.caption_entities)
        if entities is not None:
            body['caption_entities'] = entities
        if self.voice_duration is not None:
            body['voice_duration'] = self.voice_duration
        _apply_result_markup(body, self)
        return body
