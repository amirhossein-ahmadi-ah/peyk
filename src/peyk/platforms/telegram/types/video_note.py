from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .photo_size import PhotoSize

@dataclass
class VideoNote:
    """This object represents a video message (available in Telegram apps as of v.4.0).

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    length: Video width and height (diameter of the video message) as defined by the sender
    duration: Duration of the video in seconds as defined by the sender
    thumbnail: Video thumbnail
    file_size: File size in bytes"""
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    file_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['VideoNote']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), length=data.get('length', 0), duration=data.get('duration', 0), thumbnail=PhotoSize.from_dict(data.get('thumbnail')), file_size=data.get('file_size'))
