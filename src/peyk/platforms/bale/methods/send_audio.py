from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Any, Mapping, Optional, Union
from ..types.media_input import MediaInput

async def send_audio(self, chat_id: Union[int, str], audio: MediaInput, *, caption: Optional[str]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[Mapping[str, object]]=None) -> Message:
    """Sends audio through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    audio: Audio input supplied to the operation.
    caption: Value used by this operation.
    reply_to_message_id: Value used by this operation.
    reply_markup: Keyboard or reply markup attached to the request.

Returns:
    Result produced by the Bale operation."""
    'Send an audio file (shown in-app as a music player entry).\n    \n            For voice-message-style playback instead, use `send_voice`.\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        audio: Value of the declared parameter type.\n        caption: Value of the declared parameter type.\n        reply_to_message_id: Value of the declared parameter type.\n        reply_markup: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Message``).\n    '
    result = await self._send_media('sendAudio', 'audio', chat_id, audio, caption, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup, default_filename='audio.mp3')
    return Message.from_dict(result)
