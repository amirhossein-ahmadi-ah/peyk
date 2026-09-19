from __future__ import annotations
from peyk.keyboard.ir import *
from peyk.keyboard.render.common import resolve_inline
from peyk.platform_core.capabilities import CapabilitySet, Feature
from peyk.bot.policy import UnsupportedPolicy, StyleFallback
KeyboardPolicy = UnsupportedPolicy | tuple[UnsupportedPolicy, StyleFallback]
from peyk.platforms.bale.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo, CopyTextButton

def inline_keyboard(ir: InlineKeyboard, capabilities: CapabilitySet, policy: KeyboardPolicy) -> InlineKeyboardMarkup:
    """Performs the inline keyboard operation for the keyboard client.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    rows = []
    for row in ir.inline_keyboard:
        out = []
        for raw in row:
            b = resolve_inline(raw, capabilities, policy)
            out.append(InlineKeyboardButton(text=b.text, url=b.url, callback_data=b.packed_callback_data(), web_app=(b.web_app if isinstance(b.web_app, WebAppInfo) else WebAppInfo(url=b.web_app_url)) if b.web_app or b.web_app_url else None, copy_text=(b.copy_text if isinstance(b.copy_text, CopyTextButton) else CopyTextButton(text=str(b.copy_text))) if b.copy_text else None))
        rows.append(out)
    return InlineKeyboardMarkup(inline_keyboard=rows)

def reply_keyboard(ir: ReplyKeyboard, capabilities: CapabilitySet, policy: KeyboardPolicy) -> ReplyKeyboardMarkup:
    """Performs the reply keyboard operation for the keyboard client.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    rows = []
    for row in ir.keyboard:
        out = []
        for b in row:
            if not b.text:
                raise ValueError('button text cannot be empty')
            if b.request_contact and (not capabilities.supports(Feature.BUTTON_REQUEST_CONTACT)):
                raise ValueError('unsupported request_contact')
            if b.request_location and (not capabilities.supports(Feature.BUTTON_REQUEST_LOCATION)):
                raise ValueError('unsupported request_location')
            if b.web_app_url and (not capabilities.supports(Feature.BUTTON_WEB_APP)):
                raise ValueError('unsupported web_app')
            out.append(KeyboardButton(text=b.text, request_contact=b.request_contact, request_location=b.request_location, web_app=(b.web_app if isinstance(b.web_app, WebAppInfo) else WebAppInfo(url=b.web_app_url)) if b.web_app or b.web_app_url else None))
        rows.append(out)
    return ReplyKeyboardMarkup(keyboard=rows)

def remove_keyboard(ir: KeyboardRemove, capabilities: CapabilitySet, policy: KeyboardPolicy) -> ReplyKeyboardRemove:
    """Removes keyboard through the keyboard API.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    return ReplyKeyboardRemove(remove_keyboard=True)

def force_reply(ir: ForceReply, capabilities: CapabilitySet, policy: KeyboardPolicy) -> object:
    """Performs the force reply operation for the keyboard client.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    from peyk.platform_core.errors import UnsupportedFeatureError
    support = capabilities.get(Feature.FORCE_REPLY)
    raise UnsupportedFeatureError(Feature.FORCE_REPLY, capabilities.platform, support)
