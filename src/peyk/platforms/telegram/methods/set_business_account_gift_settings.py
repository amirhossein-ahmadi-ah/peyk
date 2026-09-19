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

async def set_business_account_gift_settings(self, business_connection_id: str, show_gift_button: bool, accepted_gift_types: AcceptedGiftTypes) -> bool:
    """Changes the privacy settings pertaining to incoming gifts in a managed business account. Requires the can_change_gift_settings business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    show_gift_button: Pass True if a button for sending a gift to the user or by the business account must always be shown in the input field
    accepted_gift_types: Types of gifts accepted by the business account

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if show_gift_button is not None:
        payload['show_gift_button'] = _serialize_api_value(show_gift_button)
    if accepted_gift_types is not None:
        payload['accepted_gift_types'] = _serialize_api_value(accepted_gift_types)
    result = await self._call('setBusinessAccountGiftSettings', json_body=payload)
    return _parse_api_result('bool', result)
