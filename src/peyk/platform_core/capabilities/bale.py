"""Bale capability declarations derived from the audited client/models."""
from __future__ import annotations
from . import Feature, Support, SupportLevel
from ._common import s

def _base() -> dict[Feature, Support]:
    return {f: Support(SupportLevel.UNKNOWN, confidence="low", note="Not independently established by the Phase 1 audit.") for f in Feature}
CAPABILITIES = _base()
for feature, method in {
    Feature.TEXT:"BaleClient.send_message", Feature.PHOTO:"BaleClient.send_photo", Feature.VIDEO:"BaleClient.send_video",
    Feature.AUDIO:"BaleClient.send_audio", Feature.VOICE:"BaleClient.send_voice", Feature.DOCUMENT:"BaleClient.send_document",
    Feature.ANIMATION:"BaleClient.send_animation", Feature.CONTACT:"BaleClient.send_contact", Feature.LOCATION:"BaleClient.send_location",
    Feature.MEDIA_GROUP:"BaleClient.send_media_group", Feature.COPY:"BaleClient.copy_message", Feature.FORWARD:"BaleClient.forward_message",
    Feature.EDIT_TEXT:"BaleClient.edit_message_text", Feature.EDIT_CAPTION:"BaleClient.edit_message_caption", Feature.EDIT_MARKUP:"BaleClient.edit_message_reply_markup",
    Feature.DELETE:"TelegramLikeClient.delete_message", Feature.REPLY_TO:"BaleClient.send_message", Feature.CHAT_ACTIONS:"BaleClient.send_chat_action",
    Feature.PAYMENTS:"BaleClient.send_invoice", Feature.GET_FILE:"TelegramLikeClient.get_file", Feature.POLLING:"BaleClient.get_updates",
    Feature.WEBHOOK:"BaleClient.set_webhook", Feature.BAN:"BaleClient.ban_chat_member", Feature.UNBAN:"TelegramLikeClient.unban_chat_member",
    Feature.PROMOTE:"BaleClient.promote_chat_member", Feature.PIN:"BaleClient.pin_chat_message", Feature.UNPIN:"BaleClient.unpin_chat_message",
    Feature.INVITE_LINKS:"BaleClient.create_chat_invite_link", Feature.MEMBER_COUNT:"BaleClient.get_chat_members_count", Feature.ADMINISTRATORS:"BaleClient.get_chat_administrators",
    Feature.TITLE:"TelegramLikeClient.set_chat_title", Feature.DESCRIPTION:"BaleClient.set_chat_description", Feature.CHAT_PHOTO:"BaleClient.set_chat_photo",
    Feature.LEAVE:"TelegramLikeClient.leave_chat", Feature.UPLOAD_BYTES:"TelegramLikeClient._as_file_payload",
}.items(): CAPABILITIES[feature] = s(SupportLevel.FULL, method)
CAPABILITIES[Feature.POLL] = s(SupportLevel.NONE, "docs/decisions.md", note="No send_poll method or poll model is present in the audited Bale client/model set.", confidence="inferred")
CAPABILITIES[Feature.DICE] = s(SupportLevel.NONE, "docs/decisions.md", note="No send_dice method or dice model is present in the audited Bale client/model set.", confidence="inferred")
CAPABILITIES[Feature.VENUE] = s(SupportLevel.NONE, "docs/decisions.md", note="No send_venue method is present in the audited Bale client.", confidence="inferred")
CAPABILITIES[Feature.REACTIONS] = s(SupportLevel.UNKNOWN, "docs/decisions.md", note="No confirmed Bale reaction contract in the audited project.", confidence="low")
CAPABILITIES[Feature.LINK_PREVIEW_CONTROL] = s(SupportLevel.UNKNOWN, "docs/decisions.md", note="Bale parse/formatting and link-preview behavior is not confirmed.", confidence="low")
CAPABILITIES[Feature.PROTECT_CONTENT] = s(SupportLevel.UNKNOWN, "docs/decisions.md", note="Not established by the audited Bale method signatures.", confidence="low")
CAPABILITIES[Feature.ENTITIES_FORMATTING] = s(SupportLevel.PARTIAL, "docs/decisions.md", note="D5 confirms Bale native formatting syntax; no Telegram-style parse_mode is advertised.")
CAPABILITIES[Feature.CALLBACK_ANSWER] = s(SupportLevel.FULL, "BaleClient.answer_callback_query")
CAPABILITIES[Feature.CALLBACK_ALERT_TOAST] = s(SupportLevel.FULL, "BaleClient.answer_callback_query")
CAPABILITIES[Feature.CALLBACK_DATA_LIMIT] = s(SupportLevel.FULL, "BaleClient.answer_callback_query", callback_data_max_bytes=64)
CAPABILITIES[Feature.UPDATE_OFFSET] = s(SupportLevel.FULL, "BaleClient.get_updates", offset_kind="offset")
CAPABILITIES[Feature.ALLOWED_UPDATES] = s(SupportLevel.FULL, "BaleClient.get_updates")
CAPABILITIES[Feature.LONG_POLL_TIMEOUT] = s(SupportLevel.FULL, "BaleClient.get_updates")
CAPABILITIES[Feature.INLINE_KEYBOARD] = s(SupportLevel.FULL, "bale.InlineKeyboardButton.text")
CAPABILITIES[Feature.REPLY_KEYBOARD] = s(SupportLevel.FULL, "bale.KeyboardButton.text")
CAPABILITIES[Feature.REMOVE_REPLY] = s(SupportLevel.FULL, "bale.KeyboardButton.text")
CAPABILITIES[Feature.FORCE_REPLY] = s(SupportLevel.UNKNOWN, note="No audited Bale ForceReply model.", confidence="low")
for f, field in {Feature.BUTTON_URL:"url", Feature.BUTTON_CALLBACK:"callback_data", Feature.BUTTON_WEB_APP:"web_app", Feature.BUTTON_COPY_TEXT:"copy_text"}.items():
    CAPABILITIES[f] = s(SupportLevel.FULL, f"bale.InlineKeyboardButton.{field}")
