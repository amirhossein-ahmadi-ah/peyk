from __future__ import annotations
import asyncio
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Awaitable, Callable
from aiohttp import web
from peyk.bot import Bot
from peyk.dispatcher.dispatcher import Dispatcher
from .processor import MAX_DEFAULT_BODY_SIZE, WebhookProcessor
from .security import IPFilter

class SimpleRequestHandler:
    """Serve one bot at one exact webhook path."""

    def __init__(self, dispatcher: Dispatcher, bot: Bot[object], path: str, secret: str | None=None, *, max_body_size: int=MAX_DEFAULT_BODY_SIZE, handle_in_background: bool=True, ip_filter: IPFilter | None=None, endpoint_type: str | None=None) -> None:
        self.path = path.rstrip('/') or '/'
        self.bot = bot
        self.ip_filter = ip_filter
        self.processor = WebhookProcessor(dispatcher, secret=secret, max_body_size=max_body_size, handle_in_background=handle_in_background, endpoint_type=endpoint_type)

    async def __call__(self, request: web.Request) -> web.StreamResponse:
        if request.path.rstrip('/') != self.path.rstrip('/'):
            raise web.HTTPNotFound()
        if self.ip_filter is not None:
            peer = request.remote or ''
            if not self.ip_filter.allows(peer, request.headers):
                raise web.HTTPNotFound()
        if request.content_length is not None and request.content_length > self.processor.max_body_size:
            raise web.HTTPRequestEntityTooLarge(max_size=self.processor.max_body_size, actual_size=request.content_length)
        body = await request.read()
        result = await self.processor.handle(self.bot, body, request.headers)
        return web.Response(status=result.status, body=result.body)

    async def shutdown(self) -> None:
        """Provides the shutdown operation for the peyk integration."""
        await self.processor.shutdown()

@dataclass
class _RouteEntry:
    handler: SimpleRequestHandler
    inline_handler: SimpleRequestHandler | None = None

class MultiBotRequestHandler:
    """Route multiple bots by ``{platform}/{key}`` without exposing bot tokens."""

    def __init__(self, entries: Mapping[str, _RouteEntry]) -> None:
        self.entries = dict(entries)

    async def __call__(self, request: web.Request) -> web.StreamResponse:
        parts = request.path.strip('/').split('/')
        if len(parts) < 2:
            raise web.HTTPNotFound()
        key = '/'.join(parts[:2])
        entry = self.entries.get(key)
        if entry is None:
            raise web.HTTPNotFound()
        if len(parts) == 3 and entry.inline_handler is not None and (parts[2] == 'inline'):
            return await entry.inline_handler(request)
        if len(parts) != 2:
            raise web.HTTPNotFound()
        return await entry.handler(request)

    async def shutdown(self) -> None:
        """Provides the shutdown operation for the peyk integration."""
        await asyncio.gather(*(entry.handler.shutdown() for entry in self.entries.values()))
        await asyncio.gather(*(entry.inline_handler.shutdown() for entry in self.entries.values() if entry.inline_handler is not None))

def setup_application(app: web.Application, dispatcher: Dispatcher, **workflow_data: object) -> web.Application:
    """Attach dispatcher lifecycle hooks and shared workflow data to an app."""
    dispatcher.workflow_data.update(workflow_data)

    async def startup(_: web.Application) -> None:
        await dispatcher._emit_recursive('startup')

    async def shutdown(_: web.Application) -> None:
        await dispatcher._emit_recursive('shutdown')
    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)
    return app
