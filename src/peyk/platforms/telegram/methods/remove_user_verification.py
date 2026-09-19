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

async def remove_user_verification(self, user_id: int) -> bool:
    """Removes verification from a user who is currently verified on behalf of the organization represented by the bot. Returns True on success.

Args:
    user_id: Unique identifier of the target user

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    result = await self._call('removeUserVerification', json_body=payload)
    return _parse_api_result('bool', result)
