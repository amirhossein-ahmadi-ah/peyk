from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union

from peyk.transport import run_with_retry

from ..errors import RubikaAPIError, error_for_envelope
from ..models import (
    ChatTypeEnum,
    FileTypeEnum,
    ForwardedFromEnum,
    PollStatusEnum,
    ButtonSelectionTypeEnum,
    ButtonSelectionSearchEnum,
    ButtonSelectionGetEnum,
    ButtonCalendarTypeEnum,
    ButtonTextboxTypeKeypadEnum,
    ButtonTextboxTypeLineEnum,
    ButtonLocationTypeEnum,
    MessageSenderEnum,
    UpdateTypeEnum,
    ChatKeypadTypeEnum,
    UpdateEndpointTypeEnum,
    MetadataTypeEnum,
    EnumChatAccess,
    EventTypeEnum,
    EventJoinTypeEnum,
    ButtonTypeEnum,
    File,
    Location,
    Chat,
    Bot,
    BotCommand,
    Sticker,
    ContactMessage,
    PollStatus,
    Poll,
    ForwardedFrom,
    AuxData,
    MetadataPart,
    Metadata,
    ButtonSelectionItem,
    ButtonSelection,
    ButtonCalendar,
    ButtonNumberPicker,
    ButtonStringPicker,
    ButtonTextbox,
    ButtonLocation,
    Button,
    KeypadRow,
    Keypad,
    Message,
    Event,
    Update,
    InlineMessage,
    GetUpdatesResult,
)

async def _call(self, method_name: str, *, json_body: Optional[Dict[str, object]]=None) -> object:
    '''"""Rubika client operation ``_call``.

Args:
    method_name: Value accepted by this operation.
    json_body: Value accepted by this operation.

Returns:
    Any: The value returned by the Rubika API or the local helper.

Raises:
    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.
"""'''
    url = f'{self._base_url}/{method_name}'

    async def operation():
        """Executes the operation operation.
        
        Returns:
            The operation result (``Any``).
        """
        return await self._session.request('POST', url, json_body=json_body if json_body is not None else {})
    response = await run_with_retry(operation, self._retry_policy)
    envelope = response.json
    if not isinstance(envelope, dict):
        raise RubikaAPIError(f'{method_name}: non-JSON or malformed response body', error_code='INVALID_RESPONSE', error_message='<no JSON object body>', raw=None)
    if envelope.get('status', '') != 'OK':
        raise error_for_envelope(envelope)
    return envelope.get('data')
