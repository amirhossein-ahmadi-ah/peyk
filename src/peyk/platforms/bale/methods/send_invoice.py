from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Any, Dict, Mapping, Optional, Sequence, Union

async def send_invoice(self, chat_id: Union[int, str], title: str, description: str, payload_: str, provider_token: str, prices: Sequence[Mapping[str, object]], *, photo_url: Optional[str]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[Mapping[str, object]]=None) -> Message:
    """Sends invoice through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    title: Title to apply to the target resource.
    description: Description to apply to the target resource.
    payload_: Value used by this operation.
    provider_token: Value used by this operation.
    prices: Value used by this operation.
    photo_url: Value used by this operation.
    reply_to_message_id: Value used by this operation.
    reply_markup: Keyboard or reply markup attached to the request.

Returns:
    Result produced by the Bale operation."""
    "Send a payment request (invoice).\n    \n            `payload_` is Bale's own `payload` field (an opaque, bot-defined\n            string echoed back on successful payment) -- named with a\n            trailing underscore here only to avoid shadowing Python's\n            builtin `payload` variable used throughout this module, not\n            because of any keyword collision like `from`/`from_`.\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        title: Value of the declared parameter type.\n        description: Value of the declared parameter type.\n        payload_: Value of the declared parameter type.\n        provider_token: Value of the declared parameter type.\n        prices: Value of the declared parameter type.\n        photo_url: Value of the declared parameter type.\n        reply_to_message_id: Value of the declared parameter type.\n        reply_markup: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Message``).\n    "
    body: Dict[str, object] = {'chat_id': chat_id, 'title': title, 'description': description, 'payload': payload_, 'provider_token': provider_token, 'prices': list(prices)}
    if photo_url is not None:
        body['photo_url'] = photo_url
    if reply_to_message_id is not None:
        body['reply_to_message_id'] = reply_to_message_id
    if reply_markup is not None:
        body['reply_markup'] = reply_markup
    result = await self._call('sendInvoice', json_body=body)
    return Message.from_dict(result)
