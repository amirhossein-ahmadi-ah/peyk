from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StoryAreaPosition:
    """Describes the position of a clickable area within a story.

Attributes:
    x_percentage: The abscissa of the area's center, as a percentage of the media width
    y_percentage: The ordinate of the area's center, as a percentage of the media height
    width_percentage: The width of the area's rectangle, as a percentage of the media width
    height_percentage: The height of the area's rectangle, as a percentage of the media height
    rotation_angle: The clockwise rotation angle of the rectangle, in degrees; 0-360
    corner_radius_percentage: The radius of the rectangle corner rounding, as a percentage of the media width"""
    x_percentage: float = 0.0
    y_percentage: float = 0.0
    width_percentage: float = 0.0
    height_percentage: float = 0.0
    rotation_angle: float = 0.0
    radius_percentage: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StoryAreaPosition']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StoryAreaPosition']``).\n        "
        if data is None:
            return None
        return cls(x_percentage=data.get('x_percentage', 0.0), y_percentage=data.get('y_percentage', 0.0), width_percentage=data.get('width_percentage', 0.0), height_percentage=data.get('height_percentage', 0.0), rotation_angle=data.get('rotation_angle', 0.0), radius_percentage=data.get('radius_percentage'))
