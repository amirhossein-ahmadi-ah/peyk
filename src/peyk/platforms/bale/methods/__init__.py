"""Bale client methods, one module per method."""

from .logout import logout
from .close_bot import close_bot
from .send_message import send_message
from .edit_message_text import edit_message_text
from .edit_message_caption import edit_message_caption
from .edit_message_reply_markup import edit_message_reply_markup
from .forward_message import forward_message
from .copy_message import copy_message
from .ban_chat_member import ban_chat_member
from .restrict_chat_member import restrict_chat_member
from .promote_chat_member import promote_chat_member
from .get_chat_administrators import get_chat_administrators
from .pin_chat_message import pin_chat_message
from .unpin_chat_message import unpin_chat_message
from .get_chat_members_count import get_chat_members_count
from .set_chat_description import set_chat_description
from .set_chat_photo import set_chat_photo
from .create_chat_invite_link import create_chat_invite_link
from .revoke_chat_invite_link import revoke_chat_invite_link
from .export_chat_invite_link import export_chat_invite_link
from .send_chat_action import send_chat_action
from .answer_callback_query import answer_callback_query
from .ask_review import ask_review
from .send_photo import send_photo
from .send_document import send_document
from .send_audio import send_audio
from .send_video import send_video
from .send_animation import send_animation
from .send_voice import send_voice
from ._send_media import _send_media
from .send_media_group import send_media_group
from .send_location import send_location
from .send_contact import send_contact
from .upload_sticker_file import upload_sticker_file
from .create_new_sticker_set import create_new_sticker_set
from .add_sticker_to_set import add_sticker_to_set
from .send_invoice import send_invoice
from .create_invoice_link import create_invoice_link
from .answer_pre_checkout_query import answer_pre_checkout_query
from .inquire_transaction import inquire_transaction
from .get_updates import get_updates
from .set_webhook import set_webhook
from .delete_webhook import delete_webhook

__all__ = ['logout', 'close_bot', 'send_message', 'edit_message_text', 'edit_message_caption', 'edit_message_reply_markup', 'forward_message', 'copy_message', 'ban_chat_member', 'restrict_chat_member', 'promote_chat_member', 'get_chat_administrators', 'pin_chat_message', 'unpin_chat_message', 'get_chat_members_count', 'set_chat_description', 'set_chat_photo', 'create_chat_invite_link', 'revoke_chat_invite_link', 'export_chat_invite_link', 'send_chat_action', 'answer_callback_query', 'ask_review', 'send_photo', 'send_document', 'send_audio', 'send_video', 'send_animation', 'send_voice', '_send_media', 'send_media_group', 'send_location', 'send_contact', 'upload_sticker_file', 'create_new_sticker_set', 'add_sticker_to_set', 'send_invoice', 'create_invoice_link', 'answer_pre_checkout_query', 'inquire_transaction', 'get_updates', 'set_webhook', 'delete_webhook']
