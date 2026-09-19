from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_venue(self, chat_id: ChatId, latitude: float, longitude: float, title: str, address: str, *, message_thread_id: Optional[int]=None, foursquare_id: Optional[str]=None, foursquare_type: Optional[str]=None, google_place_id: Optional[str]=None, google_place_type: Optional[str]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send information about a venue. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    latitude: Latitude of the venue
    longitude: Longitude of the venue
    title: Name of the venue
    address: Address of the venue
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    foursquare_id: Foursquare identifier of the venue
    foursquare_type: Foursquare type of the venue, if known. (For example, 'arts_entertainment/default', 'arts_entertainment/aquarium' or 'food/icecream'.)
    google_place_id: Google Places identifier of the venue
    google_place_type: Google Places type of the venue. (See supported types.)
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
    if foursquare_id is not None:
        payload['foursquare_id'] = foursquare_id
    if foursquare_type is not None:
        payload['foursquare_type'] = foursquare_type
    if google_place_id is not None:
        payload['google_place_id'] = google_place_id
    if google_place_type is not None:
        payload['google_place_type'] = google_place_type
    self._apply_send_options_json(payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    result = await self._call('sendVenue', json_body=payload)
    return Message.from_dict(result)
