from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatPhoto:
    """This object represents a chat photo.

Attributes:
    small_file_id: File identifier of small (160x160) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
    small_file_unique_id: Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    big_file_id: File identifier of big (640x640) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
    big_file_unique_id: Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file."""
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatPhoto']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(small_file_id=data.get('small_file_id', ''), small_file_unique_id=data.get('small_file_unique_id', ''), big_file_id=data.get('big_file_id', ''), big_file_unique_id=data.get('big_file_unique_id', ''))
