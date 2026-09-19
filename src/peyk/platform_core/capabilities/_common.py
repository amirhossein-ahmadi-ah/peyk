from __future__ import annotations
from typing import Iterable
from . import Support, SupportLevel
_FIELD_REFS = {'telegram.InlineKeyboardButton.url', 'telegram.InlineKeyboardButton.callback_data', 'telegram.InlineKeyboardButton.web_app', 'telegram.InlineKeyboardButton.copy_text', 'telegram.InlineKeyboardButton.style', 'telegram.InlineKeyboardButton.icon_custom_emoji_id', 'telegram.InlineKeyboardButton.pay', 'telegram.InlineKeyboardButton.switch_inline_query', 'telegram.InlineKeyboardButton.login_url', 'telegram.InlineKeyboardButton.text', 'telegram.KeyboardButton.text', 'telegram.KeyboardButton.request_contact', 'telegram.KeyboardButton.request_location', 'telegram.KeyboardButton.request_poll', 'telegram.KeyboardButton.request_users', 'telegram.KeyboardButton.request_chat', 'bale.InlineKeyboardButton.text', 'bale.InlineKeyboardButton.url', 'bale.InlineKeyboardButton.callback_data', 'bale.InlineKeyboardButton.web_app', 'bale.InlineKeyboardButton.copy_text', 'bale.KeyboardButton.text', 'bale.KeyboardButton.request_contact', 'bale.KeyboardButton.request_location', 'rubika.Button.button_text', 'rubika.Button.button_selection', 'rubika.Button.button_calendar', 'rubika.Button.button_number_picker', 'rubika.Button.button_string_picker', 'rubika.Button.button_location', 'rubika.Button.button_textbox', 'rubika.MetadataPart.type'}

def s(level: SupportLevel, *refs: str, note: str='', confidence: str='confirmed', **limits: object) -> Support:
    """Performs the s operation for the platform-core client.

Args:
    level: Value used by this operation.
    note: Value used by this operation.
    confidence: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    evidence = tuple((('doc' if ref == 'docs/decisions.md' else 'type_field' if ref in _FIELD_REFS else 'method', ref) for ref in refs))
    return Support(level, evidence, limits, note, confidence)

def audited_method_refs(names: Iterable[str]) -> tuple[tuple[str, str], ...]:
    """Performs the audited method refs operation for the platform-core client.

Args:
    names: Value used by this operation.

Returns:
    Result produced by the platform-core operation."""
    return tuple((('method', name) for name in names))
