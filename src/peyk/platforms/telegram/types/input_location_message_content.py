from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputLocationMessageContent:
    """Represents the content of a location message to be sent as the result of an inline query.

Attributes:
    latitude: Latitude of the location in degrees
    longitude: Longitude of the location in degrees
    horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
    live_period: Period in seconds during which the location can be updated, must be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely
    heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
    proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified."""
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'latitude': self.latitude, 'longitude': self.longitude}
        if self.horizontal_accuracy is not None:
            body['horizontal_accuracy'] = self.horizontal_accuracy
        if self.live_period is not None:
            body['live_period'] = self.live_period
        if self.heading is not None:
            body['heading'] = self.heading
        if self.proximity_alert_radius is not None:
            body['proximity_alert_radius'] = self.proximity_alert_radius
        return body
