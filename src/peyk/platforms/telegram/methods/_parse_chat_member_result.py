from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]


def _parse_chat_member_result(self, result: object) -> object:
    """Telegram Bot API method ``_parse_chat_member_result`` (T1-T5).

The implementation is preserves the existing implementation ``TelegramClient``
without changing request construction, return parsing, or error behavior."""
    member = type(self).chat_member_parser(result)
    if member is None:
        raise TelegramAPIError('getChatMember: empty member in response', error_code=0, description='<empty member>')
    return member
