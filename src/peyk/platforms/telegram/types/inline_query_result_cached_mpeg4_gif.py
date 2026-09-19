from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultCachedMpeg4Gif:
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers. By default, this animated MPEG-4 file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.

Attributes:
    type: Type of the result, must be mpeg4_gif
    id: Unique identifier for this result, 1-64 bytes
    mpeg4_file_id: A valid file identifier for the MPEG4 file
    title: Title for the result
    caption: Caption of the MPEG-4 file to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the video animation"""
    id: str
    mpeg4_file_id: str
    type: str = 'mpeg4_gif'
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
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'mpeg4_file_id': self.mpeg4_file_id}
        if self.title is not None:
            body['title'] = self.title
        _apply_caption_fields(body, self)
        _apply_result_markup(body, self)
        return body
