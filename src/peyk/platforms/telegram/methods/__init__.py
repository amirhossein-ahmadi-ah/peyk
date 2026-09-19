"""One-file-per-method Telegram Bot API method package."""

from __future__ import annotations

from ._apply_caption_form import _apply_caption_form
from ._apply_caption_json import _apply_caption_json
from ._apply_send_options_form import _apply_send_options_form
from ._apply_send_options_json import _apply_send_options_json
from ._edit_target import _edit_target
from ._extract_retry_hint import _extract_retry_hint
from ._parse_chat_member_result import _parse_chat_member_result
from ._parse_error_parameters import _parse_error_parameters
from ._resolve_album_item import _resolve_album_item
from ._resolve_sticker_ref import _resolve_sticker_ref
from ._send_file_message import _send_file_message
from peyk.platforms.telegram.methods._serialization import _serialize_entities
from peyk.platforms.telegram.methods._serialization import _serialize_link_preview
from ._serialize_permissions import _serialize_permissions
from ._serialize_poll_media import _serialize_poll_media
from peyk.platforms.telegram.methods._serialization import _serialize_reply_parameters
from .add_sticker_to_set import add_sticker_to_set
from .answer_callback_query import answer_callback_query
from .answer_chat_join_request_query import answer_chat_join_request_query
from .answer_guest_query import answer_guest_query
from .answer_inline_query import answer_inline_query
from .answer_pre_checkout_query import answer_pre_checkout_query
from .answer_shipping_query import answer_shipping_query
from .answer_web_app_query import answer_web_app_query
from .approve_chat_join_request import approve_chat_join_request
from .approve_suggested_post import approve_suggested_post
from .ban_chat_member import ban_chat_member
from .ban_chat_sender_chat import ban_chat_sender_chat
from .build_inline_keyboard_button import build_inline_keyboard_button
from .close_bot import close_bot
from .close_forum_topic import close_forum_topic
from .close_general_forum_topic import close_general_forum_topic
from .convert_gift_to_stars import convert_gift_to_stars
from .copy_message import copy_message
from .copy_messages import copy_messages
from .create_chat_invite_link import create_chat_invite_link
from .create_chat_subscription_invite_link import create_chat_subscription_invite_link
from .create_forum_topic import create_forum_topic
from .create_invoice_link import create_invoice_link
from .create_new_sticker_set import create_new_sticker_set
from .decline_chat_join_request import decline_chat_join_request
from .decline_suggested_post import decline_suggested_post
from .delete_all_message_reactions import delete_all_message_reactions
from .delete_business_messages import delete_business_messages
from .delete_chat_sticker_set import delete_chat_sticker_set
from .delete_ephemeral_message import delete_ephemeral_message
from .delete_forum_topic import delete_forum_topic
from .delete_message_reaction import delete_message_reaction
from .delete_messages import delete_messages
from .delete_my_commands import delete_my_commands
from .delete_sticker_from_set import delete_sticker_from_set
from .delete_sticker_set import delete_sticker_set
from .delete_story import delete_story
from .delete_webhook import delete_webhook
from .edit_chat_invite_link import edit_chat_invite_link
from .edit_chat_subscription_invite_link import edit_chat_subscription_invite_link
from .edit_ephemeral_message_caption import edit_ephemeral_message_caption
from .edit_ephemeral_message_media import edit_ephemeral_message_media
from .edit_ephemeral_message_reply_markup import edit_ephemeral_message_reply_markup
from .edit_ephemeral_message_text import edit_ephemeral_message_text
from .edit_forum_topic import edit_forum_topic
from .edit_general_forum_topic import edit_general_forum_topic
from .edit_message_caption import edit_message_caption
from .edit_message_checklist import edit_message_checklist
from .edit_message_live_location import edit_message_live_location
from .edit_message_media import edit_message_media
from .edit_message_reply_markup import edit_message_reply_markup
from .edit_message_text import edit_message_text
from .edit_story import edit_story
from .edit_user_star_subscription import edit_user_star_subscription
from .export_chat_invite_link import export_chat_invite_link
from .forward_message import forward_message
from .forward_messages import forward_messages
from .get_available_gifts import get_available_gifts
from .get_business_account_gifts import get_business_account_gifts
from .get_business_account_star_balance import get_business_account_star_balance
from .get_business_connection import get_business_connection
from .get_chat_administrators import get_chat_administrators
from .get_chat_gifts import get_chat_gifts
from .get_chat_member_count import get_chat_member_count
from .get_chat_menu_button import get_chat_menu_button
from .get_custom_emoji_stickers import get_custom_emoji_stickers
from .get_forum_topic_icon_stickers import get_forum_topic_icon_stickers
from .get_game_high_scores import get_game_high_scores
from .get_managed_bot_access_settings import get_managed_bot_access_settings
from .get_managed_bot_token import get_managed_bot_token
from .get_my_commands import get_my_commands
from .get_my_default_administrator_rights import get_my_default_administrator_rights
from .get_my_description import get_my_description
from .get_my_name import get_my_name
from .get_my_short_description import get_my_short_description
from .get_my_star_balance import get_my_star_balance
from .get_star_transactions import get_star_transactions
from .get_sticker_set import get_sticker_set
from .get_updates import get_updates
from .get_user_chat_boosts import get_user_chat_boosts
from .get_user_gifts import get_user_gifts
from .get_user_personal_chat_messages import get_user_personal_chat_messages
from .get_user_profile_audios import get_user_profile_audios
from .get_user_profile_photos import get_user_profile_photos
from .gift_premium_subscription import gift_premium_subscription
from .hide_general_forum_topic import hide_general_forum_topic
from .log_out import log_out
from .pin_chat_message import pin_chat_message
from .post_story import post_story
from .promote_chat_member import promote_chat_member
from .read_business_message import read_business_message
from .refund_star_payment import refund_star_payment
from .remove_business_account_profile_photo import remove_business_account_profile_photo
from .remove_chat_verification import remove_chat_verification
from .remove_my_profile_photo import remove_my_profile_photo
from .remove_user_verification import remove_user_verification
from .reopen_forum_topic import reopen_forum_topic
from .reopen_general_forum_topic import reopen_general_forum_topic
from .replace_managed_bot_token import replace_managed_bot_token
from .replace_sticker_in_set import replace_sticker_in_set
from .repost_story import repost_story
from .restrict_chat_member import restrict_chat_member
from .revoke_chat_invite_link import revoke_chat_invite_link
from .save_prepared_inline_message import save_prepared_inline_message
from .save_prepared_keyboard_button import save_prepared_keyboard_button
from .send_animation import send_animation
from .send_audio import send_audio
from .send_chat_action import send_chat_action
from .send_chat_join_request_web_app import send_chat_join_request_web_app
from .send_checklist import send_checklist
from .send_contact import send_contact
from .send_dice import send_dice
from .send_document import send_document
from .send_game import send_game
from .send_gift import send_gift
from .send_invoice import send_invoice
from .send_live_photo import send_live_photo
from .send_location import send_location
from .send_media_group import send_media_group
from .send_message import send_message
from .send_message_draft import send_message_draft
from .send_paid_media import send_paid_media
from .send_photo import send_photo
from .send_poll import send_poll
from .send_rich_message import send_rich_message
from .send_rich_message_draft import send_rich_message_draft
from .send_sticker import send_sticker
from .send_venue import send_venue
from .send_video import send_video
from .send_video_note import send_video_note
from .send_voice import send_voice
from .set_business_account_bio import set_business_account_bio
from .set_business_account_gift_settings import set_business_account_gift_settings
from .set_business_account_name import set_business_account_name
from .set_business_account_profile_photo import set_business_account_profile_photo
from .set_business_account_username import set_business_account_username
from .set_chat_administrator_custom_title import set_chat_administrator_custom_title
from .set_chat_description import set_chat_description
from .set_chat_member_tag import set_chat_member_tag
from .set_chat_menu_button import set_chat_menu_button
from .set_chat_permissions import set_chat_permissions
from .set_chat_photo import set_chat_photo
from .set_chat_sticker_set import set_chat_sticker_set
from .set_custom_emoji_sticker_set_thumbnail import set_custom_emoji_sticker_set_thumbnail
from .set_game_score import set_game_score
from .set_managed_bot_access_settings import set_managed_bot_access_settings
from .set_message_reaction import set_message_reaction
from .set_my_commands import set_my_commands
from .set_my_default_administrator_rights import set_my_default_administrator_rights
from .set_my_description import set_my_description
from .set_my_name import set_my_name
from .set_my_profile_photo import set_my_profile_photo
from .set_my_short_description import set_my_short_description
from .set_passport_data_errors import set_passport_data_errors
from .set_sticker_emoji_list import set_sticker_emoji_list
from .set_sticker_keywords import set_sticker_keywords
from .set_sticker_mask_position import set_sticker_mask_position
from .set_sticker_position_in_set import set_sticker_position_in_set
from .set_sticker_set_thumbnail import set_sticker_set_thumbnail
from .set_sticker_set_title import set_sticker_set_title
from .set_user_emoji_status import set_user_emoji_status
from .set_webhook import set_webhook
from .stop_message_live_location import stop_message_live_location
from .stop_poll import stop_poll
from .transfer_business_account_stars import transfer_business_account_stars
from .transfer_gift import transfer_gift
from .unban_chat_sender_chat import unban_chat_sender_chat
from .unhide_general_forum_topic import unhide_general_forum_topic
from .unpin_all_forum_topic_messages import unpin_all_forum_topic_messages
from .unpin_all_general_forum_topic_messages import unpin_all_general_forum_topic_messages
from .unpin_chat_message import unpin_chat_message
from .upgrade_gift import upgrade_gift
from .upload_sticker_file import upload_sticker_file
from .verify_chat import verify_chat
from .verify_user import verify_user

