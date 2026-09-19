from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Union

async def send_chat_action(self, chat_id: Union[int, str], action: str) -> bool:
    """Sends chat action through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    action: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Send a chat action (typing indicator, upload progress, etc.).\n    \n            `action` must be one of: `typing`, `upload_photo`, `record_video`,\n            `upload_video`, `record_voice`, `upload_voice`, `choose_sticker`.\n    \n            Per docs.bale.ai, the status is displayed for up to 6 seconds.\n            Returns `True` on success.\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        action: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    '
    payload = {'chat_id': chat_id, 'action': action}
    return bool(await self._call('sendChatAction', json_body=payload))
