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

@staticmethod
def _commands_to_list(commands: List[Union[BotCommand, Dict[str, object]]]) -> List[Dict[str, object]]:
    '''"""Rubika client operation ``_commands_to_list``.

Args:
    commands: Value accepted by this operation.

Returns:
    List[Dict[str, object]]: The value returned by the Rubika API or the local helper.

Raises:
    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.
"""'''
    return [c.to_dict() if isinstance(c, BotCommand) else dict(c) for c in commands]
