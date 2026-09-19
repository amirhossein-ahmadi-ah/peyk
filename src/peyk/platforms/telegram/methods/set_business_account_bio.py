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

async def set_business_account_bio(self, business_connection_id: str, *, bio: Optional[str]=None) -> bool:
    """Changes the bio of a managed business account. Requires the can_change_bio business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    bio: The new value of the bio for the business account; 0-140 characters

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if bio is not None:
        payload['bio'] = _serialize_api_value(bio)
    result = await self._call('setBusinessAccountBio', json_body=payload)
    return _parse_api_result('bool', result)
