from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .message_entity import MessageEntity

@dataclass
class InputMediaAnimation:
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.

Attributes:
    type: Type of the media, must be animation
    media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files
    thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://' if the thumbnail was uploaded using multipart/form-data under . More information on Sending Files
    caption: Caption of the animation to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the animation caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    width: Animation width
    height: Animation height
    duration: Animation duration in seconds
    has_spoiler: Pass True if the animation needs to be covered with a spoiler animation"""
    media: object
    thumbnail: Optional[object] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    has_spoiler: Optional[bool] = None

    def to_dict(self, media: str, thumbnail: Optional[str]=None) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media: Value used by this operation.
    thumbnail: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Serialize this type to the Telegram API request shape.\n        \n        Returns:\n            A JSON-compatible mapping representing this value.\n        \n        Args:\n            media: Value of the declared parameter type.\n            thumbnail: Value of the declared parameter type.\n        '
        body: Dict[str, object] = {'type': 'animation', 'media': media}
        if thumbnail is not None:
            body['thumbnail'] = thumbnail
        if self.caption is not None:
            body['caption'] = self.caption
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        if self.caption_entities is not None:
            body['caption_entities'] = [e.to_dict() for e in self.caption_entities]
        if self.show_caption_above_media is not None:
            body['show_caption_above_media'] = self.show_caption_above_media
        if self.width is not None:
            body['width'] = self.width
        if self.height is not None:
            body['height'] = self.height
        if self.duration is not None:
            body['duration'] = self.duration
        if self.has_spoiler is not None:
            body['has_spoiler'] = self.has_spoiler
        return body
