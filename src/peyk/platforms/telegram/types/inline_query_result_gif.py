from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultGif:
    """Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.

Attributes:
    type: Type of the result, must be gif
    id: Unique identifier for this result, 1-64 bytes
    gif_url: A valid URL for the GIF file
    thumbnail_url: URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result
    gif_width: Width of the GIF
    gif_height: Height of the GIF
    gif_duration: Duration of the GIF in seconds
    thumbnail_mime_type: MIME type of the thumbnail, must be one of 'image/jpeg', 'image/gif', or 'video/mp4'. Defaults to 'image/jpeg'.
    title: Title for the result
    caption: Caption of the GIF file to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the GIF animation"""
    id: str
    gif_url: str
    thumbnail_url: str
    type: str = 'gif'
    gif_width: Optional[int] = None
    gif_height: Optional[int] = None
    gif_duration: Optional[int] = None
    thumbnail_mime_type: Optional[str] = None
    title: Optional[str] = None
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
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'gif_url': self.gif_url, 'thumbnail_url': self.thumbnail_url}
        if self.gif_width is not None:
            body['gif_width'] = self.gif_width
        if self.gif_height is not None:
            body['gif_height'] = self.gif_height
        if self.gif_duration is not None:
            body['gif_duration'] = self.gif_duration
        if self.thumbnail_mime_type is not None:
            body['thumbnail_mime_type'] = self.thumbnail_mime_type
        if self.title is not None:
            body['title'] = self.title
        _apply_caption_fields(body, self)
        _apply_result_markup(body, self)
        return body
