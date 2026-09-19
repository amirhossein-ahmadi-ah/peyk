from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
import orjson
from peyk.transport import FilePayload
from ..errors import TelegramAPIError, ResponseParameters
from ..models import *
from .. import models as _models
globals().update({k: v for k, v in vars(_models).items() if k.startswith('_')})
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_checklist(self, business_connection_id: str, chat_id: Union[int, str], checklist: InputChecklist, *, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, message_effect_id: Optional[str]=None, reply_parameters: Optional[ReplyParameters]=None, reply_markup: Optional[InlineKeyboardMarkup]=None) -> Message:
    """Use this method to send a checklist on behalf of a connected business account. On success, the sent Message is returned.

Args:
    business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    chat_id: Unique identifier for the target chat or username of the target bot in the format @username
    checklist: A JSON-serialized object for the checklist to send
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    message_effect_id: Unique identifier of the message effect to be added to the message
    reply_parameters: A JSON-serialized object for description of the message to reply to
    reply_markup: A JSON-serialized object for an inline keyboard

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if checklist is not None:
        payload['checklist'] = _serialize_api_value(checklist)
    if disable_notification is not None:
        payload['disable_notification'] = _serialize_api_value(disable_notification)
    if protect_content is not None:
        payload['protect_content'] = _serialize_api_value(protect_content)
    if message_effect_id is not None:
        payload['message_effect_id'] = _serialize_api_value(message_effect_id)
    if reply_parameters is not None:
        payload['reply_parameters'] = _serialize_api_value(reply_parameters)
    if reply_markup is not None:
        payload['reply_markup'] = _serialize_api_value(reply_markup)
    result = await self._call('sendChecklist', json_body=payload)
    return _parse_api_result('Message', result)
