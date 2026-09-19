from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Union

async def revoke_chat_invite_link(self, chat_id: Union[int, str], invite_link: str) -> Dict[str, object]:
    """Performs the revoke chat invite link operation for the Bale client.

Args:
    chat_id: Identifier of the target chat.
    invite_link: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``revoke_chat_invite_link``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.revoke_chat_invite_link(... )``'
    payload = {'chat_id': chat_id, 'invite_link': invite_link}
    return await self._call('revokeChatInviteLink', json_body=payload)
