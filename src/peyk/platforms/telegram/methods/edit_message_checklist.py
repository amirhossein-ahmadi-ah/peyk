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

async def edit_message_checklist(self, business_connection_id: str, chat_id: Union[int, str], message_id: int, checklist: InputChecklist, *, reply_markup: Optional[InlineKeyboardMarkup]=None) -> Message:
    """Use this method to edit a checklist on behalf of a connected business account. On success, the edited Message is returned.

Args:
    business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    chat_id: Unique identifier for the target chat or username of the target bot in the format @username
    message_id: Unique identifier for the target message
    checklist: A JSON-serialized object for the new checklist
    reply_markup: A JSON-serialized object for the new inline keyboard for the message

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_id is not None:
        payload['message_id'] = _serialize_api_value(message_id)
    if checklist is not None:
        payload['checklist'] = _serialize_api_value(checklist)
    if reply_markup is not None:
        payload['reply_markup'] = _serialize_api_value(reply_markup)
    result = await self._call('editMessageChecklist', json_body=payload)
    return _parse_api_result('Message', result)
