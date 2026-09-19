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

async def upgrade_gift(self, business_connection_id: str, owned_gift_id: str, *, keep_original_details: Optional[bool]=None, star_count: Optional[int]=None) -> bool:
    """Upgrades a given regular gift to a unique gift. Requires the can_transfer_and_upgrade_gifts business bot right. Additionally requires the can_transfer_stars business bot right if the upgrade is paid. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    owned_gift_id: Unique identifier of the regular gift that should be upgraded to a unique one
    keep_original_details: Pass True to keep the original gift text, sender and receiver in the upgraded gift
    star_count: The amount of Telegram Stars that will be paid for the upgrade from the business account balance. If gift.prepaid_upgrade_star_count > 0, then pass 0, otherwise, the can_transfer_stars business bot right is required and gift.upgrade_star_count must be passed.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if owned_gift_id is not None:
        payload['owned_gift_id'] = _serialize_api_value(owned_gift_id)
    if keep_original_details is not None:
        payload['keep_original_details'] = _serialize_api_value(keep_original_details)
    if star_count is not None:
        payload['star_count'] = _serialize_api_value(star_count)
    result = await self._call('upgradeGift', json_body=payload)
    return _parse_api_result('bool', result)
