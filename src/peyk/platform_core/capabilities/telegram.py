"""Telegram capability declarations derived from the audited client/models."""
from __future__ import annotations

from . import Feature, Support, SupportLevel
from ._common import s


def _base() -> dict[Feature, Support]:
    return {f: Support(SupportLevel.UNKNOWN, confidence="low", note="Not independently established by the Phase 1 audit.") for f in Feature}

CAPABILITIES = _base()

# Confirmed messaging methods.
for feature, method in {
    Feature.TEXT: "TelegramClient.send_message", Feature.PHOTO: "TelegramClient.send_photo",
    Feature.VIDEO: "TelegramClient.send_video", Feature.AUDIO: "TelegramClient.send_audio",
    Feature.VOICE: "TelegramClient.send_voice", Feature.DOCUMENT: "TelegramClient.send_document",
    Feature.ANIMATION: "TelegramClient.send_animation", Feature.STICKER: "TelegramClient.send_sticker",
    Feature.CONTACT: "TelegramClient.send_contact", Feature.LOCATION: "TelegramClient.send_location",
    Feature.VENUE: "TelegramClient.send_venue", Feature.POLL: "TelegramClient.send_poll",
    Feature.DICE: "TelegramClient.send_dice", Feature.MEDIA_GROUP: "TelegramClient.send_media_group",
    Feature.COPY: "TelegramClient.copy_message", Feature.FORWARD: "TelegramClient.forward_message",
    Feature.EDIT_TEXT: "TelegramClient.edit_message_text", Feature.EDIT_CAPTION: "TelegramClient.edit_message_caption",
    Feature.EDIT_MEDIA: "TelegramClient.edit_message_media", Feature.EDIT_MARKUP: "TelegramClient.edit_message_reply_markup",
    Feature.DELETE: "TelegramClient.delete_message", Feature.BULK_DELETE: "TelegramClient.delete_messages",
    Feature.REPLY_TO: "TelegramClient.send_message", Feature.CHAT_ACTIONS: "TelegramClient.send_chat_action",
    Feature.REACTIONS: "TelegramClient.set_message_reaction", Feature.LINK_PREVIEW_CONTROL: "TelegramClient.send_message",
    Feature.PROTECT_CONTENT: "TelegramClient.send_message", Feature.ENTITIES_FORMATTING: "TelegramClient.send_message",
    Feature.PAYMENTS: "TelegramClient.send_invoice", Feature.INLINE_MODE: "TelegramClient.answer_inline_query",
    Feature.GET_FILE: "TelegramLikeClient.get_file", Feature.POLLING: "TelegramClient.get_updates",
    Feature.WEBHOOK: "TelegramClient.set_webhook", Feature.ALLOWED_UPDATES: "TelegramClient.get_updates",
    Feature.LONG_POLL_TIMEOUT: "TelegramClient.get_updates", Feature.BAN: "TelegramClient.ban_chat_member",
    Feature.UNBAN: "TelegramLikeClient.unban_chat_member", Feature.RESTRICT: "TelegramClient.restrict_chat_member",
    Feature.PROMOTE: "TelegramClient.promote_chat_member", Feature.PIN: "TelegramClient.pin_chat_message",
    Feature.UNPIN: "TelegramClient.unpin_chat_message", Feature.INVITE_LINKS: "TelegramClient.create_chat_invite_link",
    Feature.MEMBER_COUNT: "TelegramClient.get_chat_member_count", Feature.ADMINISTRATORS: "TelegramClient.get_chat_administrators",
    Feature.PERMISSIONS: "TelegramClient.set_chat_permissions", Feature.TITLE: "TelegramLikeClient.set_chat_title",
    Feature.DESCRIPTION: "TelegramClient.set_chat_description", Feature.CHAT_PHOTO: "TelegramClient.set_chat_photo",
    Feature.LEAVE: "TelegramLikeClient.leave_chat", Feature.JOIN_REQUESTS: "TelegramClient.approve_chat_join_request",
    Feature.FORUM_TOPICS: "TelegramClient.create_forum_topic", Feature.MEMBER_STATUS_UPDATES: "TelegramClient.get_updates",
    Feature.UPLOAD_BYTES: "TelegramLikeClient._as_file_payload", Feature.BOT_COMMANDS: "TelegramClient.set_my_commands",
    Feature.BOT_NAME: "TelegramClient.set_my_name", Feature.BOT_DESCRIPTION: "TelegramClient.set_my_description",
}.items():
    CAPABILITIES[feature] = s(SupportLevel.FULL, method)

