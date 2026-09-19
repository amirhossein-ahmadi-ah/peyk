from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultLocation:
    """Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the location.

Attributes:
    type: Type of the result, must be location
    id: Unique identifier for this result, 1-64 Bytes
    latitude: Location latitude in degrees
    longitude: Location longitude in degrees
    title: Location title
    horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
    live_period: Period in seconds during which the location can be updated, must be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely
    heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
    proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the location
    thumbnail_url: Url of the thumbnail for the result
    thumbnail_width: Thumbnail width
    thumbnail_height: Thumbnail height"""
    id: str
    latitude: float
    longitude: float
    title: str
    type: str = 'location'
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
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
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude, 'title': self.title}
        if self.horizontal_accuracy is not None:
            body['horizontal_accuracy'] = self.horizontal_accuracy
        if self.live_period is not None:
            body['live_period'] = self.live_period
        if self.heading is not None:
            body['heading'] = self.heading
        if self.proximity_alert_radius is not None:
            body['proximity_alert_radius'] = self.proximity_alert_radius
        _apply_result_markup(body, self)
        _apply_thumbnail_fields(body, self)
        return body
