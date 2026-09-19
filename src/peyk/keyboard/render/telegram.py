from __future__ import annotations
from peyk.keyboard.ir import *
from peyk.keyboard.render.common import resolve_inline
from peyk.platform_core.capabilities import CapabilitySet, Feature
from peyk.bot.policy import UnsupportedPolicy, StyleFallback
KeyboardPolicy = UnsupportedPolicy | tuple[UnsupportedPolicy, StyleFallback]
from peyk.platforms.telegram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, WebAppInfo, LoginUrl, CopyTextButton

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
            out.append(InlineKeyboardButton(text=b.text, callback_data=b.packed_callback_data(), url=b.url, web_app=(b.web_app if isinstance(b.web_app, WebAppInfo) else WebAppInfo(url=b.web_app_url)) if b.web_app or b.web_app_url else None, copy_text=(b.copy_text if isinstance(b.copy_text, CopyTextButton) else CopyTextButton(text=str(b.copy_text))) if b.copy_text else None, login_url=(b.login_url if isinstance(b.login_url, LoginUrl) else LoginUrl(url=str(b.login_url))) if b.login_url else None, switch_inline_query=b.switch_inline_query, switch_inline_query_current_chat=b.switch_inline_query_current_chat, switch_inline_query_chosen_chat=b.switch_inline_query_chosen_chat, pay=b.pay, style=b.style.value if b.style else None, icon_custom_emoji_id=b.icon_custom_emoji_id))
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
            vals = {'request_contact': b.request_contact, 'request_location': b.request_location, 'request_poll': b.request_poll, 'request_users': b.request_users, 'request_chat': b.request_chat, 'web_app': WebAppInfo(url=b.web_app_url) if b.web_app_url else None, 'style': b.style.value if b.style and capabilities.supports(Feature.BUTTON_COLOR_STYLE) else None, 'icon_custom_emoji_id': b.icon_custom_emoji_id if b.icon_custom_emoji_id and capabilities.supports(Feature.BUTTON_ICON_EMOJI) else None}
            for f, v in [(Feature.BUTTON_REQUEST_CONTACT, b.request_contact), (Feature.BUTTON_REQUEST_LOCATION, b.request_location), (Feature.BUTTON_REQUEST_POLL, b.request_poll), (Feature.BUTTON_REQUEST_USERS, b.request_users), (Feature.BUTTON_REQUEST_CHAT, b.request_chat), (Feature.BUTTON_WEB_APP, b.web_app_url)]:
                if v is not None and (not capabilities.supports(f)):
                    if b.fallback:
                        b = b.fallback
                        break
                    raise ValueError(f'unsupported keyboard feature: {f.value}')
            out.append(KeyboardButton(text=b.text, **{k: v for k, v in vals.items() if v is not None}))
        rows.append(out)
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=ir.resize_keyboard, one_time_keyboard=ir.one_time_keyboard, input_field_placeholder=ir.input_field_placeholder, is_persistent=ir.is_persistent, selective=ir.selective)

def remove_keyboard(ir: KeyboardRemove, capabilities: CapabilitySet, policy: KeyboardPolicy) -> ReplyKeyboardRemove:
    """Removes keyboard through the keyboard API.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    return ReplyKeyboardRemove(remove_keyboard=True, selective=ir.selective)

def force_reply(ir: ForceReply, capabilities: CapabilitySet, policy: KeyboardPolicy) -> ForceReply:
    """Performs the force reply operation for the keyboard client.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    return ForceReply(force_reply=True, input_field_placeholder=ir.input_field_placeholder, selective=ir.selective)
