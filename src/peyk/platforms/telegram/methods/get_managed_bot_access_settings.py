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

async def get_managed_bot_access_settings(self, user_id: Optional[int]=None, *, chat_id: Optional[int]=None) -> BotAccessSettings:
    """Use this method to get the access settings of a managed bot. Returns a BotAccessSettings object on success.

Args:
    user_id: User identifier of the managed bot whose access settings will be returned
    chat_id: Value accepted by this operation.

Returns:
    BotAccessSettings: Result returned by Telegram on successful execution."""
    if user_id is None:
        user_id = chat_id
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    result = await self._call('getManagedBotAccessSettings', json_body=payload)
    return _parse_api_result('BotAccessSettings', result)
