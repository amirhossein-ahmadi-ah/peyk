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

async def get_my_short_description(self, *, language_code: Optional[str]=None) -> BotShortDescription:
    """Use this method to get the current bot short description for the given user language. Returns BotShortDescription on success.

Args:
    language_code: A two-letter ISO 639-1 language code or an empty string"""
    payload: Dict[str, object] = {}
    if language_code is not None:
        payload['language_code'] = language_code
    return BotShortDescription.from_dict(await self._call('getMyShortDescription', json_body=payload))
