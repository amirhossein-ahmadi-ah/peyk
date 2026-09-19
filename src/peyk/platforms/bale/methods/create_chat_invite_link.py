from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Union

async def create_chat_invite_link(self, chat_id: Union[int, str]) -> Dict[str, object]:
    """Creates chat invite link through the Bale API.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``create_chat_invite_link``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.create_chat_invite_link(... )``'
    return await self._call('createChatInviteLink', json_body={'chat_id': chat_id})
