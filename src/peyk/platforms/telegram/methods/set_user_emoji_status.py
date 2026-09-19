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

async def set_user_emoji_status(self, user_id: int, *, emoji_status_custom_emoji_id: Optional[str]=None, emoji_status_expiration_date: Optional[int]=None) -> bool:
    """Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method requestEmojiStatusAccess. Returns True on success.

Args:
    user_id: Unique identifier of the target user
    emoji_status_custom_emoji_id: Custom emoji identifier of the emoji status to set. Pass an empty string to remove the status.
    emoji_status_expiration_date: Expiration date of the emoji status, if any

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if emoji_status_custom_emoji_id is not None:
        payload['emoji_status_custom_emoji_id'] = _serialize_api_value(emoji_status_custom_emoji_id)
    if emoji_status_expiration_date is not None:
        payload['emoji_status_expiration_date'] = _serialize_api_value(emoji_status_expiration_date)
    result = await self._call('setUserEmojiStatus', json_body=payload)
    return _parse_api_result('bool', result)
