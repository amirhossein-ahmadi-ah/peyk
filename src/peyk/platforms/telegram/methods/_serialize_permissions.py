from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]


def _serialize_permissions(value: Union[ChatPermissions, Mapping[str, object]]) -> Dict[str, object]:
    """Telegram Bot API method ``_serialize_permissions`` (T1-T5).

The implementation is preserves the existing implementation ``TelegramClient``
without changing request construction, return parsing, or error behavior."""
    return value.to_dict() if isinstance(value, ChatPermissions) else dict(value)
