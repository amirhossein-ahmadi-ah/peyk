"""Telegram raw-model -> normalized dispatcher contracts."""
from __future__ import annotations
from dataclasses import replace
from typing import Any, Mapping, Optional, Union
from peyk.platforms.telegram import models as tg
from peyk.platform_core.enums import ParseMode, PlatformName, UpdateDelivery
from peyk.types import CallbackQuery, Message
from peyk.types._convert import message_base, user
from peyk.platform_core.contracts import IncomingBotMembershipChange, IncomingCallbackQuery, IncomingChatMemberStatusUpdate, IncomingMessage, IncomingMessageDeleted, IncomingPreCheckoutQuery, IncomingShippingQuery, PlatformCapabilities
TELEGRAM_CAPABILITIES = __import__('peyk.platform_core.capabilities.legacy', fromlist=['legacy_capabilities']).legacy_capabilities('telegram')

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

def _first_media(raw: tg.Message) -> object:
    for name in ('animation', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'live_photo', 'contact', 'dice', 'game', 'poll', 'venue', 'location'):
        value = getattr(raw, name, None)
        if value is not None:
            return value
    return None

def normalize_message(raw: tg.Message) -> Message:
    """Convert a Telegram message to the neutral bound-action type."""
    return message_base(raw, bot=None)

def normalize_callback(raw: tg.CallbackQuery) -> CallbackQuery:
    """Convert a Telegram callback query to the neutral callback type."""
    message = getattr(raw, 'message', None)
    normalized_message = message_base(message, bot=None) if message is not None else None
    return CallbackQuery(id=raw.id, from_user_id=getattr(getattr(raw, 'from_', None), 'id', None), chat_id=normalized_message.chat_id if normalized_message else None, message_id=normalized_message.message_id if normalized_message else None, inline_message_id=getattr(raw, 'inline_message_id', None), data=getattr(raw, 'data', None), raw=raw, from_user=user(raw.from_) if raw.from_ is not None else None, message=normalized_message, bot=None)

def normalize_chat_member(raw: tg.ChatMemberUpdated) -> IncomingChatMemberStatusUpdate:
    """Performs the normalize chat member operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_chat_member operation.\n\nArgs:\n    raw: tg.ChatMemberUpdated.\n\nReturns:\n    IncomingChatMemberStatusUpdate.\n\nRaises:\n    \n'
    old = getattr(raw, 'old_chat_member', None)
    new = getattr(raw, 'new_chat_member', None)
    old_user = getattr(old, 'user', None)
    new_user = getattr(new, 'user', None)
    target = _id(new_user) if new_user is not None else _id(old_user)
    return IncomingChatMemberStatusUpdate(chat_id=_id(getattr(raw, 'chat', None)), actor_id=_id(getattr(raw, 'from_', None)), target_user_id=target, old_status=getattr(old, 'status', None), new_status=getattr(new, 'status', None), old_is_member=getattr(old, 'is_member', None), new_is_member=getattr(new, 'is_member', None), date=getattr(raw, 'date', None), raw=raw)

def normalize_pre_checkout_query(raw: object) -> IncomingPreCheckoutQuery:
    """Performs the normalize pre checkout query operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_pre_checkout_query operation.\n\nArgs:\n    raw: object.\n\nReturns:\n    IncomingPreCheckoutQuery.\n\nRaises:\n    \n'
    return IncomingPreCheckoutQuery(id=getattr(raw, 'id', None) if not isinstance(raw, Mapping) else raw.get('id'), from_user_id=_id(getattr(raw, 'from_', None)) if not isinstance(raw, Mapping) else _id(raw.get('from')), currency=getattr(raw, 'currency', None) if not isinstance(raw, Mapping) else raw.get('currency'), total_amount=getattr(raw, 'total_amount', None) if not isinstance(raw, Mapping) else raw.get('total_amount'), invoice_payload=getattr(raw, 'invoice_payload', None) if not isinstance(raw, Mapping) else raw.get('invoice_payload'), shipping_option_id=getattr(raw, 'shipping_option_id', None) if not isinstance(raw, Mapping) else raw.get('shipping_option_id'), order_info=getattr(raw, 'order_info', None) if not isinstance(raw, Mapping) else raw.get('order_info'), raw=raw)

def normalize_shipping_query(raw: object) -> IncomingShippingQuery:
    """Performs the normalize shipping query operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_shipping_query operation.\n\nArgs:\n    raw: object.\n\nReturns:\n    IncomingShippingQuery.\n\nRaises:\n    \n'
    return IncomingShippingQuery(id=getattr(raw, 'id', None) if not isinstance(raw, Mapping) else raw.get('id'), from_user_id=_id(getattr(raw, 'from_', None)) if not isinstance(raw, Mapping) else _id(raw.get('from')), invoice_payload=getattr(raw, 'invoice_payload', None) if not isinstance(raw, Mapping) else raw.get('invoice_payload'), shipping_address=getattr(raw, 'shipping_address', None) if not isinstance(raw, Mapping) else raw.get('shipping_address'), raw=raw)

def normalize_bot_membership_from_message(raw: tg.Message) -> Optional[IncomingBotMembershipChange]:
    """Performs the normalize bot membership from message operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Performs the normalize_bot_membership_from_message operation.\n\nArgs:\n    raw: tg.Message.\n\nReturns:\n    Optional[IncomingBotMembershipChange].\n\nRaises:\n    \n'
    return None

def normalize_update(raw: tg.Update) -> Union[Message, CallbackQuery, IncomingChatMemberStatusUpdate, IncomingPreCheckoutQuery, IncomingShippingQuery, tg.Update]:
    """Performs the normalize update operation for the platform-core client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    'Normalize every Telegram update kind that has a D0 contract.\n    \n        Telegram-only update kinds without a shared contract are returned through\n        the raw escape hatch by returning the original platform object unchanged.\n        \n    \n    Args:\n        raw: Value of the declared parameter type.\n    \n    \n    Returns:\n        The normalized contract, or the original ``tg.Update`` for a\n        Telegram-only update kind.\n    '
    for field in ('message', 'edited_message', 'channel_post', 'edited_channel_post', 'business_message', 'edited_business_message', 'guest_message'):
        value = getattr(raw, field, None)
        if value is not None:
            normalized = normalize_message(value)
            kind = {'message': 'message', 'edited_message': 'edited_message', 'channel_post': 'channel_post', 'edited_channel_post': 'edited_channel_post', 'business_message': 'message', 'edited_business_message': 'edited_message'}[field]
            normalized = replace(normalized, update_kind=kind)
            if field == 'edited_message' or field == 'edited_channel_post' or field == 'edited_business_message':
                normalized = replace(normalized, is_edited=True)
            return normalized
    if raw.callback_query is not None:
        return normalize_callback(raw.callback_query)
    if raw.my_chat_member is not None:
        return normalize_chat_member(raw.my_chat_member)
    if raw.chat_member is not None:
        return normalize_chat_member(raw.chat_member)
    if raw.pre_checkout_query is not None:
        return normalize_pre_checkout_query(raw.pre_checkout_query)
    if raw.shipping_query is not None:
        return normalize_shipping_query(raw.shipping_query)
    return raw
