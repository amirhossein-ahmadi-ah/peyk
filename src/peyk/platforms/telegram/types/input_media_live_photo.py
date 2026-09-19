from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .message_entity import MessageEntity

@dataclass
class InputMediaLivePhoto:
    """Represents a live photo to be sent.

Attributes:
    type: Type of the media, must be live_photo
    media: Video of the live photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files. Sending live photos by a URL is currently unsupported.
    photo: The static photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files. Sending live photos by a URL is currently unsupported.
    caption: Caption of the live photo to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the live photo caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    has_spoiler: Pass True if the live photo needs to be covered with a spoiler animation"""
    media: object
    photo: object
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None

    def to_dict(self, media: str, photo: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media: Value used by this operation.
    photo: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Serialize this type to the Telegram API request shape.\n        \n        Returns:\n            A JSON-compatible mapping representing this value.\n        \n        Args:\n            media: Value of the declared parameter type.\n            photo: Value of the declared parameter type.\n        '
        body: Dict[str, object] = {'type': 'live_photo', 'media': media, 'photo': photo}
        if self.caption is not None:
            body['caption'] = self.caption
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        if self.caption_entities is not None:
            body['caption_entities'] = [e.to_dict() for e in self.caption_entities]
        if self.show_caption_above_media is not None:
            body['show_caption_above_media'] = self.show_caption_above_media
        if self.has_spoiler is not None:
            body['has_spoiler'] = self.has_spoiler
        return body
