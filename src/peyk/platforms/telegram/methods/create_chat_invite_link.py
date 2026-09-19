from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def create_chat_invite_link(self, chat_id: ChatId, *, name: Optional[str]=None, expire_date: Optional[int]=None, member_limit: Optional[int]=None, creates_join_request: Optional[bool]=None) -> ChatInviteLink:
    """Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. The link can be revoked using the method revokeChatInviteLink. Returns the new invite link as ChatInviteLink object.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    name: Invite link name; 0-32 characters
    expire_date: Point in time (Unix timestamp) when the link will expire
    member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
    creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified."""
    payload: Dict[str, object] = {'chat_id': chat_id}
    if name is not None:
        payload['name'] = name
    if expire_date is not None:
        payload['expire_date'] = expire_date
    if member_limit is not None:
        payload['member_limit'] = member_limit
    if creates_join_request is not None:
        payload['creates_join_request'] = creates_join_request
    result = await self._call('createChatInviteLink', json_body=payload)
    return ChatInviteLink.from_dict(result)
