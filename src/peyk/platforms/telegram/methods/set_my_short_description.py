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

async def set_my_short_description(self, *, short_description: Optional[str]=None, language_code: Optional[str]=None) -> bool:
    """Use this method to change the bot's short description, which is shown on the bot's profile page and is sent together with the link when users share the bot. Returns True on success.

Args:
    short_description: New short description for the bot; 0-120 characters. Pass an empty string to remove the dedicated short description for the given language.
    language_code: A two-letter ISO 639-1 language code. If empty, the short description will be applied to all users for whose language there is no dedicated short description.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if short_description is not None:
        payload['short_description'] = short_description
    if language_code is not None:
        payload['language_code'] = language_code
    return bool(await self._call('setMyShortDescription', json_body=payload))
