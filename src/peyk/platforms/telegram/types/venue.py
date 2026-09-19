from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .location import Location

@dataclass
class Venue:
    """This object represents a venue.

Attributes:
    location: Venue location. Can't be a live location.
    title: Name of the venue
    address: Address of the venue
    foursquare_id: Foursquare identifier of the venue
    foursquare_type: Foursquare type of the venue. (For example, 'arts_entertainment/default', 'arts_entertainment/aquarium' or 'food/icecream'.)
    google_place_id: Google Places identifier of the venue
    google_place_type: Google Places type of the venue. (See supported types.)"""
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Venue']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(location=Location.from_dict(data.get('location', {})), title=data.get('title', ''), address=data.get('address', ''), foursquare_id=data.get('foursquare_id'), foursquare_type=data.get('foursquare_type'), google_place_id=data.get('google_place_id'), google_place_type=data.get('google_place_type'))
