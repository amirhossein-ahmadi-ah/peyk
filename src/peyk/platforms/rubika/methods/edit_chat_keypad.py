from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def edit_chat_keypad(self, chat_id: str, chat_keypad: Union[Keypad, Dict[str, object], None]=None, *, chat_keypad_type: str=ChatKeypadTypeEnum.NEW) -> bool:
    """Edits chat keypad through the Rubika API.

Args:
    chat_id: Identifier of the target chat.
    chat_keypad: Value used by this operation.
    chat_keypad_type: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    'Add, update, or remove a chat keypad.\n    \n            ``chat_keypad_type``:\n            - ``"New"`` (default): set/replace the keypad. Requires ``chat_keypad``.\n            - ``"Remove"``: clear the keypad. ``chat_keypad`` is ignored.\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        chat_keypad: Value of the declared parameter type.\n        chat_keypad_type: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    '
    payload: Dict[str, object] = {'chat_id': chat_id, 'chat_keypad_type': chat_keypad_type}
    kp = self._keypad_to_dict(chat_keypad)
    if kp is not None:
        payload['chat_keypad'] = kp
    await self._call('editChatKeypad', json_body=payload)
    return True
