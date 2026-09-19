"""Rubika raw-model -> normalized dispatcher contracts."""
from __future__ import annotations
from dataclasses import replace
from typing import Any, Optional, Union
from peyk.platforms.rubika import models as rb
from peyk.platforms.rubika.types import InlineMessage
from peyk.platform_core.enums import PlatformName, UpdateDelivery
from peyk.types import CallbackQuery, Message
from peyk.types._convert import chat, message_base, user
from peyk.platform_core.contracts import IncomingBotMembershipChange, IncomingCallbackQuery, IncomingChatMemberStatusUpdate, IncomingMessage, IncomingMessageDeleted, PlatformCapabilities
RUBIKA_CAPABILITIES = __import__('peyk.platform_core.capabilities.legacy', fromlist=['legacy_capabilities']).legacy_capabilities('rubika')

def normalize_message(raw: rb.Message, *, chat_id: Optional[str]=None) -> Message:
    """Convert a Rubika message to a neutral message, using Update.chat_id."""
    normalized_chat = None
    if chat_id is not None:
        from peyk.types import Chat, ChatType
        normalized_chat = Chat(id=chat_id, type=ChatType.UNKNOWN)
    return message_base(raw, bot=None, chat_override=normalized_chat)

def normalize_callback(raw: rb.InlineMessage) -> CallbackQuery:
    """Convert a Rubika inline-message callback to the neutral callback type."""
    msg = Message(message_id=raw.message_id, chat_id=raw.chat_id, chat_type=None, sender_id=raw.sender_id, raw=None, from_user=user(type('Sender', (), {'id': raw.sender_id, 'is_bot': False, 'first_name': ''})()), chat=None, bot=None)
    return CallbackQuery(id=None, from_user_id=raw.sender_id, chat_id=raw.chat_id, message_id=raw.message_id, data=raw.aux_data.button_id if raw.aux_data is not None else None, raw=raw, from_user=msg.from_user, message=msg, bot=None)

def normalize_inline_message(raw: InlineMessage) -> CallbackQuery:
    """Normalize a Rubika ``receiveInlineMessage`` callback payload."""
    return normalize_callback(raw)

def normalize_chat_member(raw: object) -> Optional[IncomingChatMemberStatusUpdate]:
    """Performs the normalize chat member operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Rubika has no confirmed rich member-status update contract.\n    \n    Args:\n        raw: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[IncomingChatMemberStatusUpdate]``).\n    '
    return None

def normalize_bot_membership(raw: rb.Event, *, chat_id: Optional[str]=None) -> Optional[IncomingBotMembershipChange]:
    """Performs the normalize bot membership operation for the platform-core client.

Args:
    raw: Value used by this operation.
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_bot_membership operation.\n\nArgs:\n    raw: rb.Event.\n    chat_id: Optional[str].\n\nReturns:\n    Optional[IncomingBotMembershipChange].\n\nRaises:\n    \n'
    if raw.type == rb.EventTypeEnum.BOT_JOINED:
        return IncomingBotMembershipChange(chat_id=chat_id, added=True, raw=raw)
    if raw.type == rb.EventTypeEnum.BOT_REMOVED:
        return IncomingBotMembershipChange(chat_id=chat_id, added=False, raw=raw)
    return None

def normalize_deleted(raw: rb.Update) -> IncomingMessageDeleted:
    """Performs the normalize deleted operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_deleted operation.\n\nArgs:\n    raw: rb.Update.\n\nReturns:\n    IncomingMessageDeleted.\n\nRaises:\n    \n'
    return IncomingMessageDeleted(chat_id=raw.chat_id, message_id=raw.removed_message_id, raw=raw)

def normalize_update(raw: rb.Update) -> Union[Message, IncomingMessageDeleted, IncomingBotMembershipChange, rb.Update]:
    """Performs the normalize update operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_update operation.\n\nArgs:\n    raw: rb.Update.\n\nReturns:\n    Union[IncomingMessage, IncomingMessageDeleted, IncomingBotMembershipChange, rb.Update].\n\nRaises:\n    \n\nExample:\n    >>> event = normalize_update(raw_update)\n'
    if raw.type == rb.UpdateTypeEnum.NEW_MESSAGE and raw.new_message is not None:
        return replace(normalize_message(raw.new_message, chat_id=raw.chat_id), update_kind='message')
    if raw.type == rb.UpdateTypeEnum.UPDATED_MESSAGE and raw.updated_message is not None:
        return replace(normalize_message(raw.updated_message, chat_id=raw.chat_id), update_kind='edited_message', is_edited=True)
    if raw.type == rb.UpdateTypeEnum.REMOVED_MESSAGE:
        return normalize_deleted(raw)
    if raw.type == rb.UpdateTypeEnum.EVENT_DATA and raw.event_data is not None:
        membership = normalize_bot_membership(raw.event_data, chat_id=raw.chat_id)
        return membership if membership is not None else raw
    return raw
