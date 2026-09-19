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

async def edit_user_star_subscription(self, user_id: int, telegram_payment_charge_id: str, is_canceled: bool) -> bool:
    """Allows the bot to cancel or re-enable extension of a subscription paid in Telegram Stars. Returns True on success.

Args:
    user_id: Identifier of the user whose subscription will be edited
    telegram_payment_charge_id: Telegram payment identifier for the subscription
    is_canceled: Pass True to cancel extension of the user subscription; the subscription must be active up to the end of the current subscription period. Pass False to allow the user to re-enable a subscription that was previously canceled by the bot.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if telegram_payment_charge_id is not None:
        payload['telegram_payment_charge_id'] = _serialize_api_value(telegram_payment_charge_id)
    if is_canceled is not None:
        payload['is_canceled'] = _serialize_api_value(is_canceled)
    result = await self._call('editUserStarSubscription', json_body=payload)
    return _parse_api_result('bool', result)
