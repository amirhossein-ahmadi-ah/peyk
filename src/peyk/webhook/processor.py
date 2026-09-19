from __future__ import annotations

import asyncio
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from peyk.bot import Bot
from peyk.platforms.bale.types import Update as BaleUpdate
from peyk.platforms.rubika.types import InlineMessage, Update as RubikaUpdate
from peyk.platforms.telegram.types import Update as TelegramUpdate

MAX_DEFAULT_BODY_SIZE: Final[int] = 4 * 1024 * 1024


@dataclass(frozen=True)
class WebhookResult:
    """HTTP result returned by a webhook processor."""

    status: int
    body: bytes | None = None


class WebhookProcessor:
    """Parse and dispatch webhook requests without depending on an HTTP server."""

    def __init__(
        self,
        dispatcher: object,
        *,
        secret: str | None = None,
        max_body_size: int = MAX_DEFAULT_BODY_SIZE,
        handle_in_background: bool = True,
        endpoint_type: str | None = None,
    ) -> None:
        self.dispatcher = dispatcher
        self.secret = secret
        self.max_body_size = max_body_size
        self.handle_in_background = handle_in_background
        self.endpoint_type = endpoint_type
        self._tasks: set[asyncio.Task[object]] = set()

    async def handle(self, bot: Bot[object], body: bytes, headers: Mapping[str, str]) -> WebhookResult:
        """Verify, parse and dispatch one webhook request.

        Malformed JSON and oversized bodies are rejected. Authentication
        failures return the same 404 used by route failures so callers cannot
        distinguish a secret oracle from an absent endpoint.
        """
        if len(body) > self.max_body_size:
            return WebhookResult(413)
        if self.secret is not None and bot.platform == "telegram":
            from .security import verify_telegram_secret_header
            if not verify_telegram_secret_header(headers, self.secret):
                return WebhookResult(404)
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
            return WebhookResult(400)
        if not isinstance(payload, dict):
            return WebhookResult(400)
        try:
            update = self._parse(bot, payload)
        except (KeyError, TypeError, ValueError):
            return WebhookResult(400)
        if update is None:
            return WebhookResult(400)
        task = asyncio.create_task(self.dispatcher.feed_raw_update(bot, update))
        if self.handle_in_background:
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
            return WebhookResult(200)
        await task
        return WebhookResult(200)

    def _parse(self, bot: Bot[object], payload: dict[str, object]) -> TelegramUpdate | BaleUpdate | RubikaUpdate | InlineMessage | None:
        if bot.platform == "telegram":
            return TelegramUpdate.from_dict(payload)
        if bot.platform == "bale":
            return BaleUpdate.from_dict(payload)
        if self.endpoint_type == "ReceiveInlineMessage":
            return InlineMessage.from_dict(payload)
        return RubikaUpdate.from_dict(payload)

    async def shutdown(self) -> None:
        """Wait for all background update tasks before server shutdown."""
        while self._tasks:
            tasks = tuple(self._tasks)
            await asyncio.gather(*tasks, return_exceptions=True)
            self._tasks.difference_update(tasks)
