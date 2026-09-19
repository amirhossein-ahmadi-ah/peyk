from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Sticker:
    """This object represents a sticker.

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    type: Type of the sticker, currently one of 'regular', 'mask', 'custom_emoji'. The type of the sticker is independent from its format, which is determined by the fields is_animated and is_video.
    width: Sticker width
    height: Sticker height
    is_animated: True, if the sticker is animated
    is_video: True, if the sticker is a video sticker
    thumbnail: Sticker thumbnail in the .WEBP or .JPG format
    emoji: Emoji associated with the sticker
    set_name: Name of the sticker set to which the sticker belongs
    premium_animation: For premium regular stickers, premium animation for the sticker
    mask_position: For mask stickers, the position where the mask should be placed
    custom_emoji_id: For custom emoji stickers, unique identifier of the custom emoji
    needs_repainting: True, if the sticker must be repainted to a text color in messages, the color of the Telegram Premium badge in emoji status, white color on chat photos, or another appropriate color in other places
    file_size: File size in bytes"""
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool = False
    is_video: bool = False
    thumbnail: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[File] = None
    mask_position: Optional[MaskPosition] = None
    custom_emoji_id: Optional[str] = None
    needs_repainting: Optional[bool] = None
    file_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Sticker']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Sticker']``).\n        "
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), type=data.get('type', 'regular'), width=data.get('width', 0), height=data.get('height', 0), is_animated=data.get('is_animated', False), is_video=data.get('is_video', False), thumbnail=PhotoSize.from_dict(data.get('thumbnail')), emoji=data.get('emoji'), set_name=data.get('set_name'), premium_animation=File.from_dict(data.get('premium_animation')), mask_position=MaskPosition.from_dict(data.get('mask_position')), custom_emoji_id=data.get('custom_emoji_id'), needs_repainting=data.get('needs_repainting'), file_size=data.get('file_size'))

    @classmethod
    def list_from(cls, data: Optional[List[dict]]) -> Optional[List['Sticker']]:
        """Provides the list from operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the list_from operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional[List['Sticker']]``).\n        "
        if data is None:
            return None
        return [cls.from_dict(item) for item in data]