__all__ = [
    "_apply_caption_form",
    "_apply_caption_json",
    "_apply_send_options_form",
    "_apply_send_options_json",
    "_edit_target",
    "_extract_retry_hint",
    "_parse_chat_member_result",
    "_parse_error_parameters",
    "_resolve_album_item",
    "_resolve_sticker_ref",
    "_send_file_message",
    "_serialize_entities",
    "_serialize_link_preview",
    "_serialize_permissions",
    "_serialize_poll_media",
    "_serialize_reply_parameters",
    "add_sticker_to_set",
    "answer_callback_query",
    "answer_chat_join_request_query",
    "answer_guest_query",
    "answer_inline_query",
    "answer_pre_checkout_query",
    "answer_shipping_query",
    "answer_web_app_query",
    "approve_chat_join_request",
    "approve_suggested_post",
    "ban_chat_member",
    "ban_chat_sender_chat",
    "build_inline_keyboard_button",
    "close_bot",
    "close_forum_topic",
    "close_general_forum_topic",
    "convert_gift_to_stars",
    "copy_message",
    "copy_messages",
    "create_chat_invite_link",
    "create_chat_subscription_invite_link",
    "create_forum_topic",
    "create_invoice_link",
    "create_new_sticker_set",
    "decline_chat_join_request",
    "decline_suggested_post",
    "delete_all_message_reactions",
    "delete_business_messages",
    "delete_chat_sticker_set",
    "delete_ephemeral_message",
    "delete_forum_topic",
    "delete_message_reaction",
    "delete_messages",
    "delete_my_commands",
    "delete_sticker_from_set",
    "delete_sticker_set",
    "delete_story",
    "delete_webhook",
    "edit_chat_invite_link",
    "edit_chat_subscription_invite_link",
    "edit_ephemeral_message_caption",
    "edit_ephemeral_message_media",
    "edit_ephemeral_message_reply_markup",
    "edit_ephemeral_message_text",
    "edit_forum_topic",
    "edit_general_forum_topic",
    "edit_message_caption",
    "edit_message_checklist",
    "edit_message_live_location",
    "edit_message_media",
    "edit_message_reply_markup",
    "edit_message_text",
    "edit_story",
    "edit_user_star_subscription",
    "export_chat_invite_link",
    "forward_message",
    "forward_messages",
    "get_available_gifts",
    "get_business_account_gifts",
    "get_business_account_star_balance",
    "get_business_connection",
    "get_chat_administrators",
    "get_chat_gifts",
    "get_chat_member_count",
    "get_chat_menu_button",
    "get_custom_emoji_stickers",
    "get_forum_topic_icon_stickers",
    "get_game_high_scores",
    "get_managed_bot_access_settings",
    "get_managed_bot_token",
    "get_my_commands",
    "get_my_default_administrator_rights",
    "get_my_description",
    "get_my_name",
    "get_my_short_description",
    "get_my_star_balance",
    "get_star_transactions",
    "get_sticker_set",
    "get_updates",
    "get_user_chat_boosts",
    "get_user_gifts",
    "get_user_personal_chat_messages",
    "get_user_profile_audios",
    "get_user_profile_photos",
    "gift_premium_subscription",
    "hide_general_forum_topic",
    "log_out",
    "pin_chat_message",
    "post_story",
    "promote_chat_member",
    "read_business_message",
    "refund_star_payment",
    "remove_business_account_profile_photo",
    "remove_chat_verification",
    "remove_my_profile_photo",
    "remove_user_verification",
    "reopen_forum_topic",
    "reopen_general_forum_topic",
    "replace_managed_bot_token",
    "replace_sticker_in_set",
    "repost_story",
    "restrict_chat_member",
    "revoke_chat_invite_link",
    "save_prepared_inline_message",
    "save_prepared_keyboard_button",
    "send_animation",
    "send_audio",
    "send_chat_action",
    "send_chat_join_request_web_app",
    "send_checklist",
    "send_contact",
    "send_dice",
    "send_document",
    "send_game",
    "send_gift",
    "send_invoice",
    "send_live_photo",
    "send_location",
    "send_media_group",
    "send_message",
    "send_message_draft",
    "send_paid_media",
    "send_photo",
    "send_poll",
    "send_rich_message",
    "send_rich_message_draft",
    "send_sticker",
    "send_venue",
    "send_video",
    "send_video_note",
    "send_voice",
    "set_business_account_bio",
    "set_business_account_gift_settings",
    "set_business_account_name",
    "set_business_account_profile_photo",
    "set_business_account_username",
    "set_chat_administrator_custom_title",
    "set_chat_description",
    "set_chat_member_tag",
    "set_chat_menu_button",
    "set_chat_permissions",
    "set_chat_photo",
    "set_chat_sticker_set",
    "set_custom_emoji_sticker_set_thumbnail",
    "set_game_score",
    "set_managed_bot_access_settings",
    "set_message_reaction",
    "set_my_commands",
    "set_my_default_administrator_rights",
    "set_my_description",
    "set_my_name",
    "set_my_profile_photo",
    "set_my_short_description",
    "set_passport_data_errors",
    "set_sticker_emoji_list",
    "set_sticker_keywords",
    "set_sticker_mask_position",
    "set_sticker_position_in_set",
    "set_sticker_set_thumbnail",
    "set_sticker_set_title",
    "set_user_emoji_status",
    "set_webhook",
    "stop_message_live_location",
    "stop_poll",
    "transfer_business_account_stars",
    "transfer_gift",
    "unban_chat_sender_chat",
    "unhide_general_forum_topic",
    "unpin_all_forum_topic_messages",
    "unpin_all_general_forum_topic_messages",
    "unpin_chat_message",
    "upgrade_gift",
    "upload_sticker_file",
    "verify_chat",
    "verify_user",
]
