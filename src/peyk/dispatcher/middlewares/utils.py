from __future__ import annotations
import asyncio, logging
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol
from peyk.platform_core.capabilities import Feature
logger = logging.getLogger(__name__)

class _BotLike(Protocol):
    platform: str

    async def send_chat_action(self, chat_id: int | str, action: str) -> bool:
        """Sends chat action through the dispatcher API.

Args:
    chat_id: Identifier of the target chat.
    action: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        ...

    async def answer_callback_query(self, callback_query_id: str, *, text: str | None=None, show_alert: bool=False) -> bool:
        """Answers the callback query request through the dispatcher API.

Args:
    callback_query_id: Identifier of the callback query.
    text: Text content supplied to the operation.
    show_alert: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        ...

    def supports(self, feature: Feature) -> bool:
        """Performs the supports operation for the dispatcher client.

Args:
    feature: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        ...

@dataclass
class ChatActionSender:
    """Keep a chat action alive while a handler is running."""
    bot: _BotLike
    chat_id: int | str
    action: str = 'typing'
    interval: float = 4.0

    @classmethod
    def _named(cls, bot: _BotLike, chat_id: int | str, action: str, interval: float=4.0) -> 'ChatActionSender':
        return cls(bot, chat_id, action, interval)

    @classmethod
    def typing(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the typing operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'typing', interval)

    @classmethod
    def upload_photo(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the upload photo operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'upload_photo', interval)

    @classmethod
    def record_video(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the record video operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'record_video', interval)

    @classmethod
    def upload_video(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the upload video operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'upload_video', interval)

    @classmethod
    def record_voice(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the record voice operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'record_voice', interval)

    @classmethod
    def upload_document(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the upload document operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'upload_document', interval)

    @classmethod
    def choose_sticker(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the choose sticker operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'choose_sticker', interval)

    @classmethod
    def find_location(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the find location operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'find_location', interval)

    @classmethod
    def record_video_note(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the record video note operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'record_video_note', interval)

    @classmethod
    def upload_video_note(cls, bot: _BotLike, chat_id: int | str, interval: float=4.0) -> 'ChatActionSender':
        """Performs the upload video note operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    interval: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        return cls._named(bot, chat_id, 'upload_video_note', interval)

    async def __aenter__(self) -> 'ChatActionSender':
        await self.bot.send_chat_action(self.chat_id, self.action)
        self._stop = asyncio.Event()
        self._task = asyncio.create_task(self._loop())
        return self

    async def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=self.interval)
            except asyncio.TimeoutError:
                await self.bot.send_chat_action(self.chat_id, self.action)

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        self._stop.set()
        await self._task

class ChatActionMiddleware:
    """Send the action named by ``flags.chat_action`` around a handler."""

    async def __call__(self, handler: Callable[[], Awaitable[object]], event: object, data: dict[str, object]) -> object:
        action = data.get('flags', {}).get('chat_action') if isinstance(data.get('flags'), dict) else None
        if not isinstance(action, str):
            return await handler()
        bot = data.get('bot')
        chat = getattr(event, 'chat_id', None) or getattr(getattr(event, 'chat', None), 'id', None)
        if bot is None or chat is None or (not bot.supports(Feature.CHAT_ACTIONS)):
            if getattr(bot, 'platform', None) == 'rubika':
                logger.debug('Rubika has no audited chat-action capability; skipping chat action.')
            return await handler()
        async with ChatActionSender(bot, chat, action):
            return await handler()

@dataclass(frozen=True)
class CallbackAnswer:
    """Configuration for automatic callback-query acknowledgement."""
    text: str | None = None
    show_alert: bool = False

class CallbackAnswerMiddleware:
    """Automatically acknowledge callback queries after a handler succeeds."""

    async def __call__(self, handler: Callable[[], Awaitable[object]], event: object, data: dict[str, object]) -> object:
        result = await handler()
        config = data.get('flags', {}).get('callback_answer') if isinstance(data.get('flags'), dict) else None
        if config is None:
            return result
        answer = config if isinstance(config, CallbackAnswer) else CallbackAnswer(config if isinstance(config, str) else None)
        callback_id = getattr(event, 'id', None)
        bot = data.get('bot')
        if callback_id is not None and bot is not None and bot.supports(Feature.CALLBACK_ANSWER):
            await bot.answer_callback_query(callback_id, text=answer.text, show_alert=answer.show_alert)
        return result
