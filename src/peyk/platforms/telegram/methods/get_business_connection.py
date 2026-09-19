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

async def get_business_connection(self, business_connection_id: str) -> BusinessConnection:
    """Use this method to get information about the connection of the bot with a business account. Returns a BusinessConnection object on success.

Args:
    business_connection_id: Unique identifier of the business connection

Returns:
    BusinessConnection: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    result = await self._call('getBusinessConnection', json_body=payload)
    return _parse_api_result('BusinessConnection', result)
