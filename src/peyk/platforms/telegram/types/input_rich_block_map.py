from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockMap:
    """A block with a map, corresponding to the custom HTML tag . The map's width and height must not exceed 10000 in total. The width and height ratio must be at most 20.

Attributes:
    type: Type of the block, always 'map'
    location: Location of the center of the map
    zoom: Map zoom level; 0-24
    width: Map width; 0-10000
    height: Map height; 0-10000
    caption: Caption of the block"""
    latitude: float = 0.0
    longitude: float = 0.0

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'latitude': self.latitude, 'longitude': self.longitude}