CAPABILITIES[Feature.ENTITIES_FORMATTING] = s(SupportLevel.FULL, "TelegramClient.send_message", note="Entity and parse-mode parameters are present on the audited client.", parse_modes=("Markdown", "MarkdownV2", "HTML"))
CAPABILITIES[Feature.CALLBACK_ANSWER] = s(SupportLevel.FULL, "TelegramClient.answer_callback_query")
CAPABILITIES[Feature.CALLBACK_ALERT_TOAST] = s(SupportLevel.FULL, "TelegramClient.answer_callback_query", note="The audited method exposes show_alert; toast is the default callback answer path.")
CAPABILITIES[Feature.CALLBACK_DATA_LIMIT] = s(SupportLevel.FULL, "telegram.InlineKeyboardButton.callback_data", callback_data_max_bytes=64)
CAPABILITIES[Feature.UPDATE_OFFSET] = s(SupportLevel.FULL, "TelegramClient.get_updates", offset_kind="offset")
CAPABILITIES[Feature.INLINE_KEYBOARD] = s(SupportLevel.FULL, "telegram.InlineKeyboardButton.text")
CAPABILITIES[Feature.REPLY_KEYBOARD] = s(SupportLevel.FULL, "telegram.KeyboardButton.text")
CAPABILITIES[Feature.REMOVE_REPLY] = s(SupportLevel.FULL, "telegram.KeyboardButton.text")
CAPABILITIES[Feature.FORCE_REPLY] = s(SupportLevel.FULL, "docs/decisions.md")
for f, field in {
    Feature.BUTTON_URL: "url", Feature.BUTTON_CALLBACK: "callback_data", Feature.BUTTON_WEB_APP: "web_app",
    Feature.BUTTON_COPY_TEXT: "copy_text", Feature.BUTTON_ICON_EMOJI: "icon_custom_emoji_id",
    Feature.BUTTON_PAY: "pay", Feature.BUTTON_SWITCH_INLINE: "switch_inline_query", Feature.BUTTON_LOGIN_URL: "login_url",
}.items():
    CAPABILITIES[f] = s(SupportLevel.FULL, f"telegram.InlineKeyboardButton.{field}")
CAPABILITIES[Feature.BUTTON_COLOR_STYLE] = s(SupportLevel.FULL, "telegram.InlineKeyboardButton.style", note="The audited type confirms a style field; the primary/success/danger wire values are inferred from the task specification and are not independently documented in the repository.", confidence="inferred")
for f in (Feature.BUTTON_REQUEST_CONTACT, Feature.BUTTON_REQUEST_LOCATION, Feature.BUTTON_REQUEST_POLL, Feature.BUTTON_REQUEST_USERS, Feature.BUTTON_REQUEST_CHAT):
    CAPABILITIES[f] = s(SupportLevel.FULL, "telegram.KeyboardButton.text")

# Telegram-only API areas are explicitly audited in the client.
for f, ref in {
    Feature.TELEGRAM_GAMES: "TelegramClient.send_game", Feature.TELEGRAM_PASSPORT: "TelegramClient.set_passport_data_errors",
    Feature.TELEGRAM_BUSINESS: "TelegramClient.get_business_connection", Feature.TELEGRAM_STORIES: "TelegramClient.post_story",
    Feature.TELEGRAM_GIFTS: "TelegramClient.get_available_gifts", Feature.TELEGRAM_STARS: "TelegramClient.get_my_star_balance",
}.items():
    CAPABILITIES[f] = s(SupportLevel.FULL, ref)

