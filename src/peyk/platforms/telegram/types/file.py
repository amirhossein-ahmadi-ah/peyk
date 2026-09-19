from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class File:
    """This object represents a file ready to be downloaded. The file can be downloaded via the link https://api.telegram.org/file/bot/. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile.
The maximum file size to download is 20 MB

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    file_size: File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value.
    file_path: File path. Use https://api.telegram.org/file/bot/ to get the file."""
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['File']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), file_size=data.get('file_size'), file_path=data.get('file_path'))
