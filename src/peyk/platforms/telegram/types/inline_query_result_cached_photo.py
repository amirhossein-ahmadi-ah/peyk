from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultCachedPhoto:
    """Represents a link to a photo stored on the Telegram servers. By default, this photo will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.

Attributes:
    type: Type of the result, must be photo
    id: Unique identifier for this result, 1-64 bytes
    photo_file_id: A valid file identifier of the photo
    title: Title for the result
    description: Short description of the result
    caption: Caption of the photo to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the photo"""
    id: str
    photo_file_id: str
    type: str = 'photo'
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]] = None
    show_caption_above_media: Optional[bool] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'photo_file_id': self.photo_file_id}
        if self.title is not None:
            body['title'] = self.title
        if self.description is not None:
            body['description'] = self.description
        _apply_caption_fields(body, self)
        _apply_result_markup(body, self)
        return body
