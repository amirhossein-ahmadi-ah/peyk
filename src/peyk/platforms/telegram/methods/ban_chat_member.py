from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def ban_chat_member(self, chat_id: ChatId, user_id: int, *, until_date: Optional[int]=None, revoke_messages: Optional[bool]=None) -> bool:
    """Use this method to ban a user in a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.

Args:
    chat_id: Unique identifier for the target group or username of the target supergroup or channel in the format @username
    user_id: Unique identifier of the target user
    until_date: Date when the user will be unbanned; Unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.
    revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'user_id': user_id}
    if until_date is not None:
        payload['until_date'] = until_date
    if revoke_messages is not None:
        payload['revoke_messages'] = revoke_messages
    return bool(await self._call('banChatMember', json_body=payload))
