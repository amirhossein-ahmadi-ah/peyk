from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Mapping, Sequence

async def create_new_sticker_set(self, user_id: int, name: str, title: str, stickers: Sequence[Mapping[str, object]]) -> bool:
    """Creates new sticker set through the Bale API.

Args:
    user_id: Identifier of the target user.
    name: Value used by this operation.
    title: Title to apply to the target resource.
    stickers: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    "Create a new sticker set owned by `user_id`.\n    \n            `stickers` is a list of raw `InputSticker`-shaped mappings (1-50\n            entries per docs.bale.ai) -- docs.bale.ai does not spell out\n            `InputSticker`'s exact fields on the page fetched for this pass,\n            so this is passed through as-is (JSON-serializable dicts) rather\n            than guessing a dataclass shape; see `docs/decisions.md`.\n            \n    \n    Args:\n        user_id: Value of the declared parameter type.\n        name: Value of the declared parameter type.\n        title: Value of the declared parameter type.\n        stickers: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    "
    payload = {'user_id': user_id, 'name': name, 'title': title, 'sticker': list(stickers)}
    return bool(await self._call('createNewStickerSet', json_body=payload))
