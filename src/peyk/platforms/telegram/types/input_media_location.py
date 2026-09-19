from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputMediaLocation:
    """Represents a location to be sent.

Attributes:
    type: Type of the media, must be location
    latitude: Latitude of the location
    longitude: Longitude of the location
    horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500"""
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.

Returns:
    A JSON-compatible mapping representing this value."""
        body: Dict[str, object] = {'type': 'location', 'latitude': self.latitude, 'longitude': self.longitude}
        if self.horizontal_accuracy is not None:
            body['horizontal_accuracy'] = self.horizontal_accuracy
        return body
