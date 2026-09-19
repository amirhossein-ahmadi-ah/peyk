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

async def set_my_profile_photo(self, photo: InputProfilePhoto) -> bool:
    """Changes the profile photo of the bot. Returns True on success.

Args:
    photo: The new profile photo to set

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if photo is not None:
        payload['photo'] = _serialize_api_value(photo)
    result = await self._call('setMyProfilePhoto', json_body=payload)
    return _parse_api_result('bool', result)
