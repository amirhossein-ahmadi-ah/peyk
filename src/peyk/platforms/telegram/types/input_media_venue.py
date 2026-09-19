from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputMediaVenue:
    """Represents a venue to be sent.

Attributes:
    type: Type of the media, must be venue
    latitude: Latitude of the location
    longitude: Longitude of the location
    title: Name of the venue
    address: Address of the venue
    foursquare_id: Foursquare identifier of the venue
    foursquare_type: Foursquare type of the venue, if known. (For example, 'arts_entertainment/default', 'arts_entertainment/aquarium' or 'food/icecream'.)
    google_place_id: Google Places identifier of the venue
    google_place_type: Google Places type of the venue. (See supported types.)"""
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.

Returns:
    A JSON-compatible mapping representing this value."""
        body: Dict[str, object] = {'type': 'venue', 'latitude': self.latitude, 'longitude': self.longitude, 'title': self.title, 'address': self.address}
        if self.foursquare_id is not None:
            body['foursquare_id'] = self.foursquare_id
        if self.foursquare_type is not None:
            body['foursquare_type'] = self.foursquare_type
        if self.google_place_id is not None:
            body['google_place_id'] = self.google_place_id
        if self.google_place_type is not None:
            body['google_place_type'] = self.google_place_type
        return body
