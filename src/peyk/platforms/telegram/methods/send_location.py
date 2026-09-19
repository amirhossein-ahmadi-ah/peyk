from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_location(self, chat_id: ChatId, latitude: float, longitude: float, *, message_thread_id: Optional[int]=None, horizontal_accuracy: Optional[float]=None, live_period: Optional[int]=None, heading: Optional[int]=None, proximity_alert_radius: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send point on the map. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    latitude: Latitude of the location
    longitude: Longitude of the location
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
    live_period: Period in seconds during which the location will be updated (see Live Locations), must be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely. Must be 0 for ephemeral messages.
    heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
    proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
    if horizontal_accuracy is not None:
        payload['horizontal_accuracy'] = horizontal_accuracy
    if live_period is not None:
        payload['live_period'] = live_period
    if heading is not None:
        payload['heading'] = heading
    if proximity_alert_radius is not None:
        payload['proximity_alert_radius'] = proximity_alert_radius
    self._apply_send_options_json(payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    result = await self._call('sendLocation', json_body=payload)
    return Message.from_dict(result)
