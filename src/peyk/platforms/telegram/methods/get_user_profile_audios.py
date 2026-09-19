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

async def get_user_profile_audios(self, user_id: int, *, offset: Optional[int]=None, limit: Optional[int]=None) -> object:
    """Use this method to get a list of profile audios for a user. Returns a UserProfileAudios object.

Args:
    user_id: Unique identifier of the target user
    offset: Sequential number of the first audio to be returned. By default, all audios are returned.
    limit: Limits the number of audios to be retrieved. Values between 1-100 are accepted. Defaults to 100."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if offset is not None:
        payload['offset'] = _serialize_api_value(offset)
    if limit is not None:
        payload['limit'] = _serialize_api_value(limit)
    result = await self._call('getUserProfileAudios', json_body=payload)
    return _parse_api_result('UserProfileAudios', result)
