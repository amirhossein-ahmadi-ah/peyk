from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PhotoSize:
    """This object represents one size of a photo or a file / sticker thumbnail.

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    width: Photo width
    height: Photo height
    file_size: File size in bytes"""
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PhotoSize']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), width=data.get('width', 0), height=data.get('height', 0), file_size=data.get('file_size'))

    @classmethod
    def list_from(cls, data: Optional[List[dict]]) -> Optional[List['PhotoSize']]:
        """Parse a Telegram API result list into this type.

Args:
    data: Raw result list, or ``None``.

Returns:
    Parsed type instances."""
        if data is None:
            return None
        return [cls.from_dict(item) for item in data]