for f, field in {
    Feature.BUTTON_COLOR_STYLE:"style", Feature.BUTTON_ICON_EMOJI:"icon_custom_emoji_id", Feature.BUTTON_PAY:"pay", Feature.BUTTON_SWITCH_INLINE:"switch_inline_query", Feature.BUTTON_LOGIN_URL:"login_url",
}.items(): CAPABILITIES[f] = s(SupportLevel.NONE, "docs/decisions.md", note=f"No `{field}` field exists on the audited Bale InlineKeyboardButton.", confidence="inferred")
for f in (Feature.BUTTON_REQUEST_CONTACT, Feature.BUTTON_REQUEST_LOCATION):
    CAPABILITIES[f] = s(SupportLevel.FULL, "bale.KeyboardButton.text")
for f in (Feature.BUTTON_REQUEST_POLL, Feature.BUTTON_REQUEST_USERS, Feature.BUTTON_REQUEST_CHAT):
    CAPABILITIES[f] = s(SupportLevel.NONE, "docs/decisions.md", note="No matching field exists on the audited Bale keyboard button model.", confidence="inferred")
for f in (Feature.TELEGRAM_GAMES, Feature.TELEGRAM_PASSPORT, Feature.TELEGRAM_BUSINESS, Feature.TELEGRAM_STORIES, Feature.TELEGRAM_GIFTS, Feature.TELEGRAM_STARS):
    CAPABILITIES[f] = s(SupportLevel.NONE, "docs/decisions.md", note="This feature is classified as Telegram-only by the Phase 1 specification.", confidence="inferred")
PLATFORM_SPECIFIC_METHODS = ('add_sticker_to_set', 'answer_pre_checkout_query', 'ask_review', 'close', 'close_bot', 'create_invoice_link', 'create_new_sticker_set', 'delete_chat_photo', 'delete_webhook', 'export_chat_invite_link', 'get_chat', 'get_chat_member', 'get_me', 'get_webhook_info', 'inquire_transaction', 'logout', 'revoke_chat_invite_link', 'unpin_all_chat_messages', 'upload_sticker_file', 'field:InlineKeyboardButton.text', 'field:InlineKeyboardButton.callback_data', 'field:InlineKeyboardButton.copy_text', 'field:InlineKeyboardButton.url', 'field:InlineKeyboardButton.web_app', 'field:KeyboardButton.request_contact', 'field:KeyboardButton.request_location', 'field:KeyboardButton.text', 'field:KeyboardButton.web_app')

CAPABILITIES[Feature.WEBHOOK_SECRET_HEADER] = s(SupportLevel.NONE, "docs/decisions.md", note="Bale documents no webhook request secret/header mechanism in the audited contract.", confidence="confirmed")
