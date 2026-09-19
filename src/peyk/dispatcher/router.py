from __future__ import annotations
import inspect
import logging
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass, field
from typing import Generic, ParamSpec, TypeVar
from .event.bases import ErrorEvent, SkipHandler, UNHANDLED
from .middlewares.base import BaseMiddleware
from peyk.filters import BaseFilter, normalize_filter
from peyk.platform_core.contracts import IncomingBotMembershipChange, IncomingCallbackQuery, IncomingChatMemberStatusUpdate, IncomingMessage, IncomingMessageDeleted, IncomingPreCheckoutQuery, IncomingShippingQuery
logger = logging.getLogger(__name__)
Handler = Callable[..., object]
P = ParamSpec('P')
R = TypeVar('R')

@dataclass(frozen=True)
class _Handler:
    callback: Handler
    filters: tuple[BaseFilter, ...] = field(default_factory=tuple)
    flags: dict[str, object] = field(default_factory=dict)

class Observer:
    """Handler collection for one event type, with filters and middleware."""

    def __init__(self, router: Router, name: str) -> None:
        self.router, self.name = (router, name)
        self.handlers: list[_Handler] = []
        self._filters: list[BaseFilter] = []
        self._inner: list[BaseMiddleware] = []
        self._outer: list[BaseMiddleware] = []

    def __call__(self, *filters: object) -> Callable[[Callable[P, R]], Callable[P, R]]:
        normalized = tuple((normalize_filter(f) for f in filters))

        def decorator(handler: Callable[P, R]) -> Callable[P, R]:
            self.register(handler, *normalized)
            return handler
        return decorator

    def register(self, handler: Callable[P, R], *filters: object) -> Callable[P, R]:
        """Performs the register operation for the dispatcher client.

Args:
    handler: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        if not callable(handler):
            raise TypeError('handler must be callable')
        self.handlers.append(_Handler(handler, tuple((normalize_filter(f) for f in filters)), dict(getattr(handler, '__peyk_flags__', {}))))
        return handler

    def filter(self, *filters: object) -> Observer:
        """Performs the filter operation for the dispatcher client.

Returns:
    Result produced by the dispatcher operation."""
        self._filters.extend((normalize_filter(f) for f in filters))
        return self

    def middleware(self, middleware: BaseMiddleware) -> BaseMiddleware:
        """Performs the middleware operation for the dispatcher client.

