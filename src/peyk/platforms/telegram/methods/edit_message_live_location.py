from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def edit_message_live_location(self, latitude: float, longitude: float, *, chat_id: Optional[ChatId]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, live_period: Optional[int]=None, horizontal_accuracy: Optional[float]=None, heading: Optional[int]=None, proximity_alert_radius: Optional[int]=None, reply_markup: Optional[ReplyMarkup]=None) -> Union[Message, bool]:
    """Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

Args:
    latitude: Latitude of new location
    longitude: Longitude of new location
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
    message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    live_period: New period in seconds during which the location can be updated, starting from the message send date. If 0x7FFFFFFF is specified, then the location can be updated forever. Otherwise, the new value must not exceed the current live_period by more than a day, and the live location expiration date must remain within the next 90 days. If not specified, then live_period remains unchanged.
    horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
    heading: Direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
    proximity_alert_radius: The maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
    reply_markup: A JSON-serialized object for a new inline keyboard

Returns:
    Union[Message, bool]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = self._edit_target(chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, method='edit_message_live_location')
    payload['latitude'] = latitude
    payload['longitude'] = longitude
    if live_period is not None:
        payload['live_period'] = live_period
    if horizontal_accuracy is not None:
        payload['horizontal_accuracy'] = horizontal_accuracy
    if heading is not None:
        payload['heading'] = heading
    if proximity_alert_radius is not None:
        payload['proximity_alert_radius'] = proximity_alert_radius
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('editMessageLiveLocation', json_body=payload)
    if isinstance(result, bool):
        return result
    return Message.from_dict(result)
