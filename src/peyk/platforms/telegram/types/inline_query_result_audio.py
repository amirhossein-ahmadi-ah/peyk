from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultAudio:
    """Represents a link to an MP3 audio file. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.

Attributes:
    type: Type of the result, must be audio
    id: Unique identifier for this result, 1-64 bytes
    audio_url: A valid URL for the audio file
    title: Title
    caption: Caption, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the audio caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    performer: Performer
    audio_duration: Audio duration in seconds
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the audio"""
    id: str
    audio_url: str
    title: str
    type: str = 'audio'
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]] = None
    performer: Optional[str] = None
    audio_duration: Optional[int] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'audio_url': self.audio_url, 'title': self.title}
        if self.caption is not None:
            body['caption'] = self.caption
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        entities = _serialize_entities(self.caption_entities)
        if entities is not None:
            body['caption_entities'] = entities
        if self.performer is not None:
            body['performer'] = self.performer
        if self.audio_duration is not None:
            body['audio_duration'] = self.audio_duration
        _apply_result_markup(body, self)
        return body
