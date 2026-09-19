from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import File
from ..types.media_input import MediaInput

async def upload_sticker_file(self, user_id: int, sticker: MediaInput) -> File:
    """Performs the upload sticker file operation for the Bale client.

Args:
    user_id: Identifier of the target user.
    sticker: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Upload a sticker file for later use in `create_new_sticker_set`/\n            `add_sticker_to_set`. Per docs.bale.ai, must be `.WEBP`, `.PNG`,\n            `.TGS`, or `.WEBM`.\n            \n    \n    Args:\n        user_id: Value of the declared parameter type.\n        sticker: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``File``).\n    '
    fields = {'user_id': str(user_id)}
    files = {'sticker': self._as_file_payload(sticker, default_filename='sticker.webp')}
    result = await self._call('uploadStickerFile', data=fields, files=files)
    return File.from_dict(result)
