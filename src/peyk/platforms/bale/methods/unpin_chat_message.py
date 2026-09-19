from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Union

async def unpin_chat_message(self, chat_id: Union[int, str], message_id: int) -> bool:
    """Performs the unpin chat message operation for the Bale client.

Args:
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``unpin_chat_message``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.unpin_chat_message(... )``'
    payload = {'chat_id': chat_id, 'message_id': message_id}
    return bool(await self._call('unpinChatMessage', json_body=payload))
