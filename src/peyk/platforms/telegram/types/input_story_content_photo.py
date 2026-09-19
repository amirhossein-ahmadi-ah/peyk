from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputStoryContentPhoto:
    """Describes a photo to post as a story.

Attributes:
    type: Type of the content, must be photo
    photo: The photo to post as a story. The photo must be of the size 1080x1920 and must not exceed 10 MB. The photo can't be reused and can only be uploaded as a new file, so you can pass 'attach://' if the photo was uploaded using multipart/form-data under . More information on Sending Files"""
    media: object = None
    photo: object = None
    type: str = 'photo'
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None

    def to_dict(self, media_ref: Optional[str]=None) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            media_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        ref = media_ref if media_ref is not None else self.media if self.media is not None else self.photo
        body: Dict[str, object] = {'type': 'photo', 'photo': ref}
        if self.caption is not None:
            body['caption'] = self.caption
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        if self.caption_entities is not None:
            body['caption_entities'] = [e.to_dict() for e in self.caption_entities]
        return body

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InputStoryContentPhoto']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InputStoryContentPhoto']``).\n        "
        if data is None:
            return None
        return cls(media=data.get('media', data.get('photo')), photo=data.get('photo'), type=data.get('type', 'photo'), caption=data.get('caption'), parse_mode=data.get('parse_mode'), caption_entities=MessageEntity.list_from(data.get('caption_entities')))
