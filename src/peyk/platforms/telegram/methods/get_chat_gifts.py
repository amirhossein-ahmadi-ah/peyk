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

async def get_chat_gifts(self, chat_id: Union[int, str], *, exclude_unsaved: Optional[bool]=None, exclude_saved: Optional[bool]=None, exclude_unlimited: Optional[bool]=None, exclude_limited_upgradable: Optional[bool]=None, exclude_limited_non_upgradable: Optional[bool]=None, exclude_from_blockchain: Optional[bool]=None, exclude_unique: Optional[bool]=None, sort_by_price: Optional[bool]=None, offset: Optional[str]=None, limit: Optional[int]=None) -> OwnedGifts:
    """Returns the gifts owned by a chat. Returns OwnedGifts on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    exclude_unsaved: Pass True to exclude gifts that aren't saved to the chat's profile page. Always True, unless the bot has the can_post_messages administrator right in the channel.
    exclude_saved: Pass True to exclude gifts that are saved to the chat's profile page. Always False, unless the bot has the can_post_messages administrator right in the channel.
    exclude_unlimited: Pass True to exclude gifts that can be purchased an unlimited number of times
    exclude_limited_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can be upgraded to unique
    exclude_limited_non_upgradable: Pass True to exclude gifts that can be purchased a limited number of times and can't be upgraded to unique
    exclude_from_blockchain: Pass True to exclude gifts that were assigned from the TON blockchain and can't be resold or transferred in Telegram
    exclude_unique: Pass True to exclude unique gifts
    sort_by_price: Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.
    offset: Offset of the first entry to return as received from the previous request; use an empty string to get the first chunk of results
    limit: The maximum number of gifts to be returned; 1-100. Defaults to 100."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
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
    if exclude_from_blockchain is not None:
        payload['exclude_from_blockchain'] = _serialize_api_value(exclude_from_blockchain)
    if exclude_unique is not None:
        payload['exclude_unique'] = _serialize_api_value(exclude_unique)
    if sort_by_price is not None:
        payload['sort_by_price'] = _serialize_api_value(sort_by_price)
    if offset is not None:
        payload['offset'] = _serialize_api_value(offset)
    if limit is not None:
        payload['limit'] = _serialize_api_value(limit)
    result = await self._call('getChatGifts', json_body=payload)
    return _parse_api_result('OwnedGifts', result)
