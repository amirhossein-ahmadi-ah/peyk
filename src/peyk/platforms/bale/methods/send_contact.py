from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Any, Dict, Mapping, Optional, Union

async def send_contact(self, chat_id: Union[int, str], phone_number: str, first_name: str, *, last_name: Optional[str]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[Mapping[str, object]]=None) -> Message:
    """Sends contact through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    phone_number: Value used by this operation.
    first_name: Value used by this operation.
    last_name: Value used by this operation.
    reply_to_message_id: Value used by this operation.
    reply_markup: Keyboard or reply markup attached to the request.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``send_contact``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.send_contact(... )``'
    payload: Dict[str, object] = {'chat_id': chat_id, 'phone_number': phone_number, 'first_name': first_name}
    if last_name is not None:
        payload['last_name'] = last_name
    if reply_to_message_id is not None:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup is not None:
        payload['reply_markup'] = reply_markup
    result = await self._call('sendContact', json_body=payload)
    return Message.from_dict(result)
