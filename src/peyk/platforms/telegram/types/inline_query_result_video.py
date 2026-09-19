from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultVideo:
    """Represents a link to a page containing an embedded video player or a video file. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.
If an InlineQueryResultVideo message contains an embedded video (e.g., YouTube), you must replace its content using input_message_content.

Attributes:
    type: Type of the result, must be video
    id: Unique identifier for this result, 1-64 bytes
    video_url: A valid URL for the embedded video player or video file
    mime_type: MIME type of the content of the video URL, 'text/html' or 'video/mp4'
    thumbnail_url: URL of the thumbnail (JPEG only) for the video
    title: Title for the result
    caption: Caption of the video to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    video_width: Video width
    video_height: Video height
    video_duration: Video duration in seconds
    description: Short description of the result
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the video. This field is required if InlineQueryResultVideo is used to send an HTML-page as a result (e.g., a YouTube video)."""
    id: str
    video_url: str
    mime_type: str
    thumbnail_url: str
    title: str
    type: str = 'video'
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]] = None
    show_caption_above_media: Optional[bool] = None
    video_width: Optional[int] = None
    video_height: Optional[int] = None
    video_duration: Optional[int] = None
    description: Optional[str] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'video_url': self.video_url, 'mime_type': self.mime_type, 'thumbnail_url': self.thumbnail_url, 'title': self.title}
        _apply_caption_fields(body, self)
        if self.video_width is not None:
            body['video_width'] = self.video_width
        if self.video_height is not None:
            body['video_height'] = self.video_height
        if self.video_duration is not None:
            body['video_duration'] = self.video_duration
        if self.description is not None:
            body['description'] = self.description
        _apply_result_markup(body, self)
        return body
