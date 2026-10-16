"""Soroush Plus (Splus) capability declarations.

Derived from the official Splus bot documentation (https://splus.ir/p/documents,
scraped and audited).  Features the docs mark 'coming soon' or do not mention
are ``NONE``; anything not covered stays ``UNKNOWN`` and is refused by
:class:`peyk.Bot`.  ``docs/capabilities_todo.md`` lists the UNKNOWN rows.
"""
from __future__ import annotations

from . import Feature, Support, SupportLevel
from ._common import s


def _base() -> dict[Feature, Support]:
    return {f: Support(SupportLevel.UNKNOWN, confidence="low", note="Not confirmed by the Splus client libraries; needs a live probe.") for f in Feature}


CAPABILITIES = _base()

_NOTE = "Confirmed by the official Splus bot documentation."
for feature, method in {
    Feature.TEXT: "SplusClient.send_message", Feature.PHOTO: "SplusClient.send_photo",
    Feature.VIDEO: "SplusClient.send_video", Feature.AUDIO: "SplusClient.send_audio",
    Feature.VOICE: "SplusClient.send_voice", Feature.DOCUMENT: "SplusClient.send_document",
    Feature.ANIMATION: "SplusClient.send_animation", Feature.STICKER: "SplusClient.send_sticker",
    Feature.CONTACT: "SplusClient.send_contact", Feature.LOCATION: "SplusClient.send_location",
    Feature.MEDIA_GROUP: "SplusClient.send_media_group",
    Feature.COPY: "SplusClient.copy_message", Feature.FORWARD: "SplusClient.forward_message",
    Feature.EDIT_TEXT: "SplusClient.edit_message_text", Feature.EDIT_CAPTION: "SplusClient.edit_message_caption",
    Feature.EDIT_MEDIA: "SplusClient.edit_message_media", Feature.EDIT_MARKUP: "SplusClient.edit_message_reply_markup",
    Feature.DELETE: "TelegramLikeClient.delete_message", Feature.REPLY_TO: "SplusClient.send_message",
    Feature.GET_FILE: "TelegramLikeClient.get_file",
    Feature.UPLOAD_BYTES: "TelegramLikeClient._as_file_payload", Feature.POLLING: "SplusClient.get_updates",
    Feature.WEBHOOK: "SplusClient.set_webhook", Feature.UPDATE_OFFSET: "SplusClient.get_updates",
    Feature.ALLOWED_UPDATES: "SplusClient.get_updates", Feature.LONG_POLL_TIMEOUT: "SplusClient.get_updates",
    Feature.BOT_COMMANDS: "SplusClient.set_my_commands",
}.items():
    CAPABILITIES[feature] = s(SupportLevel.FULL, method, note=_NOTE if feature is Feature.TEXT else "")

CAPABILITIES[Feature.LINK_PREVIEW_CONTROL] = s(SupportLevel.FULL, "SplusClient.send_message", note="Sent as the classic disable_web_page_preview field (translated from link_preview_options).")
CAPABILITIES[Feature.ENTITIES_FORMATTING] = s(SupportLevel.FULL, "SplusClient.send_message", note="Official docs list MarkdownV2, HTML and Markdown formatting options.", parse_modes=("MarkdownV2", "HTML", "Markdown"))
CAPABILITIES[Feature.CALLBACK_ANSWER] = s(SupportLevel.FULL, "SplusClient.answer_callback_query")
CAPABILITIES[Feature.CALLBACK_ALERT_TOAST] = s(SupportLevel.FULL, "SplusClient.answer_callback_query", note="answer_callback_query exposes show_alert.")
CAPABILITIES[Feature.CALLBACK_DATA_LIMIT] = s(SupportLevel.FULL, "telegram.InlineKeyboardButton.callback_data", note="Official docs: callback_data is 1-64 bytes.", callback_data_max_bytes=64)
CAPABILITIES[Feature.INLINE_KEYBOARD] = s(SupportLevel.FULL, "telegram.InlineKeyboardButton.text")
CAPABILITIES[Feature.REPLY_KEYBOARD] = s(SupportLevel.FULL, "telegram.KeyboardButton.text")
CAPABILITIES[Feature.REMOVE_REPLY] = s(SupportLevel.FULL, "telegram.KeyboardButton.text")
for f, field in {Feature.BUTTON_URL: "url", Feature.BUTTON_CALLBACK: "callback_data"}.items():
    CAPABILITIES[f] = s(SupportLevel.FULL, f"telegram.InlineKeyboardButton.{field}")
