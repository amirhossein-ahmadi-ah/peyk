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

async def get_star_transactions(self, *, offset: Optional[int]=None, limit: Optional[int]=None) -> object:
    """Returns the bot's Telegram Star transactions in chronological order. On success, returns a StarTransactions object.

Args:
    offset: Number of transactions to skip in the response
    limit: The maximum number of transactions to be retrieved. Values between 1-100 are accepted. Defaults to 100."""
    payload: Dict[str, object] = {}
    if offset is not None:
        payload['offset'] = _serialize_api_value(offset)
    if limit is not None:
        payload['limit'] = _serialize_api_value(limit)
    result = await self._call('getStarTransactions', json_body=payload)
    return _parse_api_result('StarTransactions', result)
