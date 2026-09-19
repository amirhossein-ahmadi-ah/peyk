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

def build_inline_keyboard_button(text: str, callback_data: str) -> InlineKeyboardButton:
    """Provides the build inline keyboard button operation for the Telegram integration.

Args:
    text: Text supplied to the operation.
    callback_data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Build an `InlineKeyboardButton`, validating `callback_data` first.\n    \n        Same role as the Bale-side helper (separate code until the shared\n        base is extracted): fail fast client-side on the 1-64 byte UTF-8\n        limit instead of sending a request the server will reject.\n        \n    \n    Args:\n        text: Value of the declared parameter type.\n        callback_data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``InlineKeyboardButton``).\n    '
    from ..client import TelegramClient
    payload = TelegramClient._build_inline_keyboard_button_payload(text, callback_data)
    return InlineKeyboardButton(**payload)
