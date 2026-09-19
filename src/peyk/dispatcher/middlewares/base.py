"""Base protocol for normalized-event dispatcher middleware."""
from __future__ import annotations

from typing import Awaitable, Callable, Protocol, runtime_checkable

MiddlewareHandler = Callable[..., object]
MiddlewareNext = Callable[[], Awaitable[object]]


@runtime_checkable
class BaseMiddleware(Protocol):
    """Awaitable middleware around dispatcher execution.

    Middleware receives the next callable, the normalized event, and a mutable
    context dictionary.  It may add values to ``data`` before calling ``next``;
    matching handlers receive those values as keyword arguments.
    """

    async def __call__(
        self,
        handler: MiddlewareNext,
        event: object,
        data: dict[str, object],
    ) -> object: ...
