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

async def set_business_account_username(self, business_connection_id: str, *, username: Optional[str]=None) -> bool:
    """Changes the username of a managed business account. Requires the can_change_username business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    username: The new value of the username for the business account; 0-32 characters

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if username is not None:
        payload['username'] = _serialize_api_value(username)
    result = await self._call('setBusinessAccountUsername', json_body=payload)
    return _parse_api_result('bool', result)
