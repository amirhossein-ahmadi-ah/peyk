"""Platform-neutral dispatcher event logging middleware."""
from __future__ import annotations

import logging
from typing import Awaitable, Callable

from peyk.transport.logging_hook import get_default_logger

from .base import BaseMiddleware


class LoggingMiddleware:
    """Log normalized dispatcher events without inspecting platform raw data.

    The existing transport logging hook remains the logging integration point;
    ``log_event`` is an additive hook on that same logger abstraction.
    """

    def __init__(self, logger: object | None = None) -> None:
        self._logger = logger or get_default_logger()
        self._fallback = logging.getLogger("peyk.dispatcher")

    async def __call__(
        self,
        handler: Callable[[], Awaitable[object]],
        event: object,
        data: dict[str, object],
    ) -> object:
        log_event = getattr(self._logger, "log_event", None)
        if callable(log_event):
            log_event(event)
        else:
            # Preserve compatibility with older/custom TransportLogger
            # implementations that predate the additive event hook.
            self._fallback.info("dispatcher event: %s", type(event).__name__)
        return await handler()
