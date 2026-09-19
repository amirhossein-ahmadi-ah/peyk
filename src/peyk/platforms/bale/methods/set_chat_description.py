from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Union

async def set_chat_description(self, chat_id: Union[int, str], description: str) -> bool:
    """Updates chat description through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    description: Description to apply to the target resource.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``set_chat_description``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.set_chat_description(... )``'
    payload = {'chat_id': chat_id, 'description': description}
    return bool(await self._call('setChatDescription', json_body=payload))
