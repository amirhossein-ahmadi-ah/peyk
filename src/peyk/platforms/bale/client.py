"""Bale client facade preserving the historical import surface."""
from __future__ import annotations
from typing import Any, Dict
from .errors import BaleAPIError
from .._telegram_like import TelegramLikeClient
from .models import Chat, ChatMember, File, Message, PreCheckoutQuery, StickerSet, Transaction, Update, User, WebhookInfo
from .types import *
from .methods import *
BASE_URL = 'https://tapi.bale.ai'
MAX_CALLBACK_DATA_BYTES = 64

def validate_callback_data(data: str) -> None:
    """Performs the validate callback data operation for the Bale client.

Args:
    data: Value used by this operation."""
    'Validate Bale callback data using the shared rule.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``None``).\n    '
    BaleClient.validate_callback_data(data)

def build_inline_keyboard_button(text: str, callback_data: str) -> Dict[str, str]:
    """Performs the build inline keyboard button operation for the Bale client.

Args:
    text: Text content supplied to the operation.
    callback_data: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Build a Bale-compatible common-subset inline button.\n    \n    Args:\n        text: Value of the declared parameter type.\n        callback_data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Dict[str, str]``).\n    '
    return BaleClient._build_inline_keyboard_button_payload(text, callback_data)

class BaleClient(TelegramLikeClient[User, WebhookInfo, File, Chat, ChatMember]):
    """A thin, typed async wrapper around the Bale Bot API.

    Bale-specific lifecycle behavior includes ``close_bot``; member counts use
    Bale's ``getChatMembersCount`` operation rather than Telegram's
    ``getChatMemberCount`` name.

    Args:
        token: The bot token issued by Bale.
        session: Optional existing transport session.
        retry_policy: Optional transport retry policy.
        logger: Logger used by a newly-created session.
        base_url: Optional API base URL override for local tests.
    """
    base_url = BASE_URL
    chat_model = Chat
    chat_member_parser = ChatMember.from_dict
    chat_member_count_method = 'getChatMembersCount'
    _error_class = BaleAPIError
    user_model = User
    webhook_info_model = WebhookInfo
    file_model = File
    logout = logout
    close_bot = close_bot
    send_message = send_message
    edit_message_text = edit_message_text
    edit_message_caption = edit_message_caption
    edit_message_reply_markup = edit_message_reply_markup
    forward_message = forward_message
    copy_message = copy_message
    ban_chat_member = ban_chat_member
    promote_chat_member = promote_chat_member
    get_chat_administrators = get_chat_administrators
    pin_chat_message = pin_chat_message
    unpin_chat_message = unpin_chat_message
    get_chat_members_count = get_chat_members_count
    set_chat_description = set_chat_description
    set_chat_photo = set_chat_photo
    create_chat_invite_link = create_chat_invite_link
    revoke_chat_invite_link = revoke_chat_invite_link
    export_chat_invite_link = export_chat_invite_link
    send_chat_action = send_chat_action
    answer_callback_query = answer_callback_query
    ask_review = ask_review
    send_photo = send_photo
    send_document = send_document
    send_audio = send_audio
    send_video = send_video
    send_animation = send_animation
    send_voice = send_voice
    _send_media = _send_media
    send_media_group = send_media_group
    send_location = send_location
    send_contact = send_contact
    upload_sticker_file = upload_sticker_file
    create_new_sticker_set = create_new_sticker_set
    add_sticker_to_set = add_sticker_to_set
    send_invoice = send_invoice
    create_invoice_link = create_invoice_link
    answer_pre_checkout_query = answer_pre_checkout_query
    inquire_transaction = inquire_transaction
    get_updates = get_updates
    set_webhook = set_webhook
    delete_webhook = delete_webhook
