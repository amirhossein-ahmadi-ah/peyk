from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputSticker:
    """This object describes a sticker to be added to a sticker set.

Attributes:
    sticker: The added sticker. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or pass 'attach://' to upload a new file using multipart/form-data under  name. Animated and video stickers can't be uploaded via HTTP URL. More information on Sending Files
    format: Format of the added sticker, must be one of 'static' for a .WEBP or .PNG image, 'animated' for a .TGS animation, 'video' for a .WEBM video
    emoji_list: List of 1-20 emoji associated with the sticker
    mask_position: Position where the mask should be placed on faces. For 'mask' stickers only.
    keywords: List of 0-20 search keywords for the sticker with total length of up to 64 characters. For 'regular' and 'custom_emoji' stickers only."""
    sticker: object
    format: str
    emoji_list: List[str]
    mask_position: Optional[MaskPosition] = None
    keywords: Optional[List[str]] = None

    def to_dict(self, sticker_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    sticker_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Serialize for the request body.\n        \n                `sticker_ref` is the already-resolved reference (a `file_id`/URL\n                string, or an `attach://` name wired to a multipart part).\n                \n        \n        Args:\n            sticker_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'sticker': sticker_ref, 'format': self.format, 'emoji_list': list(self.emoji_list)}
        if self.mask_position is not None:
            body['mask_position'] = self.mask_position.to_dict()
        if self.keywords is not None:
            body['keywords'] = list(self.keywords)
        return body
