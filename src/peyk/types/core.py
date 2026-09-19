"""Neutral inbound bot objects and their bound actions."""
from __future__ import annotations

from dataclasses import dataclass, field
from peyk.enums import ChatType, ContentType
from typing import TYPE_CHECKING, Any, Optional, Union

from peyk.platform_core.contracts.message import IncomingMessage, Identifier
from peyk.platform_core.contracts.callback import IncomingCallbackQuery
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from peyk.utils.text_formatting import RichText
    from peyk.formatting import Text

TextContent = Union[str, "RichText", "Text"]

if TYPE_CHECKING:
    from peyk.bot.base import Bot


@dataclass(frozen=True)
class User:
    """Platform-neutral user identity."""

    id: Identifier
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    raw: object = field(default=None, repr=False, compare=False, hash=False)  # raw escape hatch; platform model is intentionally untyped.


@dataclass(frozen=True)
class Chat:
    """Platform-neutral chat identity and display metadata."""

    id: Identifier
    type: ChatType
    title: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    raw: object = field(default=None, repr=False, compare=False, hash=False)  # raw escape hatch; platform model is intentionally untyped.


@dataclass(frozen=True)
class File:
    """Platform-neutral file descriptor returned by ``Bot.get_file``."""

    id: str
    path: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    raw: object = field(default=None, repr=False, compare=False, hash=False)  # raw escape hatch.


@dataclass(frozen=True)
class ChatMember:
    """Platform-neutral chat membership status."""

    status: str
    user: Optional[User] = None
    raw: object = field(default=None, repr=False, compare=False, hash=False)  # raw escape hatch.


class _BoundActions:
    """Common binding check shared by normalized event objects."""

    bot: Optional["Bot"]

    def _require_bot(self) -> "Bot":
        from peyk.bot.base import BotNotBoundError
        if self.bot is None:
            raise BotNotBoundError("This event is not bound to a Bot; use Bot.normalize_update() first.")
        return self.bot


@dataclass(frozen=True)
class Message(IncomingMessage, _BoundActions):
    """Normalized message with a bound :class:`peyk.Bot` action surface."""

    from_user: Optional[User] = None
    chat: Optional[Chat] = None
    content_type: ContentType = ContentType.UNKNOWN
    bot: Optional["Bot"] = field(default=None, repr=False, compare=False, hash=False)

    def _chat(self) -> Identifier:
        if self.chat_id is None:
            raise ValueError("This message has no chat_id")
        return self.chat_id

    def _message(self) -> Identifier:
        if self.message_id is None:
            raise ValueError("This message has no message_id")
        return self.message_id

    async def answer(self, text: TextContent, **kwargs: object) -> "Message":
        """Send a text message to this message's chat."""
        return await self._require_bot().send_message(self._chat(), text, reply_to_message_id=self._message(), **kwargs)

    async def reply(self, text: TextContent, **kwargs: object) -> "Message":
        """Alias for :meth:`answer`."""
        return await self.answer(text, **kwargs)

    async def edit_text(self, text: TextContent, **kwargs: object) -> "Message":
        """Edit this message's text."""
        return await self._require_bot().edit_message_text(self._chat(), self._message(), text, **kwargs)

    async def delete(self) -> bool:
        """Delete this message."""
        return await self._require_bot().delete_message(self._chat(), self._message())

    async def forward(self, chat_id: Identifier) -> "Message":
        """Forward this message to ``chat_id``."""
        return await self._require_bot().forward_message(chat_id, self._chat(), self._message())

    async def answer_photo(self, photo: object, *, caption: TextContent | None = None, **kwargs: object) -> "Message":
        """Send a photo in this message's chat."""
        if caption is not None:
            kwargs["caption"] = caption
        return await self._require_bot().send_photo(self._chat(), photo, reply_to_message_id=self._message(), **kwargs)

    async def answer_video(self, video: object, *, caption: TextContent | None = None, **kwargs: object) -> "Message":
        """Send a video in this message's chat."""
        if caption is not None:
            kwargs["caption"] = caption
        return await self._require_bot().send_video(self._chat(), video, reply_to_message_id=self._message(), **kwargs)

    async def answer_audio(self, audio: object, *, caption: TextContent | None = None, **kwargs: object) -> "Message":
        """Send audio in this message's chat."""
        if caption is not None:
            kwargs["caption"] = caption
        return await self._require_bot().send_audio(self._chat(), audio, reply_to_message_id=self._message(), **kwargs)

    async def answer_voice(self, voice: object, *, caption: TextContent | None = None, **kwargs: object) -> "Message":
        """Send a voice message in this message's chat."""
        if caption is not None:
            kwargs["caption"] = caption
        return await self._require_bot().send_voice(self._chat(), voice, reply_to_message_id=self._message(), **kwargs)

    async def answer_document(self, document: object, *, caption: TextContent | None = None, **kwargs: object) -> "Message":
        """Send a document in this message's chat."""
        if caption is not None:
            kwargs["caption"] = caption
        return await self._require_bot().send_document(self._chat(), document, reply_to_message_id=self._message(), **kwargs)

    async def answer_chat_action(self, action: str) -> bool:
        """Send a chat action to this message's chat."""
        return await self._require_bot().send_chat_action(self._chat(), action)


@dataclass(frozen=True)
class CallbackQuery(IncomingCallbackQuery, _BoundActions):
    """Normalized callback event with message actions when a message exists."""

    from_user: Optional[User] = None
    message: Optional[Message] = None
    bot: Optional["Bot"] = field(default=None, repr=False, compare=False, hash=False)

    async def answer(self, text: Optional[str] = None, show_alert: bool = False) -> bool:
        """Answer this callback, degrading cosmetic toast/alert differences by policy."""
        bot = self._require_bot()
        if self.id is None:
            return await bot._unsupported_callback_answer(text=text, show_alert=show_alert)
        return await bot.answer_callback_query(self.id, text=text, show_alert=show_alert)
