from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BackgroundFillGradient:
    """The background is a gradient fill.

Attributes:
    type: Type of the background fill, always 'gradient'
    top_color: Top color of the gradient in the RGB24 format
    bottom_color: Bottom color of the gradient in the RGB24 format
    rotation_angle: Clockwise rotation angle of the background fill in degrees; 0-359"""
    type: str = 'gradient'
    top_color: int = 0
    bottom_color: int = 0
    rotation_angle: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BackgroundFillGradient']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BackgroundFillGradient']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'gradient'), top_color=data.get('top_color', 0), bottom_color=data.get('bottom_color', 0), rotation_angle=data.get('rotation_angle', 0))
