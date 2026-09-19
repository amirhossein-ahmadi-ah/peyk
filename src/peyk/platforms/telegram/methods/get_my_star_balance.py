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

async def get_my_star_balance(self) -> object:
    """A method to get the current Telegram Stars balance of the bot. Requires no parameters. On success, returns a StarAmount object."""
    payload: Dict[str, object] = {}
    result = await self._call('getMyStarBalance', json_body=payload)
    return _parse_api_result('StarAmount', result)
