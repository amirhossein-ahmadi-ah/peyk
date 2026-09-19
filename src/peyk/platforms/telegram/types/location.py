from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Location:
    """This object represents a point on the map.

Attributes:
    latitude: Latitude as defined by the sender
    longitude: Longitude as defined by the sender
    horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
    live_period: Time relative to the message sending date, during which the location can be updated; in seconds. For active live locations only.
    heading: The direction in which user is moving, in degrees; 1-360. For active live locations only.
    proximity_alert_radius: The maximum distance for proximity alerts about approaching another chat member, in meters. For sent live locations only."""
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Location']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(latitude=data.get('latitude', 0.0), longitude=data.get('longitude', 0.0), horizontal_accuracy=data.get('horizontal_accuracy'), live_period=data.get('live_period'), heading=data.get('heading'), proximity_alert_radius=data.get('proximity_alert_radius'))
