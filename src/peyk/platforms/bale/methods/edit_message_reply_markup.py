from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Any, Dict, Mapping, Optional, Union

async def edit_message_reply_markup(self, chat_id: Union[int, str], message_id: int, *, reply_markup: Optional[Mapping[str, object]]=None) -> Message:
    """Edits message reply markup through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.
    reply_markup: Keyboard or reply markup attached to the request.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``edit_message_reply_markup``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.edit_message_reply_markup(... )``'
    payload: Dict[str, object] = {'chat_id': chat_id, 'message_id': message_id}
    if reply_markup is not None:
        payload['reply_markup'] = reply_markup
    result = await self._call('editMessageReplyMarkup', json_body=payload)
    return Message.from_dict(result)
