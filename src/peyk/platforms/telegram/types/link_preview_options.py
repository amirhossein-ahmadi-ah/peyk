from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class LinkPreviewOptions:
    """Describes the options used for link preview generation.

Attributes:
    is_disabled: True, if the link preview is disabled
    url: URL to use for the link preview. If empty, then the first URL found in the message text will be used.
    prefer_small_media: True, if the media in the link preview is supposed to be shrunk; ignored if the URL isn't explicitly specified or media size change isn't supported for the preview
    prefer_large_media: True, if the media in the link preview is supposed to be enlarged; ignored if the URL isn't explicitly specified or media size change isn't supported for the preview
    show_above_text: True, if the link preview must be shown above the message text; otherwise, the link preview will be shown below the message text"""
    is_disabled: Optional[bool] = None
    url: Optional[str] = None
    prefer_small_media: Optional[bool] = None
    prefer_large_media: Optional[bool] = None
    show_above_text: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['LinkPreviewOptions']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(is_disabled=data.get('is_disabled'), url=data.get('url'), prefer_small_media=data.get('prefer_small_media'), prefer_large_media=data.get('prefer_large_media'), show_above_text=data.get('show_above_text'))

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.

Returns:
    A JSON-compatible mapping representing this value."""
        body: Dict[str, object] = {}
        if self.is_disabled is not None:
            body['is_disabled'] = self.is_disabled
        if self.url is not None:
            body['url'] = self.url
        if self.prefer_small_media is not None:
            body['prefer_small_media'] = self.prefer_small_media
        if self.prefer_large_media is not None:
            body['prefer_large_media'] = self.prefer_large_media
        if self.show_above_text is not None:
            body['show_above_text'] = self.show_above_text
        return body
