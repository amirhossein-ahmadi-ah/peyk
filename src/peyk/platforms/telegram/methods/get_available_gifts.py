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

async def get_available_gifts(self) -> object:
    """Returns the list of gifts that can be sent by the bot to users and channel chats. Requires no parameters. Returns a Gifts object."""
    payload: Dict[str, object] = {}
    result = await self._call('getAvailableGifts', json_body=payload)
    return _parse_api_result('Gifts', result)
