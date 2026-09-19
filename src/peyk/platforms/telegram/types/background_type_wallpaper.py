from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BackgroundTypeWallpaper:
    """The background is a wallpaper in the JPEG format.

Attributes:
    type: Type of the background, always 'wallpaper'
    document: Document with the wallpaper
    dark_theme_dimming: Dimming of the background in dark themes, as a percentage; 0-100
    is_blurred: True, if the wallpaper is downscaled to fit in a 450x450 square and then box-blurred with radius 12
    is_moving: True, if the background moves slightly when the device is tilted"""
    type: str = 'wallpaper'
    document: Optional[Document] = None
    dark_theme_dimming: int = 0
    is_blurred: Optional[bool] = None
    is_moving: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BackgroundTypeWallpaper']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BackgroundTypeWallpaper']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'wallpaper'), document=Document.from_dict(data.get('document')), dark_theme_dimming=data.get('dark_theme_dimming', 0), is_blurred=data.get('is_blurred'), is_moving=data.get('is_moving'))
