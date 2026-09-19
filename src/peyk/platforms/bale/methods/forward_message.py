from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Union

async def forward_message(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int) -> Message:
    """Performs the forward message operation for the Bale client.

Args:
    chat_id: Identifier of the target chat.
    from_chat_id: Value used by this operation.
    message_id: Identifier of the target message.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``forward_message``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.forward_message(... )``'
    payload = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    result = await self._call('forwardMessage', json_body=payload)
    return Message.from_dict(result)