Args:
    middleware: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        self._inner.append(middleware)
        return middleware

    def outer_middleware(self, middleware: BaseMiddleware) -> BaseMiddleware:
        """Performs the outer middleware operation for the dispatcher client.

Args:
    middleware: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        self._outer.append(middleware)
        return middleware

    async def _matches_observer(self, event: object, data: dict[str, object]) -> tuple[bool, dict[str, object]]:
        merged = dict(data)
        for filter_ in self._filters:
            result = await filter_(event, **merged)
            if not result:
                return (False, merged)
            if isinstance(result, dict):
                merged.update(result)
        return (True, merged)

class Router:
    """Aiogram-style first-match router with nested ordered subrouters."""

    def __init__(self, *, name: str | None=None) -> None:
        self.name = name or 'router'
        self.message = Observer(self, 'message')
        self.edited_message = Observer(self, 'edited_message')
        self.channel_post = Observer(self, 'channel_post')
        self.edited_channel_post = Observer(self, 'edited_channel_post')
        self.platform_event = Observer(self, 'platform_event')
        self.callback_query = Observer(self, 'callback_query')
        self.chat_member_status_update = Observer(self, 'chat_member_status_update')
        self.bot_membership = Observer(self, 'bot_membership')
        self.message_deleted = Observer(self, 'message_deleted')
        self.pre_checkout_query = Observer(self, 'pre_checkout_query')
        self.shipping_query = Observer(self, 'shipping_query')
        self.errors = Observer(self, 'errors')
        self.startup = _LifecycleObserver(self, 'startup')
        self.shutdown = _LifecycleObserver(self, 'shutdown')
        self._message = self.message.handlers
        self._edited_message = self.edited_message.handlers
        self._channel_post = self.channel_post.handlers
        self._edited_channel_post = self.edited_channel_post.handlers
        self._callback_query = self.callback_query.handlers
        self._chat_member_status_update = self.chat_member_status_update.handlers
        self._bot_membership = self.bot_membership.handlers
        self._message_deleted = self.message_deleted.handlers
        self._pre_checkout_query = self.pre_checkout_query.handlers
        self._shipping_query = self.shipping_query.handlers
        self._platform_event = self.platform_event.handlers
        self._telegram_observers: dict[str, Observer] = {}
        for _name in ('inline_query', 'chosen_inline_result', 'poll', 'poll_answer', 'chat_join_request', 'message_reaction', 'message_reaction_count', 'chat_boost', 'removed_chat_boost', 'business_connection', 'business_message', 'edited_business_message', 'deleted_business_messages', 'purchased_paid_media', 'callback_query', 'shipping_query', 'pre_checkout_query', 'message', 'edited_message', 'channel_post', 'edited_channel_post', 'my_chat_member', 'chat_member', 'managed_bot', 'subscription', 'stopped_message_generation'):
            if _name not in {'message', 'edited_message', 'channel_post', 'edited_channel_post', 'callback_query', 'shipping_query', 'pre_checkout_query'}:
                self._telegram_observers[_name] = Observer(self, _name)
                setattr(self, _name, self._telegram_observers[_name])
        self._children: list[Router] = []
        self._middlewares: list[BaseMiddleware] = []
        self._handler_middlewares: list[BaseMiddleware] = []

    def command(self, *names: str, prefix: str='/') -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Register a message handler for one or more bot commands.

        This is shorthand for ``router.message(Command(name, prefix=prefix))``
        and is available on :class:`Router`, :class:`Dispatcher` and (through
        :meth:`Bot.command`) on the bot's own router. Each alias is registered
        independently, so all of them share the same Python callable::

            @router.command("start", "help")
            async def start(message): ...
        """
        if not names:
            raise ValueError('command() requires at least one name')
        from peyk.filters.command import Command
        filters = tuple((Command(name, prefix=prefix) for name in names))

        def decorator(handler: Callable[P, R]) -> Callable[P, R]:
            for command_filter in filters:
                self.message(command_filter)(handler)
            return handler
        return decorator

    def include_router(self, router: Router) -> Router:
        """Performs the include router operation for the dispatcher client.

Args:
    router: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        if not isinstance(router, Router):
            raise TypeError('include_router() expects a Router')
        if router is self:
            raise ValueError('a router cannot include itself')
        if router._contains(self):
            raise ValueError('including this router would create a cycle')
        if router not in self._children:
            self._children.append(router)
        return router

    def _contains(self, target: Router, seen: set[int] | None=None) -> bool:
        if self is target:
            return True
        seen = seen or set()
        if id(self) in seen:
            return False
        seen.add(id(self))
        return any((child._contains(target, seen) for child in self._children))

    def middleware(self, middleware: BaseMiddleware) -> BaseMiddleware:
        """Register outer whole-subtree middleware, preserving the D3 API."""
        if not callable(middleware):
            raise TypeError('middleware must be callable')
        self._middlewares.append(middleware)
        return middleware

    def handler_middleware(self, middleware: BaseMiddleware) -> BaseMiddleware:
        """Register middleware that runs after handler flags have been injected."""
        if not callable(middleware):
            raise TypeError('middleware must be callable')
        self._handler_middlewares.append(middleware)
        return middleware

    def has_handlers(self) -> bool:
        """Performs the has handlers operation for the dispatcher client.

