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

async def save_prepared_keyboard_button(self, user_id: int, button: KeyboardButton) -> object:
    """Stores a keyboard button that can be used by a user within a Mini App. Returns a PreparedKeyboardButton object.

Args:
    user_id: Unique identifier of the target user that can use the button
    button: A JSON-serialized object describing the button to be saved. The button must be of the type request_users, request_chat, or request_managed_bot."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if button is not None:
        payload['button'] = _serialize_api_value(button)
    result = await self._call('savePreparedKeyboardButton', json_body=payload)
    return _parse_api_result('PreparedKeyboardButton', result)
