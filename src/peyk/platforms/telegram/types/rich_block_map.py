from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockMap:
    """A block with a map, corresponding to the custom HTML tag .

Attributes:
    type: Type of the block, always 'map'
    location: Location of the center of the map
    zoom: Map zoom level; 13-20
    width: Expected width of the map
    height: Expected height of the map
    caption: Caption of the block"""
    latitude: float = 0.0
    longitude: float = 0.0

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(latitude=data.get('latitude', 0.0), longitude=data.get('longitude', 0.0)) if data else None
