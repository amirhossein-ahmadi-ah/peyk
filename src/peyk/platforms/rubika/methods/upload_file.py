from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def upload_file(self, upload_url: str, file_bytes: bytes, *, filename: str='file', content_type: str='application/octet-stream') -> str:
    """Performs the upload file operation for the Rubika client.

Args:
    upload_url: Value used by this operation.
    file_bytes: Value used by this operation.
    filename: Value used by this operation.
    content_type: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    'Upload file bytes to ``upload_url``; returns the ``file_id``.\n    \n    Args:\n        upload_url: Value of the declared parameter type.\n        file_bytes: Value of the declared parameter type.\n        filename: Value of the declared parameter type.\n        content_type: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``str``).\n    '
    from peyk.transport.multipart import FilePayload

    async def operation():
        """Performs the operation operation for the Rubika client."""
        'Executes the operation operation.\n        \n        Returns:\n            The operation result (``Any``).\n        '
        return await self._session.request('POST', upload_url, files={'file': FilePayload(content=file_bytes, filename=filename, content_type=content_type)})
    response = await run_with_retry(operation, self._retry_policy)
    data = response.json
    if isinstance(data, dict):
        if 'file_id' in data:
            return str(data['file_id'])
        nested = data.get('data')
        if isinstance(nested, dict) and 'file_id' in nested:
            return str(nested['file_id'])
    return ''