Returns:
    Result produced by the dispatcher operation."""
        return any((obs.handlers for obs in self._event_observers())) or any((obs.handlers for obs in self._telegram_observers.values())) or any((c.has_handlers() for c in self._children))

    def _event_observers(self) -> tuple[Observer, ...]:
        return (self.message, self.edited_message, self.channel_post, self.edited_channel_post, self.callback_query, self.chat_member_status_update, self.bot_membership, self.message_deleted, self.pre_checkout_query, self.shipping_query, self.platform_event)

    def _observer_for(self, event: object) -> Observer | None:
        if isinstance(event, IncomingMessage):
            kind = getattr(event, 'update_kind', 'message')
            if kind == 'edited_message':
                return self.edited_message
            if kind == 'channel_post':
                return self.channel_post
            if kind == 'edited_channel_post':
                return self.edited_channel_post
            if kind == 'message':
                return self.message
            return None
        if isinstance(event, IncomingCallbackQuery):
            return self.callback_query
        if isinstance(event, IncomingChatMemberStatusUpdate):
            return self.chat_member_status_update
        if isinstance(event, IncomingBotMembershipChange):
            return self.bot_membership
        if isinstance(event, IncomingMessageDeleted):
            return self.message_deleted
        if isinstance(event, IncomingPreCheckoutQuery):
            return self.pre_checkout_query
        if isinstance(event, IncomingShippingQuery):
            return self.shipping_query
        return None

    async def _run_middleware(self, middlewares: tuple[BaseMiddleware, ...], terminal: Callable[[], Awaitable[object]], event: object, data: dict[str, object]) -> object:
        if not middlewares:
            return await terminal()
        index = 0

        async def call_next() -> object:
            nonlocal index
            current = index
            index += 1
            if current >= len(middlewares):
                return await terminal()
            result = middlewares[current](call_next, event, data)
            return await result if inspect.isawaitable(result) else result
        return await call_next()

    async def _call_handler(self, handler: Handler, event: object, data: dict[str, object]) -> object:
        try:
            sig = inspect.signature(handler)
        except (TypeError, ValueError):
            return await _maybe_await(handler(event))
        accepts_kwargs = any((p.kind is inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()))
        names = {n for n, p in sig.parameters.items() if p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)}
        kwargs = data if accepts_kwargs else {k: v for k, v in data.items() if k in names}
        return await _maybe_await(handler(event, **kwargs))

    async def _run_handler(self, observer: Observer, item: _Handler, event: object, data: dict[str, object]) -> object:
        merged = dict(data)
        merged['handler'] = item.callback
        merged['flags'] = dict(item.flags)
        for filter_ in item.filters:
            result = await filter_(event, **merged)
            if not result:
                return UNHANDLED
            if isinstance(result, dict):
                merged.update(result)

        async def terminal() -> object:
            return await self._call_handler(item.callback, event, merged)
        return await self._run_middleware(tuple(observer._inner) + tuple(self._handler_middlewares), terminal, event, merged)

    async def _dispatch_observer(self, observer: Observer, event: object, data: dict[str, object]) -> object:
        matched, merged = await observer._matches_observer(event, data)
        if not matched:
            return UNHANDLED

        async def terminal() -> object:
            for item in tuple(observer.handlers):
                try:
                    result = await self._run_handler(observer, item, event, merged)
                except SkipHandler:
                    continue
                except Exception as exc:
                    if observer is self.errors:
                        logger.exception('error observer failed in router %s', self.name, exc_info=exc)
                    else:
                        await self._dispatch_error(event, exc, merged)
                    return UNHANDLED
                if result is not UNHANDLED:
                    return result
            return UNHANDLED
        try:
            return await self._run_middleware(tuple(observer._outer), terminal, event, merged)
        except Exception as exc:
            if observer is self.errors:
                logger.exception('error observer middleware failed in router %s', self.name, exc_info=exc)
                return UNHANDLED
            await self._dispatch_error(event, exc, merged)
            return UNHANDLED

    async def _dispatch_error(self, event: object, exc: Exception, data: dict[str, object]) -> object:
        error_event = ErrorEvent(event, exc)
        result = await self._dispatch_observer(self.errors, error_event, data)
        if result is UNHANDLED:
            logger.exception('Unhandled exception in router %s', self.name, exc_info=exc)
        return result

    async def _dispatch(self, event: object, data: dict[str, object]) -> object:
        observer = self._observer_for(event)
        if observer is not None:
            result = await self._dispatch_observer(observer, event, data)
            if result is not UNHANDLED:
                return result
        for child in tuple(self._children):
            result = await child._dispatch(event, dict(data))
            if result is not UNHANDLED:
                return result
        return UNHANDLED

    async def propagate_platform_event(self, update: object, *, platform: str, **data: object) -> object:
        """Dispatch a native platform update and its named Telegram field observer.

        ``platform_event`` receives the complete native update object. For
        Telegram, a named observer receives the native model stored in the
        corresponding ``Update`` field; other platforms currently have no
        named-native observer surface.
        """
        merged = dict(data)
        merged['platform'] = platform
        result = await self._dispatch_observer(self.platform_event, update, merged)
        if result is not UNHANDLED:
            return result
        if platform == 'telegram':
            fields = getattr(update, '__dataclass_fields__', {})
            for name in fields:
                if name == 'update_id':
                    continue
                value = getattr(update, name, None)
                if value is None:
                    continue
                observer = self._telegram_observers.get(name)
                if observer is None:
                    continue
                bound = value
                bot = merged.get('bot')
                if bot is not None and hasattr(bound, 'bot'):
                    try:
                        setattr(bound, 'bot', bot)
                    except (AttributeError, TypeError):
                        pass
                result = await self._dispatch_observer(observer, bound, merged)
                if result is not UNHANDLED:
                    return result
        for child in tuple(self._children):
            result = await child.propagate_platform_event(update, platform=platform, **dict(data))
            if result is not UNHANDLED:
                return result
        return UNHANDLED

    async def propagate_event(self, event: object, **data: object) -> object:
        """Dispatch one event using first-match-wins semantics."""

        async def terminal() -> object:
            """Performs the terminal operation for the dispatcher client.

