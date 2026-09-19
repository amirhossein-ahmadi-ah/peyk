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

async def remove_business_account_profile_photo(self, business_connection_id: str, *, is_public: Optional[bool]=None) -> bool:
    """Removes the current profile photo of a managed business account. Requires the can_edit_profile_photo business bot right. Returns True on success.

Args:
    business_connection_id: Unique identifier of the business connection
    is_public: Pass True to remove the public photo, which is visible even if the main photo is hidden by the business account's privacy settings. After the main photo is removed, the previous profile photo (if present) becomes the main photo.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if is_public is not None:
        payload['is_public'] = _serialize_api_value(is_public)
    result = await self._call('removeBusinessAccountProfilePhoto', json_body=payload)
    return _parse_api_result('bool', result)
