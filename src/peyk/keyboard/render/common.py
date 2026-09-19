from __future__ import annotations
from dataclasses import replace
from peyk.keyboard.ir import *
from peyk.platform_core.capabilities import CapabilitySet, Feature, SupportLevel
from peyk.platform_core.errors import UnsupportedFeatureError
from peyk.bot.policy import UnsupportedPolicy, StyleFallback
KeyboardPolicy = UnsupportedPolicy | tuple[UnsupportedPolicy, StyleFallback]

def callback_bytes(value: str | None, capabilities: CapabilitySet) -> None:
    """Performs the callback bytes operation for the keyboard client.

Args:
    value: Value used by this operation.
    capabilities: Value used by this operation."""
    if value is None:
        return
    limit = capabilities.get(Feature.CALLBACK_DATA_LIMIT).limit('callback_data_max_bytes')
    if isinstance(limit, int):
        size = len(value.encode('utf-8'))
        if size < 1 or size > limit:
            raise ValueError(f'callback_data must be 1-{limit} UTF-8 bytes; got {size}')

def _policy_values(policy: KeyboardPolicy) -> tuple[UnsupportedPolicy, StyleFallback]:
    if isinstance(policy, tuple):
        return (policy[0], policy[1])
    return (policy if isinstance(policy, UnsupportedPolicy) else UnsupportedPolicy.DEFAULT, StyleFallback.NONE)

def _support(cap: CapabilitySet, feature: Feature, policy: KeyboardPolicy, *, cosmetic: bool, fallback: object | None) -> bool:
    unsupported_policy, _ = _policy_values(policy)
    s = cap.get(feature)
    if s.level not in {SupportLevel.NONE, SupportLevel.UNKNOWN}:
        return True
    if fallback is not None:
        return False
    if cosmetic and unsupported_policy is not UnsupportedPolicy.RAISE:
        return False
    raise UnsupportedFeatureError(feature, cap.platform, s)

def resolve_inline(b: InlineButton, cap: CapabilitySet, policy: UnsupportedPolicy) -> InlineButton:
    """Performs the resolve inline operation for the keyboard client.

Args:
    b: Value used by this operation.
    cap: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    if not b.text:
        raise ValueError('button text cannot be empty')
    value = b.packed_callback_data()
    callback_bytes(value, cap)
    checks = [(Feature.BUTTON_URL, b.url), (Feature.BUTTON_CALLBACK, value), (Feature.BUTTON_WEB_APP, b.web_app_url or b.web_app), (Feature.BUTTON_COPY_TEXT, b.copy_text), (Feature.BUTTON_LOGIN_URL, b.login_url), (Feature.BUTTON_SWITCH_INLINE, b.switch_inline_query or b.switch_inline_query_current_chat or b.switch_inline_query_chosen_chat), (Feature.BUTTON_PAY, b.pay)]
    for f, v in checks:
        if v is not None and (not _support(cap, f, policy, cosmetic=False, fallback=b.fallback)):
            return resolve_inline(b.fallback, cap, policy) if b.fallback else b
    unsupported_policy, style_fallback = _policy_values(policy)
    native_style = b.style and _support(cap, Feature.BUTTON_COLOR_STYLE, policy, cosmetic=True, fallback=None)
    style = b.style if native_style else None
    text = b.text
    if b.style and (not native_style) and (style_fallback is StyleFallback.EMOJI):
        text = {'primary': '🔵', 'success': '🟢', 'danger': '🔴'}[b.style.value] + text
    icon = b.icon_custom_emoji_id if b.icon_custom_emoji_id and _support(cap, Feature.BUTTON_ICON_EMOJI, policy, cosmetic=True, fallback=None) else None
    return replace(b, text=text, callback_data=value, style=style, icon_custom_emoji_id=icon)
