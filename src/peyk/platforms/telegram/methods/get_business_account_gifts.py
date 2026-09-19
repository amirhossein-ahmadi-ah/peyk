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

async def get_business_account_gifts(self, business_connection_id: str, *, exclude_unsaved: Optional[bool]=None, exclude_saved: Optional[bool]=None, exclude_unlimited: Optional[bool]=None, exclude_limited_upgradable: Optional[bool]=None, exclude_limited_non_upgradable: Optional[bool]=None, exclude_unique: Optional[bool]=None, exclude_from_blockchain: Optional[bool]=None, sort_by_price: Optional[bool]=None, offset: Optional[str]=None, limit: Optional[int]=None) -> OwnedGifts:
    """Returns the gifts received and owned by a managed business account. Requires the can_view_gifts_and_stars business bot right. Returns OwnedGifts on success.

Args:
    business_connection_id: Unique identifier of the business connection
    exclude_unsaved: Pass True to exclude gifts that aren't saved to the account's profile page
    exclude_saved: Pass True to exclude gifts that are saved to the account's profile page
    exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
    exclude_limited_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can be upgraded to unique
    exclude_limited_non_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can't be upgraded to unique
    exclude_unique: Pass True to exclude unique gifts
    exclude_from_blockchain: Pass True to exclude gifts that were assigned from the TON blockchain and can't be resold or transferred in Telegram
    sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
    offset: Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
    limit: The maximum number of gifts to be returned; 1-100. Defaults to 100."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if exclude_unsaved is not None:
        payload['exclude_unsaved'] = _serialize_api_value(exclude_unsaved)
    if exclude_saved is not None:
        payload['exclude_saved'] = _serialize_api_value(exclude_saved)
    if exclude_unlimited is not None:
        payload['exclude_unlimited'] = _serialize_api_value(exclude_unlimited)
    if exclude_limited_upgradable is not None:
        payload['exclude_limited_upgradable'] = _serialize_api_value(exclude_limited_upgradable)
    if exclude_limited_non_upgradable is not None:
        payload['exclude_limited_non_upgradable'] = _serialize_api_value(exclude_limited_non_upgradable)
    if exclude_unique is not None:
        payload['exclude_unique'] = _serialize_api_value(exclude_unique)
    if exclude_from_blockchain is not None:
        payload['exclude_from_blockchain'] = _serialize_api_value(exclude_from_blockchain)
    if sort_by_price is not None:
        payload['sort_by_price'] = _serialize_api_value(sort_by_price)
    if offset is not None:
        payload['offset'] = _serialize_api_value(offset)
    if limit is not None:
        payload['limit'] = _serialize_api_value(limit)
    result = await self._call('getBusinessAccountGifts', json_body=payload)
    return _parse_api_result('OwnedGifts', result)
