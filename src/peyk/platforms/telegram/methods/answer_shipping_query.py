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

async def answer_shipping_query(self, shipping_query_id: str, ok: bool, *, shipping_options: Optional[List[ShippingOption]]=None, error_message: Optional[str]=None) -> bool:
    """If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned.

Args:
    shipping_query_id: Unique identifier for the query to be answered
    ok: Pass True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
    shipping_options: Required if ok is True. A JSON-serialized Array of available shipping options.
    error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. 'Sorry, delivery to your desired address is unavailable'). Telegram will display this message to the user.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if shipping_query_id is not None:
        payload['shipping_query_id'] = _serialize_api_value(shipping_query_id)
    if ok is not None:
        payload['ok'] = _serialize_api_value(ok)
    if shipping_options is not None:
        payload['shipping_options'] = _serialize_api_value(shipping_options)
    if error_message is not None:
        payload['error_message'] = _serialize_api_value(error_message)
    result = await self._call('answerShippingQuery', json_body=payload)
    return _parse_api_result('bool', result)
