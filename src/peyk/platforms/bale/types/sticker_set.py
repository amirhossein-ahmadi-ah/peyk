from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .photo_size import PhotoSize
from .sticker import Sticker
@dataclass
class StickerSet:
    """Represent the Bale Bot API ``StickerSet`` object.

Preserves the existing dataclass fields and parsing behavior."""
    name: str
    title: str
    stickers: List[Sticker]
    thumbnail: Optional[PhotoSize] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StickerSet']:
        """Parse raw Bale data into ``StickerSet``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[StickerSet]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(name=data.get('name', ''), title=data.get('title', ''), stickers=[Sticker.from_dict(s) for s in data.get('stickers', [])], thumbnail=PhotoSize.from_dict(data.get('thumbnail')))
