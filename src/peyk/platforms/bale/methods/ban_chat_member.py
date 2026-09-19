from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Union

async def ban_chat_member(self, chat_id: Union[int, str], user_id: int) -> bool:
    """Performs the ban chat member operation for the Bale client.

Args:
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``ban_chat_member``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.ban_chat_member(... )``'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    return bool(await self._call('banChatMember', json_body=payload))
