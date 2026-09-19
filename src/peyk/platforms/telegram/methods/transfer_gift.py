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

async def transfer_gift(self, business_connection_id: str, owned_gift_id: str, new_owner_chat_id: int, *, star_count: Optional[int]=None) -> bool:
    """Transfers an owned unique gift to another user. Requires the can_transfer_and_upgrade_gifts business bot right. Requires can_transfer_stars business bot right if the transfer is paid. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    owned_gift_id: Unique identifier of the regular gift that should be transferred
    new_owner_chat_id: Unique identifier of the chat which will own the gift. The chat must be active in the last 24 hours.
    star_count: The amount of Telegram Stars that will be paid for the transfer from the business account balance. If positive, then the can_transfer_stars business bot right is required.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if owned_gift_id is not None:
        payload['owned_gift_id'] = _serialize_api_value(owned_gift_id)
    if new_owner_chat_id is not None:
        payload['new_owner_chat_id'] = _serialize_api_value(new_owner_chat_id)
    if star_count is not None:
        payload['star_count'] = _serialize_api_value(star_count)
    result = await self._call('transferGift', json_body=payload)
    return _parse_api_result('bool', result)
