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

async def decline_suggested_post(self, chat_id: int, message_id: int, *, comment: Optional[str]=None) -> bool:
    """Use this method to decline a suggested post in a direct messages chat. The bot must have the 'can_manage_direct_messages' administrator right in the corresponding channel chat. Returns True on success.

Args:
    chat_id: Unique identifier for the target direct messages chat
    message_id: Identifier of a suggested post message to decline
    comment: Comment for the creator of the suggested post; 0-128 characters

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_id is not None:
        payload['message_id'] = _serialize_api_value(message_id)
    if comment is not None:
        payload['comment'] = _serialize_api_value(comment)
    result = await self._call('declineSuggestedPost', json_body=payload)
    return _parse_api_result('bool', result)
