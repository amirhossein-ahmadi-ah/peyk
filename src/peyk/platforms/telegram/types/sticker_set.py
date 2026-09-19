from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StickerSet:
    """This object represents a sticker set.

Attributes:
    name: Sticker set name
    title: Sticker set title
    sticker_type: Type of stickers in the set, currently one of 'regular', 'mask', 'custom_emoji'
    stickers: List of all set stickers
    thumbnail: Sticker set thumbnail in the .WEBP, .TGS, or .WEBM format
    is_animated: True, if the sticker set contains animated stickers
    is_video: True, if the sticker set contains video stickers"""
    name: str
    title: str
    sticker_type: str
    stickers: List[Sticker]
    is_animated: bool = False
    is_video: bool = False
    thumbnail: Optional[PhotoSize] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StickerSet']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StickerSet']``).\n        "
        if data is None:
            return None
        return cls(name=data.get('name', ''), title=data.get('title', ''), sticker_type=data.get('sticker_type', 'regular'), stickers=[s for s in (Sticker.from_dict(item) for item in data.get('stickers', [])) if s is not None], is_animated=data.get('is_animated', False), is_video=data.get('is_video', False), thumbnail=PhotoSize.from_dict(data.get('thumbnail')))
