from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Union

async def get_chat_members_count(self, chat_id: Union[int, str]) -> int:
    """Retrieves chat members count from the Bale API.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``get_chat_members_count``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.get_chat_members_count(... )``'
    return await self._get_chat_member_count(chat_id)
