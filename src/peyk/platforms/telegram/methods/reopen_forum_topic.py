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

async def reopen_forum_topic(self, chat_id: ChatId, message_thread_id: int) -> bool:
    """Use this method to reopen a closed topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    message_thread_id: Unique identifier for the target message thread of the forum topic

Returns:
    bool: Result returned by Telegram on successful execution."""
    return bool(await self._call('reopenForumTopic', json_body={'chat_id': chat_id, 'message_thread_id': message_thread_id}))
