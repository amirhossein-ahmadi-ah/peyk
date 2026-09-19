from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Any, Mapping, Optional, Union
from ..types.media_input import MediaInput

async def send_voice(self, chat_id: Union[int, str], voice: MediaInput, *, caption: Optional[str]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[Mapping[str, object]]=None) -> Message:
    """Sends voice through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    voice: Voice input supplied to the operation.
    caption: Value used by this operation.
    reply_to_message_id: Value used by this operation.
    reply_markup: Keyboard or reply markup attached to the request.

Returns:
    Result produced by the Bale operation."""
    'Send a voice message (played in-app with a voice-message UI).\n    \n            Per docs.bale.ai, for URL/file_id-free uploads the source file\n            must be `audio/ogg` and under 1MB to render as a voice message.\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        voice: Value of the declared parameter type.\n        caption: Value of the declared parameter type.\n        reply_to_message_id: Value of the declared parameter type.\n        reply_markup: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Message``).\n    '
    result = await self._send_media('sendVoice', 'voice', chat_id, voice, caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup, default_filename='voice.ogg')
    return Message.from_dict(result)
