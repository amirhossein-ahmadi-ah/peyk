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

async def remove_chat_verification(self, chat_id: Union[int, str]) -> bool:
    """Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot or channel in the format @username

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    result = await self._call('removeChatVerification', json_body=payload)
    return _parse_api_result('bool', result)
