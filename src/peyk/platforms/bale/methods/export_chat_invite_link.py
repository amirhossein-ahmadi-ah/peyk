from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Union

async def export_chat_invite_link(self, chat_id: Union[int, str]) -> str:
    """Performs the export chat invite link operation for the Bale client.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the Bale operation."""
    "Generate (or regenerate) a chat's primary invite link.\n    \n            Per docs.bale.ai, `exportChatInviteLink` is distinct from\n            `createChatInviteLink`/`revokeChatInviteLink`: it returns the\n            invite link directly as the `result` (a bare string), not a\n            dict of invite-link metadata.\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``str``).\n    "
    result = await self._call('exportChatInviteLink', json_body={'chat_id': chat_id})
    return str(result)
