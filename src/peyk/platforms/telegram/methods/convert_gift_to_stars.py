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

async def convert_gift_to_stars(self, business_connection_id: str, owned_gift_id: str) -> bool:
    """Converts a given regular gift to Telegram Stars. Requires the can_convert_gifts_to_stars business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    owned_gift_id: Unique identifier of the regular gift that should be converted to Telegram Stars

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if owned_gift_id is not None:
        payload['owned_gift_id'] = _serialize_api_value(owned_gift_id)
    result = await self._call('convertGiftToStars', json_body=payload)
    return _parse_api_result('bool', result)
