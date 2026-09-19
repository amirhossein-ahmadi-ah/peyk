from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BackgroundTypeFill:
    """The background is automatically filled based on the selected colors.

Attributes:
    type: Type of the background, always 'fill'
    fill: The background fill
    dark_theme_dimming: Dimming of the background in dark themes, as a percentage; 0-100"""
    type: str = 'fill'
    fill: Optional[BackgroundFill] = None
    dark_theme_dimming: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BackgroundTypeFill']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BackgroundTypeFill']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'fill'), fill=parse_background_fill(data.get('fill')), dark_theme_dimming=data.get('dark_theme_dimming', 0))
