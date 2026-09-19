from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]


def _edit_target(self, *, chat_id: Optional[ChatId], message_id: Optional[int], inline_message_id: Optional[str], method: str) -> Dict[str, object]:
    """Telegram Bot API method ``_edit_target`` (T1-T5).

The implementation is preserves the existing implementation ``TelegramClient``
without changing request construction, return parsing, or error behavior."""
    if inline_message_id is not None:
        return {'inline_message_id': inline_message_id}
    if chat_id is None or message_id is None:
        raise ValueError(f'{method} requires chat_id+message_id or inline_message_id')
    return {'chat_id': chat_id, 'message_id': message_id}
