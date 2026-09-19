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

async def refund_star_payment(self, user_id: int, telegram_payment_charge_id: str) -> bool:
    """Refunds a successful payment in Telegram Stars. Returns True on success.

Args:
    user_id: Identifier of the user whose payment will be refunded
    telegram_payment_charge_id: Telegram payment identifier

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if telegram_payment_charge_id is not None:
        payload['telegram_payment_charge_id'] = _serialize_api_value(telegram_payment_charge_id)
    result = await self._call('refundStarPayment', json_body=payload)
    return _parse_api_result('bool', result)
