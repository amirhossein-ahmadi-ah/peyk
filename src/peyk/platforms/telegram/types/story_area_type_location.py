from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StoryAreaTypeLocation:
    """Describes a story area pointing to a location. Currently, a story can have up to 10 location areas.

Attributes:
    type: Type of the area, always 'location'
    latitude: Location latitude in degrees
    longitude: Location longitude in degrees
    address: Address of the location"""
    latitude: float
    longitude: float
    type: str = 'location'
    address: Optional[LocationAddress] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StoryAreaTypeLocation']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StoryAreaTypeLocation']``).\n        "
        if data is None:
            return None
        return cls(latitude=_parse_api_value('Float', data.get('latitude')), longitude=_parse_api_value('Float', data.get('longitude')), type=_parse_api_value('String', data.get('type')), address=_parse_api_value('LocationAddress', data.get('address')))