PLATFORM_SPECIFIC_METHODS = ('add_sticker_to_set', 'answer_chat_join_request_query', 'answer_guest_query', 'answer_pre_checkout_query', 'answer_shipping_query', 'answer_web_app_query', 'approve_suggested_post', 'ban_chat_sender_chat', 'close', 'close_bot', 'close_forum_topic', 'close_general_forum_topic', 'convert_gift_to_stars', 'copy_messages', 'create_chat_subscription_invite_link', 'create_invoice_link', 'create_new_sticker_set', 'decline_chat_join_request', 'decline_suggested_post', 'delete_all_message_reactions', 'delete_business_messages', 'delete_chat_photo', 'delete_chat_sticker_set', 'delete_ephemeral_message', 'delete_forum_topic', 'delete_message_reaction', 'delete_my_commands', 'delete_sticker_from_set', 'delete_sticker_set', 'delete_story', 'delete_webhook', 'edit_chat_invite_link', 'edit_chat_subscription_invite_link', 'edit_ephemeral_message_caption', 'edit_ephemeral_message_media', 'edit_ephemeral_message_reply_markup', 'edit_ephemeral_message_text', 'edit_forum_topic', 'edit_general_forum_topic', 'edit_message_checklist', 'edit_message_live_location', 'edit_story', 'edit_user_star_subscription', 'export_chat_invite_link', 'forward_messages', 'get_business_account_gifts', 'get_business_account_star_balance', 'get_chat', 'get_chat_gifts', 'get_chat_member', 'get_chat_menu_button', 'get_custom_emoji_stickers', 'get_forum_topic_icon_stickers', 'get_game_high_scores', 'get_managed_bot_access_settings', 'get_managed_bot_token', 'get_me', 'get_my_commands', 'get_my_default_administrator_rights', 'get_my_description', 'get_my_name', 'get_my_short_description', 'get_star_transactions', 'get_sticker_set', 'get_user_chat_boosts', 'get_user_gifts', 'get_user_personal_chat_messages', 'get_user_profile_audios', 'get_user_profile_photos', 'get_webhook_info', 'gift_premium_subscription', 'hide_general_forum_topic', 'log_out', 'read_business_message', 'refund_star_payment', 'remove_business_account_profile_photo', 'remove_chat_verification', 'remove_my_profile_photo', 'remove_user_verification', 'reopen_forum_topic', 'reopen_general_forum_topic', 'replace_managed_bot_token', 'replace_sticker_in_set', 'repost_story', 'revoke_chat_invite_link', 'save_prepared_inline_message', 'save_prepared_keyboard_button', 'send_chat_join_request_web_app', 'send_checklist', 'send_gift', 'send_live_photo', 'send_message_draft', 'send_paid_media', 'send_rich_message', 'send_rich_message_draft', 'send_video_note', 'set_business_account_bio', 'set_business_account_gift_settings', 'set_business_account_name', 'set_business_account_profile_photo', 'set_business_account_username', 'set_chat_administrator_custom_title', 'set_chat_member_tag', 'set_chat_menu_button', 'set_chat_sticker_set', 'set_custom_emoji_sticker_set_thumbnail', 'set_game_score', 'set_managed_bot_access_settings', 'set_my_default_administrator_rights', 'set_my_profile_photo', 'set_my_short_description', 'set_sticker_emoji_list', 'set_sticker_keywords', 'set_sticker_mask_position', 'set_sticker_position_in_set', 'set_sticker_set_thumbnail', 'set_sticker_set_title', 'set_user_emoji_status', 'stop_message_live_location', 'stop_poll', 'transfer_business_account_stars', 'transfer_gift', 'unban_chat_sender_chat', 'unhide_general_forum_topic', 'unpin_all_chat_messages', 'unpin_all_forum_topic_messages', 'unpin_all_general_forum_topic_messages', 'upgrade_gift', 'upload_sticker_file', 'verify_chat', 'verify_user', 'field:InlineKeyboardButton.text', 'field:InlineKeyboardButton.disabled', 'field:InlineKeyboardButton.switch_inline_query_current_chat', 'field:InlineKeyboardButton.switch_inline_query_chosen_chat', 'field:InlineKeyboardButton.callback_game', 'field:KeyboardButton.text', 'field:KeyboardButton.request_users', 'field:KeyboardButton.request_chat', 'field:InlineKeyboardButton.callback_data', 'field:InlineKeyboardButton.copy_text', 'field:InlineKeyboardButton.icon_custom_emoji_id', 'field:InlineKeyboardButton.login_url', 'field:InlineKeyboardButton.pay', 'field:InlineKeyboardButton.style', 'field:InlineKeyboardButton.switch_inline_query', 'field:InlineKeyboardButton.url', 'field:InlineKeyboardButton.web_app', 'field:KeyboardButton.icon_custom_emoji_id', 'field:KeyboardButton.request_contact', 'field:KeyboardButton.request_location', 'field:KeyboardButton.request_managed_bot', 'field:KeyboardButton.request_poll', 'field:KeyboardButton.style', 'field:KeyboardButton.web_app')
CAPABILITIES[Feature.WEBHOOK_SECRET_HEADER] = s(SupportLevel.FULL, "TelegramClient.set_webhook", note="Telegram enforces secret_token through the X-Telegram-Bot-Api-Secret-Token request header.")
