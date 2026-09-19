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

async def set_business_account_name(self, business_connection_id: str, first_name: str, *, last_name: Optional[str]=None) -> bool:
    """Changes the first and last name of a managed business account. Requires the can_change_name business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    first_name: The new value of the first name for the business account; 1-64 characters
    last_name: The new value of the last name for the business account; 0-64 characters

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if first_name is not None:
        payload['first_name'] = _serialize_api_value(first_name)
    if last_name is not None:
        payload['last_name'] = _serialize_api_value(last_name)
    result = await self._call('setBusinessAccountName', json_body=payload)
    return _parse_api_result('bool', result)
