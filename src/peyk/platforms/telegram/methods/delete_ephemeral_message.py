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

async def delete_ephemeral_message(self, chat_id: Union[int, str], receiver_user_id: Optional[int]=None, ephemeral_message_id: Optional[int]=None) -> bool:
    """Use this method to delete an ephemeral message. Note that it is not guaranteed that the user will receive the message deletion event, especially if they are offline. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    receiver_user_id: Identifier of the user who received the message
    ephemeral_message_id: Identifier of the ephemeral message to delete

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if receiver_user_id is not None:
        payload['receiver_user_id'] = _serialize_api_value(receiver_user_id)
    if ephemeral_message_id is not None:
        payload['ephemeral_message_id'] = _serialize_api_value(ephemeral_message_id)
    result = await self._call('deleteEphemeralMessage', json_body=payload)
    return _parse_api_result('bool', result)
