from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class VideoQuality:
    """This object represents a video file of a specific quality.

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    width: Video width
    height: Video height
    codec: Codec that was used to encode the video, for example, 'h264', 'h265', or 'av01'
    file_size: File size in bytes. It can be bigger than 2^31 and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this value."""
    type: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['VideoQuality']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['VideoQuality']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', ''), width=data.get('width'), height=data.get('height'), duration=data.get('duration'))
