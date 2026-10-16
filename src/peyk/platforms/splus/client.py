"""Async client for the Soroush Plus (Splus) bot API.

Splus exposes a Telegram-shaped HTTP Bot API at
``https://api.splus.ir/bot<TOKEN>/<method>``: the same JSON envelope, the same
method names (``getMe``, ``sendMessage``, ``getUpdates``, ``setWebhook`` ...),
and Telegram-style ``Update``/``Message``/``CallbackQuery`` objects.  The client
therefore reuses the Telegram models, request mechanics and per-method
implementations, but binds **only the methods that published Splus client
libraries confirm** (see ``SPLUS_METHODS``).  It deliberately does not inherit
the full Telegram surface.  Beyond that it adds:

* the base URL and error class;
* a request-level translation of two modern-Telegram parameters
  (``reply_parameters`` and ``link_preview_options``) into the classic
  ``reply_to_message_id`` / ``allow_sending_without_reply`` /
  ``disable_web_page_preview`` fields that the published Splus client
  libraries use;
* the list of update kinds Splus delivers (``SPLUS_UPDATE_TYPES``).

Support levels per feature are declared in
``peyk.platform_core.capabilities.splus``.
"""
from __future__ import annotations

from typing import Dict, Mapping, Optional

import orjson

from peyk.platforms._telegram_like import TelegramLikeClient
from peyk.platforms.telegram import methods as _m
from peyk.platforms.telegram.models import ChatFullInfo, ChatMember, File, User, WebhookInfo, parse_chat_member
from peyk.transport import FilePayload

from .errors import SplusAPIError

BASE_URL = "https://api.splus.ir"

#: Update kinds the Splus bot API is known to deliver.
SPLUS_UPDATE_TYPES: tuple[str, ...] = ("message", "edited_message", "callback_query")


def _translate_fields(fields: Dict[str, object]) -> None:
    """Rewrite modern-Telegram request fields to the classic form, in place.

    Values may be native objects (JSON bodies) or JSON strings (multipart form
    fields); both shapes are understood.
    """
    reply = fields.pop("reply_parameters", None)
    if isinstance(reply, (str, bytes)):
        try:
            reply = orjson.loads(reply)
        except orjson.JSONDecodeError:
            reply = None
    if isinstance(reply, Mapping):
        if reply.get("message_id") is not None:
            fields["reply_to_message_id"] = reply["message_id"]
        if reply.get("allow_sending_without_reply") is not None:
            fields["allow_sending_without_reply"] = reply["allow_sending_without_reply"]

    preview = fields.pop("link_preview_options", None)
    if isinstance(preview, (str, bytes)):
        try:
            preview = orjson.loads(preview)
        except orjson.JSONDecodeError:
            preview = None
    if isinstance(preview, Mapping) and preview.get("is_disabled") is not None:
        fields["disable_web_page_preview"] = preview["is_disabled"]


def _translated(fields: Optional[Mapping[str, object]]) -> Optional[Dict[str, object]]:
    if fields is None:
        return None
    copy = dict(fields)
    _translate_fields(copy)
    return copy


class SplusClient(TelegramLikeClient[User, WebhookInfo, File, ChatFullInfo, ChatMember]):
    """A thin, typed async wrapper around the Soroush Plus bot API.

    Args:
        token: The bot token issued by Soroush Plus' bot father.
        session: An existing ``peyk.transport.Session`` to reuse.
        retry_policy: Transport-level retry policy for this client's calls.
        logger: Passed to the ``Session`` this client builds itself.
        base_url: Override for the API base URL (tests, proxies).
    """

    base_url = BASE_URL
    chat_model = ChatFullInfo
    chat_member_parser = parse_chat_member
    chat_member_count_method = 'getChatMemberCount'
    _error_class = SplusAPIError
    user_model = User
    webhook_info_model = WebhookInfo
    file_model = File

    async def _call(self, method_name: str, *, json_body: Optional[Mapping[str, object]] = None, data: Optional[Mapping[str, str]] = None, files: Optional[Mapping[str, FilePayload]] = None) -> object:
        """POST a Splus method; see :meth:`TelegramLikeClient._call`."""
        return await super()._call(method_name, json_body=_translated(json_body), data=_translated(data), files=files)


# Methods confirmed for Splus by its published client libraries.  Each name is
# the Telegram-shaped implementation re-used verbatim; the neutral request
# fields are rewritten in ``SplusClient._call``.
SPLUS_METHODS: tuple[str, ...] = (
    "get_updates", "set_webhook", "delete_webhook", "log_out",
    "send_message", "forward_message", "copy_message",
    "send_photo", "send_audio", "send_document", "send_video", "send_animation",
    "send_voice", "send_video_note", "send_media_group", "send_location",
    "send_contact", "send_sticker",
    "edit_message_text", "edit_message_caption", "edit_message_media", "edit_message_reply_markup",
    "answer_callback_query",
    "set_my_commands", "get_my_commands", "delete_my_commands",
)

_HELPERS: tuple[str, ...] = (
    "_apply_send_options_json", "_apply_send_options_form", "_send_file_message",
    "_resolve_album_item", "_edit_target", "_parse_error_parameters", "_extract_retry_hint",
)

for _name in SPLUS_METHODS + _HELPERS:
    setattr(SplusClient, _name, getattr(_m, _name))
SplusClient._apply_caption_json = staticmethod(_m._apply_caption_json)
SplusClient._apply_caption_form = staticmethod(_m._apply_caption_form)

__all__ = ["BASE_URL", "SPLUS_METHODS", "SPLUS_UPDATE_TYPES", "SplusClient"]
