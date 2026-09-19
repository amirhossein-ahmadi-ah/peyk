from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def approve_chat_join_request(self, chat_id: ChatId, user_id: int) -> bool:
    """Use this method to approve a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    user_id: Unique identifier of the target user

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload = {'chat_id': chat_id, 'user_id': user_id}
    return bool(await self._call('approveChatJoinRequest', json_body=payload))
