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

async def gift_premium_subscription(self, user_id: int, month_count: int, star_count: Optional[int]=None, *, text: Optional[str]=None, text_parse_mode: Optional[str]=None, text_entities: Optional[List[MessageEntity]]=None) -> bool:
    """Gifts a Telegram Premium subscription to the given user. Returns True on success.

Args:
    user_id: Unique identifier of the target user who will receive a Telegram Premium subscription
    month_count: Number of months the Telegram Premium subscription will be active for the user; must be one of 3, 6, or 12
    star_count: Number of Telegram Stars to pay for the Telegram Premium subscription; must be 1000 for 3 months, 1500 for 6 months, and 2500 for 12 months
    text: Text that will be shown along with the service message about the subscription; 0-128 characters
    text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than 'bold', 'italic', 'underline', 'strikethrough', 'spoiler', 'custom_emoji', and 'date_time' are ignored.
    text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than 'bold', 'italic', 'underline', 'strikethrough', 'spoiler', 'custom_emoji', and 'date_time' are ignored.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if month_count is not None:
        payload['month_count'] = _serialize_api_value(month_count)
    if star_count is not None:
        payload['star_count'] = _serialize_api_value(star_count)
    if text is not None:
        payload['text'] = _serialize_api_value(text)
    if text_parse_mode is not None:
        payload['text_parse_mode'] = _serialize_api_value(text_parse_mode)
    if text_entities is not None:
        payload['text_entities'] = _serialize_api_value(text_entities)
    result = await self._call('giftPremiumSubscription', json_body=payload)
    return _parse_api_result('bool', result)
