"""Compatibility facade for the Telegram Bot API client.

The concrete Telegram Bot API methods live one-per-file under
``platforms.telegram.methods``. This module preserves the historical
``TelegramClient`` import path and class attributes while keeping the client
logic unchanged.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload, Session
from .errors import TelegramAPIError, ResponseParameters
from .._telegram_like import TelegramLikeClient
from .models import *

BASE_URL = 'https://api.telegram.org'

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

from .methods import *  # noqa: F401,F403

# Legacy top-level helpers remain importable from this module.
_serialize_entities = globals().get("_serialize_entities")
_serialize_reply_parameters = globals().get("_serialize_reply_parameters")
_serialize_link_preview = globals().get("_serialize_link_preview")
_resolve_sticker_ref = globals().get("_resolve_sticker_ref")
build_inline_keyboard_button = globals().get("build_inline_keyboard_button")


class TelegramClient(TelegramLikeClient[User, WebhookInfo, File, ChatFullInfo, ChatMember]):
    """A thin, typed async wrapper around the Telegram Bot API.

    Args:
        token: The bot token issued by Telegram (``@BotFather``).
        session: An existing ``peyk.transport.Session`` to reuse. If not
            given, a default-tuned ``Session`` is built.
        retry_policy: Transport-level retry policy for this client's
            calls. Defaults to ``RetryPolicy()``'s defaults.
        logger: Passed through to a ``Session`` this client builds itself;
            ignored if an existing ``session`` is given (that session
            already has its own logger).
        base_url: Override for the API base URL. Not part of the real
            Telegram API surface -- exists solely so tests can point this
            client at a local fake server instead of ``api.telegram.org``.
    """

    base_url = BASE_URL
    chat_model = ChatFullInfo
    chat_member_parser = parse_chat_member
    chat_member_count_method = 'getChatMemberCount'
    _error_class = TelegramAPIError
    user_model = User
    webhook_info_model = WebhookInfo
    file_model = File

TelegramClient.get_updates = get_updates
TelegramClient.set_webhook = set_webhook
TelegramClient.delete_webhook = delete_webhook
TelegramClient.send_message = send_message
TelegramClient.forward_message = forward_message
TelegramClient.forward_messages = forward_messages
TelegramClient.copy_message = copy_message
TelegramClient.copy_messages = copy_messages
TelegramClient.delete_messages = delete_messages
TelegramClient.edit_message_text = edit_message_text
TelegramClient.edit_message_reply_markup = edit_message_reply_markup
TelegramClient._apply_send_options_json = _apply_send_options_json
TelegramClient._apply_send_options_form = _apply_send_options_form
TelegramClient._apply_caption_json = staticmethod(_apply_caption_json)
TelegramClient._apply_caption_form = staticmethod(_apply_caption_form)
TelegramClient._send_file_message = _send_file_message
TelegramClient.send_photo = send_photo
TelegramClient.send_audio = send_audio
TelegramClient.send_document = send_document
TelegramClient.send_video = send_video
TelegramClient.send_animation = send_animation
TelegramClient.send_voice = send_voice
TelegramClient.send_video_note = send_video_note
TelegramClient.send_live_photo = send_live_photo
TelegramClient._resolve_album_item = _resolve_album_item
TelegramClient.send_media_group = send_media_group
TelegramClient._edit_target = _edit_target
TelegramClient.edit_message_media = edit_message_media
TelegramClient.edit_message_caption = edit_message_caption
TelegramClient._serialize_poll_media = staticmethod(_serialize_poll_media)
TelegramClient.send_location = send_location
TelegramClient.edit_message_live_location = edit_message_live_location
TelegramClient.stop_message_live_location = stop_message_live_location
TelegramClient.send_venue = send_venue
TelegramClient.send_contact = send_contact
TelegramClient.send_poll = send_poll
TelegramClient.stop_poll = stop_poll
TelegramClient.send_dice = send_dice
TelegramClient._serialize_permissions = staticmethod(_serialize_permissions)
TelegramClient.ban_chat_member = ban_chat_member
TelegramClient.restrict_chat_member = restrict_chat_member
TelegramClient.promote_chat_member = promote_chat_member
TelegramClient.set_chat_administrator_custom_title = set_chat_administrator_custom_title
TelegramClient.ban_chat_sender_chat = ban_chat_sender_chat
TelegramClient.unban_chat_sender_chat = unban_chat_sender_chat
TelegramClient.set_chat_permissions = set_chat_permissions
TelegramClient.export_chat_invite_link = export_chat_invite_link
TelegramClient.create_chat_invite_link = create_chat_invite_link
TelegramClient.edit_chat_invite_link = edit_chat_invite_link
TelegramClient.revoke_chat_invite_link = revoke_chat_invite_link
TelegramClient.approve_chat_join_request = approve_chat_join_request
TelegramClient.decline_chat_join_request = decline_chat_join_request
TelegramClient.set_chat_photo = set_chat_photo
TelegramClient.set_chat_description = set_chat_description
TelegramClient.pin_chat_message = pin_chat_message
TelegramClient.unpin_chat_message = unpin_chat_message
TelegramClient.get_chat_member_count = get_chat_member_count
TelegramClient._parse_chat_member_result = _parse_chat_member_result
TelegramClient.get_chat_administrators = get_chat_administrators
TelegramClient.set_chat_sticker_set = set_chat_sticker_set
TelegramClient.delete_chat_sticker_set = delete_chat_sticker_set
TelegramClient._parse_error_parameters = _parse_error_parameters
TelegramClient._extract_retry_hint = _extract_retry_hint
TelegramClient.create_forum_topic = create_forum_topic
TelegramClient.edit_forum_topic = edit_forum_topic
TelegramClient.close_forum_topic = close_forum_topic
TelegramClient.reopen_forum_topic = reopen_forum_topic
TelegramClient.delete_forum_topic = delete_forum_topic
TelegramClient.unpin_all_forum_topic_messages = unpin_all_forum_topic_messages
TelegramClient.edit_general_forum_topic = edit_general_forum_topic
TelegramClient.close_general_forum_topic = close_general_forum_topic
TelegramClient.reopen_general_forum_topic = reopen_general_forum_topic
TelegramClient.hide_general_forum_topic = hide_general_forum_topic
TelegramClient.unhide_general_forum_topic = unhide_general_forum_topic
TelegramClient.unpin_all_general_forum_topic_messages = unpin_all_general_forum_topic_messages
TelegramClient.get_forum_topic_icon_stickers = get_forum_topic_icon_stickers
TelegramClient.answer_callback_query = answer_callback_query
TelegramClient.set_my_commands = set_my_commands
TelegramClient.get_my_commands = get_my_commands
TelegramClient.delete_my_commands = delete_my_commands
TelegramClient.set_my_name = set_my_name
TelegramClient.get_my_name = get_my_name
TelegramClient.set_my_description = set_my_description
TelegramClient.get_my_description = get_my_description
TelegramClient.set_my_short_description = set_my_short_description
TelegramClient.get_my_short_description = get_my_short_description
TelegramClient.set_chat_menu_button = set_chat_menu_button
TelegramClient.get_chat_menu_button = get_chat_menu_button
TelegramClient.set_my_default_administrator_rights = set_my_default_administrator_rights
TelegramClient.get_my_default_administrator_rights = get_my_default_administrator_rights
TelegramClient.answer_inline_query = answer_inline_query
TelegramClient.save_prepared_inline_message = save_prepared_inline_message
TelegramClient.send_sticker = send_sticker
TelegramClient.get_sticker_set = get_sticker_set
TelegramClient.get_custom_emoji_stickers = get_custom_emoji_stickers
TelegramClient.upload_sticker_file = upload_sticker_file
TelegramClient.create_new_sticker_set = create_new_sticker_set
TelegramClient.add_sticker_to_set = add_sticker_to_set
TelegramClient.set_sticker_position_in_set = set_sticker_position_in_set
TelegramClient.delete_sticker_from_set = delete_sticker_from_set
TelegramClient.replace_sticker_in_set = replace_sticker_in_set
TelegramClient.set_sticker_emoji_list = set_sticker_emoji_list
TelegramClient.set_sticker_keywords = set_sticker_keywords
TelegramClient.set_sticker_mask_position = set_sticker_mask_position
TelegramClient.set_sticker_set_title = set_sticker_set_title
TelegramClient.set_sticker_set_thumbnail = set_sticker_set_thumbnail
TelegramClient.set_custom_emoji_sticker_set_thumbnail = set_custom_emoji_sticker_set_thumbnail
TelegramClient.delete_sticker_set = delete_sticker_set
TelegramClient.log_out = log_out
TelegramClient.close_bot = close_bot
TelegramClient.send_paid_media = send_paid_media
TelegramClient.send_checklist = send_checklist
TelegramClient.send_message_draft = send_message_draft
TelegramClient.send_chat_action = send_chat_action
TelegramClient.set_message_reaction = set_message_reaction
TelegramClient.get_user_profile_photos = get_user_profile_photos
TelegramClient.get_user_profile_audios = get_user_profile_audios
TelegramClient.set_user_emoji_status = set_user_emoji_status
TelegramClient.set_chat_member_tag = set_chat_member_tag
TelegramClient.create_chat_subscription_invite_link = create_chat_subscription_invite_link
TelegramClient.edit_chat_subscription_invite_link = edit_chat_subscription_invite_link
TelegramClient.answer_chat_join_request_query = answer_chat_join_request_query
TelegramClient.send_chat_join_request_web_app = send_chat_join_request_web_app
TelegramClient.get_user_personal_chat_messages = get_user_personal_chat_messages
TelegramClient.answer_guest_query = answer_guest_query
TelegramClient.get_user_chat_boosts = get_user_chat_boosts
TelegramClient.get_business_connection = get_business_connection
TelegramClient.get_managed_bot_token = get_managed_bot_token
TelegramClient.replace_managed_bot_token = replace_managed_bot_token
TelegramClient.get_managed_bot_access_settings = get_managed_bot_access_settings
TelegramClient.set_managed_bot_access_settings = set_managed_bot_access_settings
TelegramClient.set_my_profile_photo = set_my_profile_photo
TelegramClient.remove_my_profile_photo = remove_my_profile_photo
TelegramClient.get_available_gifts = get_available_gifts
TelegramClient.send_gift = send_gift
TelegramClient.gift_premium_subscription = gift_premium_subscription
TelegramClient.verify_user = verify_user
TelegramClient.verify_chat = verify_chat
TelegramClient.remove_user_verification = remove_user_verification
TelegramClient.remove_chat_verification = remove_chat_verification
TelegramClient.read_business_message = read_business_message
TelegramClient.delete_business_messages = delete_business_messages
TelegramClient.set_business_account_name = set_business_account_name
TelegramClient.set_business_account_username = set_business_account_username
TelegramClient.set_business_account_bio = set_business_account_bio
TelegramClient.set_business_account_profile_photo = set_business_account_profile_photo
TelegramClient.remove_business_account_profile_photo = remove_business_account_profile_photo
TelegramClient.set_business_account_gift_settings = set_business_account_gift_settings
TelegramClient.get_business_account_star_balance = get_business_account_star_balance
TelegramClient.transfer_business_account_stars = transfer_business_account_stars
TelegramClient.get_business_account_gifts = get_business_account_gifts
TelegramClient.get_user_gifts = get_user_gifts
TelegramClient.get_chat_gifts = get_chat_gifts
TelegramClient.convert_gift_to_stars = convert_gift_to_stars
TelegramClient.upgrade_gift = upgrade_gift
TelegramClient.transfer_gift = transfer_gift
TelegramClient.post_story = post_story
TelegramClient.repost_story = repost_story
TelegramClient.edit_story = edit_story
TelegramClient.delete_story = delete_story
TelegramClient.answer_web_app_query = answer_web_app_query
TelegramClient.save_prepared_keyboard_button = save_prepared_keyboard_button
TelegramClient.edit_message_checklist = edit_message_checklist
TelegramClient.edit_ephemeral_message_text = edit_ephemeral_message_text
TelegramClient.edit_ephemeral_message_media = edit_ephemeral_message_media
TelegramClient.edit_ephemeral_message_caption = edit_ephemeral_message_caption
TelegramClient.edit_ephemeral_message_reply_markup = edit_ephemeral_message_reply_markup
TelegramClient.approve_suggested_post = approve_suggested_post
TelegramClient.decline_suggested_post = decline_suggested_post
TelegramClient.delete_ephemeral_message = delete_ephemeral_message
TelegramClient.delete_message_reaction = delete_message_reaction
TelegramClient.delete_all_message_reactions = delete_all_message_reactions
TelegramClient.send_rich_message = send_rich_message
TelegramClient.send_rich_message_draft = send_rich_message_draft
TelegramClient.send_invoice = send_invoice
TelegramClient.create_invoice_link = create_invoice_link
TelegramClient.answer_shipping_query = answer_shipping_query
TelegramClient.answer_pre_checkout_query = answer_pre_checkout_query
TelegramClient.get_my_star_balance = get_my_star_balance
TelegramClient.get_star_transactions = get_star_transactions
TelegramClient.refund_star_payment = refund_star_payment
TelegramClient.edit_user_star_subscription = edit_user_star_subscription
TelegramClient.set_passport_data_errors = set_passport_data_errors
TelegramClient.send_game = send_game
TelegramClient.set_game_score = set_game_score
TelegramClient.get_game_high_scores = get_game_high_scores

__all__ = [
    "BASE_URL",
    "ChatId",
    "EntitiesInput",
    "MediaInput",
    "TelegramClient",
    "build_inline_keyboard_button",
    "_serialize_entities",
    "_serialize_reply_parameters",
    "_serialize_link_preview",
    "_resolve_sticker_ref",
]
