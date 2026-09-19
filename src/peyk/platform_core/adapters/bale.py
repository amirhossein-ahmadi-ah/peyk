"""Bale raw-model -> normalized dispatcher contracts."""
from __future__ import annotations
from dataclasses import replace
from typing import Any, Mapping, Optional, Union
from peyk.platforms.bale import models as bale
from peyk.platform_core.enums import PlatformName, UpdateDelivery
from peyk.types import CallbackQuery, Message
from peyk.types._convert import message_base, user
from peyk.platform_core.contracts import IncomingBotMembershipChange, IncomingCallbackQuery, IncomingChatMemberStatusUpdate, IncomingMessage, IncomingMessageDeleted, IncomingPreCheckoutQuery, PlatformCapabilities
BALE_CAPABILITIES = __import__('peyk.platform_core.capabilities.legacy', fromlist=['legacy_capabilities']).legacy_capabilities('bale')

def _id(value: object) -> object:
    if value is None:
        return None
    if hasattr(value, 'id'):
        return value.id
    if hasattr(value, 'message_id'):
        return value.message_id
    if hasattr(value, 'chat_id'):
        return value.chat_id
    return value

def _first_media(raw: bale.Message) -> object:
    for name in ('animation', 'audio', 'document', 'photo', 'sticker', 'video', 'voice', 'contact', 'location'):
        value = getattr(raw, name, None)
        if value is not None:
            return value
    return None

def normalize_message(raw: bale.Message) -> Message:
    """Convert a Bale message to the neutral bound-action type."""
    return message_base(raw, bot=None)

def normalize_callback(raw: bale.CallbackQuery) -> CallbackQuery:
    """Convert a Bale callback query to the neutral callback type."""
    normalized_message = message_base(raw.message, bot=None) if raw.message is not None else None
    return CallbackQuery(id=raw.id, from_user_id=getattr(raw.from_, 'id', None), chat_id=normalized_message.chat_id if normalized_message else None, message_id=normalized_message.message_id if normalized_message else None, data=raw.data, raw=raw, from_user=user(raw.from_) if raw.from_ is not None else None, message=normalized_message, bot=None)

def normalize_chat_member(raw: object) -> Optional[IncomingChatMemberStatusUpdate]:
    """Performs the normalize chat member operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Bale has no confirmed incoming rich member-status update kind.\n    \n    Args:\n        raw: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[IncomingChatMemberStatusUpdate]``).\n    '
    return None

def normalize_pre_checkout_query(raw: bale.PreCheckoutQuery) -> IncomingPreCheckoutQuery:
    """Performs the normalize pre checkout query operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_pre_checkout_query operation.\n\nArgs:\n    raw: bale.PreCheckoutQuery.\n\nReturns:\n    IncomingPreCheckoutQuery.\n\nRaises:\n    \n'
    return IncomingPreCheckoutQuery(id=raw.id, from_user_id=_id(raw.from_), currency=raw.currency, total_amount=raw.total_amount, invoice_payload=raw.invoice_payload, raw=raw)

def normalize_update(raw: bale.Update) -> Union[Message, CallbackQuery, IncomingPreCheckoutQuery, bale.Update]:
    """Performs the normalize update operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_update operation.\n\nArgs:\n    raw: bale.Update.\n\nReturns:\n    Union[IncomingMessage, IncomingCallbackQuery, IncomingPreCheckoutQuery, bale.Update].\n\nRaises:\n    \n\nExample:\n    >>> event = normalize_update(raw_update)\n'
    if raw.message is not None:
        return replace(normalize_message(raw.message), update_kind='message')
    if raw.edited_message is not None:
        return replace(normalize_message(raw.edited_message), update_kind='edited_message', is_edited=True)
    if raw.callback_query is not None:
        return normalize_callback(raw.callback_query)
    if raw.pre_checkout_query is not None:
        return normalize_pre_checkout_query(raw.pre_checkout_query)
    return raw
