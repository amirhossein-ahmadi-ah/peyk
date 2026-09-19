from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Union
from ..types.media_input import MediaInput

async def set_chat_photo(self, chat_id: Union[int, str], photo: MediaInput) -> bool:
    """Updates chat photo through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    photo: Photo input supplied to the operation.

Returns:
    Result produced by the Bale operation."""
    'Set a new chat photo. Bale documents this as upload-only (`InputFile`).\n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        photo: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    '
    fields = {'chat_id': str(chat_id)}
    files = {'photo': self._as_file_payload(photo, default_filename='chat_photo.jpg')}
    return bool(await self._call('setChatPhoto', data=fields, files=files))
