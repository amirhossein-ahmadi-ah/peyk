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

async def set_my_name(self, *, name: Optional[str]=None, language_code: Optional[str]=None) -> bool:
    """Use this method to change the bot's name. Returns True on success.

Args:
    name: New bot name; 0-64 characters. Pass an empty string to remove the dedicated name for the given language.
    language_code: A two-letter ISO 639-1 language code. If empty, the name will be shown to all users for whose language there is no dedicated name.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if name is not None:
        payload['name'] = name
    if language_code is not None:
        payload['language_code'] = language_code
    return bool(await self._call('setMyName', json_body=payload))
