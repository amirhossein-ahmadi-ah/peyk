from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def upload_and_send_file(self, chat_id: str, file_bytes: bytes, *, file_type: str=FileTypeEnum.FILE, filename: str='file', content_type: str='application/octet-stream', text: Optional[str]=None, **send_kwargs: object) -> Message:
    """Performs the upload and send file operation for the Rubika client.

Args:
    chat_id: Identifier of the target chat.
    file_bytes: Value used by this operation.
    file_type: Value used by this operation.
    filename: Value used by this operation.
    content_type: Value used by this operation.
    text: Text content supplied to the operation.

Returns:
    Result produced by the Rubika operation."""
    '"""Rubika client operation ``upload_and_send_file``.\n\nArgs:\n    chat_id: Value accepted by this operation.\n    file_bytes: Value accepted by this operation.\n    file_type: Value accepted by this operation.\n    filename: Value accepted by this operation.\n    content_type: Value accepted by this operation.\n    text: Value accepted by this operation.\n\nReturns:\n    Message: The value returned by the Rubika API or the local helper.\n\nRaises:\n    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.\n"""'
    upload_url = await self.request_send_file(type=file_type)
    if not upload_url:
        raise RubikaAPIError('requestSendFile: empty upload_url in OK response', error_code='INVALID_RESPONSE', error_message='<empty upload_url>', raw=None)
    file_id = await self.upload_file(upload_url, file_bytes, filename=filename, content_type=content_type)
    if not file_id:
        raise RubikaAPIError('uploadFile: empty file_id in response', error_code='INVALID_RESPONSE', error_message='<empty file_id>', raw=None)
    return await self.send_file(chat_id, file_id, text=text, **send_kwargs)
