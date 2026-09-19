from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .photo_size import PhotoSize

@dataclass
class Audio:
    """This object represents an audio file to be treated as music by the Telegram clients.

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    duration: Duration of the audio in seconds as defined by the sender
    performer: Performer of the audio as defined by the sender or by audio tags
    title: Title of the audio as defined by the sender or by audio tags
    file_name: Original filename as defined by the sender
    mime_type: MIME type of the file as defined by the sender
    file_size: File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value.
    thumbnail: Thumbnail of the album cover to which the music file belongs"""
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumbnail: Optional[PhotoSize] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Audio']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), duration=data.get('duration', 0), performer=data.get('performer'), title=data.get('title'), file_name=data.get('file_name'), mime_type=data.get('mime_type'), file_size=data.get('file_size'), thumbnail=PhotoSize.from_dict(data.get('thumbnail')))
