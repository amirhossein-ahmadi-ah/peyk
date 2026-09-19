from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Mapping

async def add_sticker_to_set(self, user_id: int, name: str, sticker: Mapping[str, object]) -> bool:
    """Performs the add sticker to set operation for the Bale client.

Args:
    user_id: Identifier of the target user.
    name: Value used by this operation.
    sticker: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``add_sticker_to_set``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.add_sticker_to_set(... )``'
    payload = {'user_id': user_id, 'name': name, 'sticker': dict(sticker)}
    return bool(await self._call('addStickerToSet', json_body=payload))
