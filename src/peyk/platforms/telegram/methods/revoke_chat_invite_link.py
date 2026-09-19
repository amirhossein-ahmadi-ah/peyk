from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def revoke_chat_invite_link(self, chat_id: ChatId, invite_link: str) -> ChatInviteLink:
    """Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the revoked invite link as ChatInviteLink object.

Args:
    chat_id: Unique identifier of the target chat or username of the target channel in the format @username
    invite_link: The invite link to revoke"""
    payload = {'chat_id': chat_id, 'invite_link': invite_link}
    result = await self._call('revokeChatInviteLink', json_body=payload)
    return ChatInviteLink.from_dict(result)
