"""Dispatcher middleware that injects FSM context and event isolation."""
from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from peyk.bot import Bot
from peyk.dispatcher.middlewares.base import BaseMiddleware

from .context import FSMContext, FSMStrategy, build_storage_key
from .storage.base import BaseStorage
from .storage.isolation import BaseEventIsolation, DisabledEventIsolation

logger = logging.getLogger(__name__)


class FSMContextMiddleware(BaseMiddleware):
    """Inject ``state`` and ``raw_state`` for every normalized dispatcher event."""

    def __init__(
        self,
        storage: BaseStorage,
        *,
        strategy: str | FSMStrategy = FSMStrategy.USER_IN_CHAT,
        events_isolation: BaseEventIsolation | None = None,
    ) -> None:
        self.storage = storage
        self.strategy = strategy
        self.events_isolation = events_isolation or DisabledEventIsolation()

    async def __call__(
        self,
        handler: Callable[[], Awaitable[object]],
        event: object,
        data: dict[str, object],
    ) -> object:
        bot_value = data.get("bot")
        if not isinstance(bot_value, Bot):
            raise RuntimeError("FSMContextMiddleware requires dispatcher DI key 'bot'")
        bot = bot_value
        try:
            key = build_storage_key(
                event,
                platform=bot.platform,
                bot_id=bot.id,
                strategy=self.strategy,
            )
        except ValueError as exc:
            # Some updates have no chat/user to key a conversation on (for
            # example a raw Telegram ``inline_query`` that no native observer
            # handled).  They cannot use FSM state, but that is no reason to
            # fail the whole update with an "Unhandled exception" traceback.
            logger.debug("FSM state skipped for %s: %s", type(event).__name__, exc)
            return await handler()
        state = FSMContext(self.storage, key)
        data["state"] = state
        data["raw_state"] = await state.get_state()
        async with self.events_isolation.lock(key):
            return await handler()
