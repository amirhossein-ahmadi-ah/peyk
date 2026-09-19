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

async def replace_managed_bot_token(self, user_id: int) -> str:
    """Use this method to revoke the current token of a managed bot and generate a new one. Returns the new token as String on success.

Args:
    user_id: User identifier of the managed bot whose token will be replaced

Returns:
    str: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    result = await self._call('replaceManagedBotToken', json_body=payload)
    return _parse_api_result('str', result)
