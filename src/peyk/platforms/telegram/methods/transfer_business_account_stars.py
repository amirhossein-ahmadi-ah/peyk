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

async def transfer_business_account_stars(self, business_connection_id: str, star_count: int) -> bool:
    """Transfers Telegram Stars from the business account balance to the bot's balance. Requires the can_transfer_stars business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    star_count: Number of Telegram Stars to transfer; 1-10000

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if star_count is not None:
        payload['star_count'] = _serialize_api_value(star_count)
    result = await self._call('transferBusinessAccountStars', json_body=payload)
    return _parse_api_result('bool', result)
