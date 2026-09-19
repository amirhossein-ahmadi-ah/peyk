from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Union

async def copy_message(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int) -> Dict[str, object]:
    """Performs the copy message operation for the Bale client.

Args:
    chat_id: Identifier of the target chat.
    from_chat_id: Value used by this operation.
    message_id: Identifier of the target message.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``copy_message``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.copy_message(... )``'
    payload = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    return await self._call('copyMessage', json_body=payload)
