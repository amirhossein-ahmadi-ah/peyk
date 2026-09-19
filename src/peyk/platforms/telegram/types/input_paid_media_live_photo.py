from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputPaidMediaLivePhoto:
    """The paid media to send is a live photo.

Attributes:
    type: Type of the media, must be live_photo
    media: Video of the live photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files. Sending live photos by a URL is currently unsupported.
    photo: The static photo to send. Pass a file_id to send a file that exists on the Telegram servers (recommended) or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files. Sending live photos by a URL is currently unsupported."""
    media: object
    photo: object
    type: str = 'live_photo'
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_spoiler: Optional[bool] = None

    def to_dict(self, media_ref: str, photo_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media_ref: Value used by this operation.
    photo_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            media_ref: Value of the declared parameter type.\n            photo_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': 'live_photo', 'media': media_ref, 'photo': photo_ref}
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
