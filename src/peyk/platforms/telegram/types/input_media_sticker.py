from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputMediaSticker:
    """Represents a sticker file to be sent.

Attributes:
    type: Type of the media, must be sticker
    media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a .WEBP sticker from the Internet, or pass 'attach://' to upload a new .WEBP, .TGS, or .WEBM sticker using multipart/form-data under  name. More information on Sending Files
    emoji: Emoji associated with the sticker; only for just uploaded stickers"""
    media: object
    type: str = 'sticker'
    emoji: Optional[str] = None
    mask_position: Optional[object] = None

    def to_dict(self, media_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            media_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': 'sticker', 'media': media_ref}
        if self.emoji is not None:
            body['emoji'] = self.emoji
        if self.mask_position is not None:
            body['mask_position'] = self.mask_position
        return body
