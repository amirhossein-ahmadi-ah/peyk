from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultVenue:
    """Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the venue.

Attributes:
    type: Type of the result, must be venue
    id: Unique identifier for this result, 1-64 Bytes
    latitude: Latitude of the venue location in degrees
    longitude: Longitude of the venue location in degrees
    title: Title of the venue
    address: Address of the venue
    foursquare_id: Foursquare identifier of the venue if known
    foursquare_type: Foursquare type of the venue, if known. (For example, 'arts_entertainment/default', 'arts_entertainment/aquarium' or 'food/icecream'.)
    google_place_id: Google Places identifier of the venue
    google_place_type: Google Places type of the venue. (See supported types.)
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the venue
    thumbnail_url: Url of the thumbnail for the result
    thumbnail_width: Thumbnail width
    thumbnail_height: Thumbnail height"""
    id: str
    latitude: float
    longitude: float
    title: str
    address: str
    type: str = 'venue'
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude, 'title': self.title, 'address': self.address}
        if self.foursquare_id is not None:
            body['foursquare_id'] = self.foursquare_id
        if self.foursquare_type is not None:
            body['foursquare_type'] = self.foursquare_type
        if self.google_place_id is not None:
            body['google_place_id'] = self.google_place_id
        if self.google_place_type is not None:
            body['google_place_type'] = self.google_place_type
        _apply_result_markup(body, self)
        _apply_thumbnail_fields(body, self)
        return body