Returns:
    Result produced by the dispatcher operation."""
            result = await self._dispatch(event, data)
            if result is UNHANDLED:
                logger.debug('Update is not handled by router %s', self.name)
            return result
        try:
            return await self._run_middleware(tuple(self._middlewares), terminal, event, data)
        except Exception as exc:
            await self._dispatch_error(event, exc, data)
            return UNHANDLED

    async def _emit_lifecycle(self, kind: str) -> None:
        observer = self.startup if kind == 'startup' else self.shutdown
        await observer.emit()
        for child in tuple(self._children):
            await child._emit_lifecycle(kind)

class _LifecycleObserver:

    def __init__(self, router: Router, name: str) -> None:
        self.router, self.name, self.handlers = (router, name, [])

    def __call__(self, callback: Callable[P, R] | None=None) -> Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]:
        if callback is not None:
            self.handlers.append(callback)
            return callback

        def decorator(handler: Callable[P, R]) -> Callable[P, R]:
            self.handlers.append(handler)
            return handler
        return decorator

    def register(self, handler: Callable[P, R]) -> Callable[P, R]:
        """Performs the register operation for the dispatcher client.

Args:
    handler: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
        self.handlers.append(handler)
        return handler

    async def emit(self) -> None:
        """Performs the emit operation for the dispatcher client."""
        for handler in tuple(self.handlers):
            try:
                await _maybe_await(handler())
            except Exception as exc:
                logger.exception('router %s observer failed', self.name, exc_info=exc)

async def _maybe_await(value: object) -> object:
    if inspect.isawaitable(value):
        return await value
    return value
