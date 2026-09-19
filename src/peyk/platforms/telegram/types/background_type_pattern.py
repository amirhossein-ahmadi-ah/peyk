from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BackgroundTypePattern:
    """The background is a .PNG or .TGV (gzipped subset of SVG with MIME type 'application/x-tgwallpattern') pattern to be combined with the background fill chosen by the user.

Attributes:
    type: Type of the background, always 'pattern'
    document: Document with the pattern
    fill: The background fill that is combined with the pattern
    intensity: Intensity of the pattern when it is shown above the filled background; 0-100
    is_inverted: True, if the background fill must be applied only to the pattern itself. All other pixels are black in this case. For dark themes only.
    is_moving: True, if the background moves slightly when the device is tilted"""
    type: str = 'pattern'
    document: Optional[Document] = None
    fill: Optional[BackgroundFill] = None
    intensity: int = 0
    is_inverted: Optional[bool] = None
    is_moving: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BackgroundTypePattern']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BackgroundTypePattern']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'pattern'), document=Document.from_dict(data.get('document')), fill=parse_background_fill(data.get('fill')), intensity=data.get('intensity', 0), is_inverted=data.get('is_inverted'), is_moving=data.get('is_moving'))
