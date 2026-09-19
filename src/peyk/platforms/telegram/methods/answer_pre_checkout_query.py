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

async def answer_pre_checkout_query(self, pre_checkout_query_id: str, ok: bool, *, error_message: Optional[str]=None) -> bool:
    """Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.

Args:
    pre_checkout_query_id: Unique identifier for the query to be answered
    ok: Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
    error_message: Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if pre_checkout_query_id is not None:
        payload['pre_checkout_query_id'] = _serialize_api_value(pre_checkout_query_id)
    if ok is not None:
        payload['ok'] = _serialize_api_value(ok)
    if error_message is not None:
        payload['error_message'] = _serialize_api_value(error_message)
    result = await self._call('answerPreCheckoutQuery', json_body=payload)
    return _parse_api_result('bool', result)
