from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Any, Mapping, Optional, Union
from ..types.media_input import MediaInput

async def send_animation(self, chat_id: Union[int, str], animation: MediaInput, *, caption: Optional[str]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[Mapping[str, object]]=None) -> Message:
    """Sends animation through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    animation: Value used by this operation.
    caption: Value used by this operation.
    reply_to_message_id: Value used by this operation.
    reply_markup: Keyboard or reply markup attached to the request.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``send_animation``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.send_animation(... )``'
    result = await self._send_media('sendAnimation', 'animation', chat_id, animation, caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup, default_filename='animation.gif')
    return Message.from_dict(result)
