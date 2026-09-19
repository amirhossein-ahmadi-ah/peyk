from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import ChatMember
from typing import List, Union

async def get_chat_administrators(self, chat_id: Union[int, str]) -> List[ChatMember]:
    """Retrieves chat administrators from the Bale API.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the Bale operation."""
    'Get a list of chat administrators.\n    \n            Per docs.bale.ai, returns an array of `ChatMember` objects\n            describing the current administrators of the chat.\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``List[ChatMember]``).\n    '
    result = await self._call('getChatAdministrators', json_body={'chat_id': chat_id})
    return [ChatMember.from_dict(item) for item in result or []]
