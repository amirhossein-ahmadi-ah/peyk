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

async def read_business_message(self, business_connection_id: str, chat_id: int, message_id: int) -> bool:
    """Marks incoming message as read on behalf of a business account. Requires the can_read_messages business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection on behalf of which to read the message
    chat_id: Unique identifier of the chat in which the message was received. The chat must have been active in the last 24 hours.
    message_id: Unique identifier of the message to mark as read

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_id is not None:
        payload['message_id'] = _serialize_api_value(message_id)
    result = await self._call('readBusinessMessage', json_body=payload)
    return _parse_api_result('bool', result)