CAPABILITIES[Feature.BUTTON_REQUEST_CONTACT] = s(SupportLevel.FULL, "telegram.KeyboardButton.request_contact")
CAPABILITIES[Feature.BUTTON_REQUEST_LOCATION] = s(SupportLevel.FULL, "telegram.KeyboardButton.request_location")

# Positively absent from the Splus models (Update has only message/edited_message/callback_query).
_ABSENT = {
    Feature.DICE: "Official docs have no sendDice method and no dice field on Message.",
    Feature.CHAT_ACTIONS: "sendChatAction is marked 'coming soon' in the official docs.",
    Feature.PIN: "pinChatMessage is marked 'coming soon' in the official docs.",
    Feature.UNPIN: "unpinChatMessage is marked 'coming soon' in the official docs.",
    Feature.FORCE_REPLY: "ForceReply is marked 'coming soon' in the official docs.",
    Feature.BUTTON_WEB_APP: "InlineKeyboardButton documents only text, url and callback_data.",
    Feature.BUTTON_COPY_TEXT: "InlineKeyboardButton documents only text, url and callback_data.",
    Feature.POLL: "No send_poll method and no poll field on the Splus Message model.",
    Feature.VENUE: "No send_venue method in the Splus client libraries.",
    Feature.PAYMENTS: "No invoice/payment methods in the Splus client libraries.",
    Feature.INLINE_MODE: "No inline-query update or answer method in the Splus client libraries.",
    Feature.BULK_DELETE: "Only single delete_message is exposed.",
    Feature.WEBHOOK_SECRET_HEADER: "set_webhook has no secret_token parameter; peyk uses the framework path secret instead.",
    Feature.MEMBER_STATUS_UPDATES: "Splus Update carries only message, edited_message and callback_query.",
}
for f, note in _ABSENT.items():
    CAPABILITIES[f] = s(SupportLevel.NONE, "docs/decisions.md", note=note, confidence="confirmed")
for f in (Feature.TELEGRAM_GAMES, Feature.TELEGRAM_PASSPORT, Feature.TELEGRAM_BUSINESS, Feature.TELEGRAM_STORIES, Feature.TELEGRAM_GIFTS, Feature.TELEGRAM_STARS):
    CAPABILITIES[f] = s(SupportLevel.NONE, "docs/decisions.md", note="Telegram-only feature; not part of the Splus bot API.", confidence="inferred")

PLATFORM_SPECIFIC_METHODS: tuple[str, ...] = (
    # Bound client methods that have no neutral Feature row (or whose Feature is
    # still UNKNOWN), plus the keyboard-button fields this platform shares with Telegram.
    'close', 'delete_chat_photo', 'delete_my_commands', 'delete_webhook', 'get_chat', 'get_chat_member', 'get_me', 'get_my_commands', 'get_webhook_info', 'leave_chat', 'log_out', 'send_video_note', 'set_chat_title', 'unban_chat_member', 'unpin_all_chat_messages',
    'field:InlineKeyboardButton.callback_data', 'field:InlineKeyboardButton.callback_game', 'field:InlineKeyboardButton.copy_text', 'field:InlineKeyboardButton.disabled', 'field:InlineKeyboardButton.icon_custom_emoji_id', 'field:InlineKeyboardButton.login_url', 'field:InlineKeyboardButton.pay', 'field:InlineKeyboardButton.style', 'field:InlineKeyboardButton.switch_inline_query', 'field:InlineKeyboardButton.switch_inline_query_chosen_chat', 'field:InlineKeyboardButton.switch_inline_query_current_chat', 'field:InlineKeyboardButton.text', 'field:InlineKeyboardButton.url', 'field:InlineKeyboardButton.web_app', 'field:KeyboardButton.icon_custom_emoji_id', 'field:KeyboardButton.request_chat', 'field:KeyboardButton.request_contact', 'field:KeyboardButton.request_location', 'field:KeyboardButton.request_managed_bot', 'field:KeyboardButton.request_poll', 'field:KeyboardButton.request_users', 'field:KeyboardButton.style', 'field:KeyboardButton.text', 'field:KeyboardButton.web_app',
)
