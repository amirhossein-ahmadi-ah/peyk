from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .photo_size import PhotoSize

@dataclass
class Video:
    """This object represents a video file.

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    width: Video width as defined by the sender
    height: Video height as defined by the sender
    duration: Duration of the video in seconds as defined by the sender
    thumbnail: Video thumbnail
    cover: Available sizes of the cover of the video in the message
    start_timestamp: Timestamp in seconds from which the video will play in the message
    qualities: List of available qualities of the video
    file_name: Original filename as defined by the sender
    mime_type: MIME type of the file as defined by the sender
    file_size: File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    cover: Optional[List[PhotoSize]] = None
    start_timestamp: Optional[int] = None
    qualities: Optional[object] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Video']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), width=data.get('width', 0), height=data.get('height', 0), duration=data.get('duration', 0), thumbnail=PhotoSize.from_dict(data.get('thumbnail')), cover=PhotoSize.list_from(data.get('cover')), start_timestamp=data.get('start_timestamp'), qualities=data.get('qualities'), file_name=data.get('file_name'), mime_type=data.get('mime_type'), file_size=data.get('file_size'))
