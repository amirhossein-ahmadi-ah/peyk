from __future__ import annotations
import asyncio
import inspect
import logging
import random
import signal
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from peyk.bot import Bot
from peyk.platforms.bale.types import Update as BaleUpdate
from peyk.platforms.rubika.types import Update as RubikaUpdate
from peyk.platforms.telegram.types import Update as TelegramUpdate
from peyk.transport.errors import HTTPStatusError, NetworkError, RateLimitedError, TimeoutError_, TransportError
from .router import Router, UNHANDLED
from peyk.fsm import FSMStrategy
from peyk.fsm.storage import BaseEventIsolation, BaseStorage
logger = logging.getLogger(__name__)
Sleep = Callable[[float], Awaitable[None]]

@dataclass(frozen=True)
class _BotRun:
    bot: Bot[object]
    poller: object

class Dispatcher(Router):
    """Root router that feeds normalized updates from one or more bots.

    The dispatcher owns polling tasks but deliberately delegates event matching
    to :class:`Router`; Phase 3 does not alter router matching semantics.
    """

    def __init__(self, *, name: str | None=None, storage: BaseStorage | None=None, fsm_strategy: FSMStrategy | str=FSMStrategy.USER_IN_CHAT, events_isolation: BaseEventIsolation | None=None, **workflow_data: object) -> None:
        super().__init__(name=name or 'dispatcher')
        from peyk.fsm import MemoryStorage, SimpleEventIsolation
        from peyk.fsm.middleware import FSMContextMiddleware
        self.storage: BaseStorage = storage if storage is not None else MemoryStorage()
        if not isinstance(fsm_strategy, (FSMStrategy, str)):
            raise TypeError('fsm_strategy must be an FSMStrategy value')
        isolation = events_isolation or SimpleEventIsolation()
        if fsm_strategy not in {FSMStrategy.USER_IN_CHAT, FSMStrategy.CHAT, FSMStrategy.GLOBAL_USER}:
            raise ValueError(f'unsupported FSM strategy: {fsm_strategy}')
        self.fsm_strategy = fsm_strategy
        self.events_isolation: BaseEventIsolation = isolation
        self.fsm = FSMContextMiddleware(self.storage, strategy=fsm_strategy, events_isolation=isolation)
        self.middleware(self.fsm)
        from peyk.dispatcher.middlewares import CallbackAnswerMiddleware, ChatActionMiddleware
        self.handler_middleware(ChatActionMiddleware())
        self.handler_middleware(CallbackAnswerMiddleware())
        self.workflow_data: dict[str, object] = dict(workflow_data)
        self._startup_observers: list[Callable[[], Awaitable[None] | None]] = []
        self._shutdown_observers: list[Callable[[], Awaitable[None] | None]] = []
        self._polling_stop = asyncio.Event()
        self._polling_tasks: set[asyncio.Task[None]] = set()
        self._handler_tasks: set[asyncio.Task[object]] = set()
        self._bots: list[Bot[object]] = []
        self._closed_bots: set[int] = set()

    def __getitem__(self, key: str) -> object:
        return self.workflow_data[key]

    def __setitem__(self, key: str, value: object) -> None:
        self.workflow_data[key] = value

    async def _emit_recursive(self, kind: str) -> None:
        await self._emit_lifecycle(kind)

    def resolve_used_update_types(self) -> list[str]:
        """Return the Telegram update types this dispatcher should receive.

        Telegram *remembers* the ``allowed_updates`` last sent for a bot token,
        whether it came from ``getUpdates``, from ``setWebhook`` or from a
        completely different program that used the same token earlier. If a
        new run does not send the parameter, the old filter silently stays in
        effect, so e.g. ``callback_query`` and ``inline_query`` updates never
        arrive even though the handlers are registered. Peyk therefore always
        sends an explicit list.

        The list contains every update type Peyk can parse, except the three
        opt-in types Telegram does not deliver by default (``chat_member``,
        ``message_reaction`` and ``message_reaction_count``); those are added
        only when a router in the tree has a handler that needs them.

        Returns:
            Update type names in Telegram's ``allowed_updates`` spelling.
        """
        opt_in = {'chat_member', 'message_reaction', 'message_reaction_count'}
        routers: list[Router] = []
        stack: list[Router] = [self]
        while stack:
            router = stack.pop()
            routers.append(router)
            stack.extend(router._children)
        wanted: set[str] = set()
        for router in routers:
            if router.platform_event.handlers:
                wanted |= opt_in
            if router.chat_member_status_update.handlers:
                wanted.add('chat_member')
            for name in opt_in:
                observer = router._telegram_observers.get(name)
                if observer is not None and observer.handlers:
                    wanted.add(name)
        return [name for name in TelegramUpdate.__dataclass_fields__ if name != 'update_id' and (name not in opt_in or name in wanted)]

    async def feed_raw_update(self, bot: Bot[object], raw_update: object) -> object:
        """Normalize one raw update, inject dispatcher context, and propagate it."""
        await bot.me()
        event = bot.normalize_update(raw_update)
        data: dict[str, object] = dict(self.workflow_data)
        data.update({'bot': bot, 'dispatcher': self})
        from_user = getattr(event, 'from_user', None)
        chat = getattr(event, 'chat', None)
        if from_user is not None:
            data['event_from_user'] = from_user
        if chat is not None:
            data['event_chat'] = chat
        platform_result = await self.propagate_platform_event(raw_update, platform=bot.platform, **data)
        if platform_result is not UNHANDLED:
            return platform_result
        return await self._propagate_with_data(event, data)

    async def _propagate_with_data(self, event: object, data: dict[str, object]) -> object:
        return await self.propagate_event(event, **data)

    def _warn_unsupported_observers(self, bot: Bot[object]) -> None:
        """Warn once when registered Telegram-native observers cannot receive updates on a bot."""
        if bot.platform == 'telegram':
            return
        names = [name for name, observer in self._telegram_observers.items() if observer.handlers]
        if names:
            logger.warning('%s does not deliver Telegram-native update observers: %s', bot.platform, ', '.join(sorted(names)))
        if self.edited_message.handlers or self.channel_post.handlers or self.edited_channel_post.handlers:
            if bot.platform == 'rubika':
                logger.warning('rubika does not expose Telegram channel-post update kinds in the audited model; registered neutral observers will not fire: %s', ', '.join((name for name, obs in (('edited_message', self.edited_message), ('channel_post', self.channel_post), ('edited_channel_post', self.edited_channel_post)) if obs.handlers)))

    async def start_polling(self, *bots: Bot[object], polling_timeout: int=30, allowed_updates: Sequence[str] | None=None, skip_updates: bool=False, handle_signals: bool=True, close_bots: bool=True, handle_as_tasks: bool=False, max_concurrent_updates: int=100) -> None:
        """Poll all supplied bots concurrently until stopped or cancelled."""
        if not bots:
            raise ValueError('start_polling() requires at least one bot')
        if max_concurrent_updates < 1:
            raise ValueError('max_concurrent_updates must be positive')
        from .polling import make_poller, prepare_polling
        self._polling_stop.clear()
        self._bots = list(bots)
        semaphore = asyncio.Semaphore(max_concurrent_updates)
        loop = asyncio.get_running_loop()
        installed: list[signal.Signals] = []

        def request_stop() -> None:
            """Performs the request stop operation for the dispatcher client."""
            self._polling_stop.set()
        if handle_signals:
            for sig in (signal.SIGINT, signal.SIGTERM):
                try:
                    loop.add_signal_handler(sig, request_stop)
                    installed.append(sig)
                except (NotImplementedError, RuntimeError):
                    continue
        await self._emit_recursive('startup')
        try:
            runs: list[_BotRun] = []
            for bot in bots:
                self._warn_unsupported_observers(bot)
                await bot.me()
                await prepare_polling(bot, skip_updates=skip_updates)
                bot_allowed_updates = allowed_updates
                if bot_allowed_updates is None and bot.platform == 'telegram':
                    bot_allowed_updates = self.resolve_used_update_types()
                    logger.info('telegram polling with allowed_updates=%s', bot_allowed_updates)
                runs.append(_BotRun(bot, make_poller(bot, polling_timeout, bot_allowed_updates)))

            async def run_one(run: _BotRun) -> None:
                """Performs the run one operation for the dispatcher client.

Args:
    run: Value used by this operation."""
                await _poll_bot(self, run.bot, run.poller, semaphore, handle_as_tasks, self._polling_stop)
            self._polling_tasks = {asyncio.create_task(run_one(run), name=f'peyk-poll-{run.bot.platform}') for run in runs}
            done, pending = await asyncio.wait(self._polling_tasks, return_when=asyncio.FIRST_EXCEPTION)
            for task in done:
                exception = task.exception()
                if exception is not None:
                    logger.exception('polling task stopped with an error', exc_info=exception)
                    self._polling_stop.set()
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
        finally:
            self._polling_stop.set()
            if self._polling_tasks:
                await asyncio.gather(*self._polling_tasks, return_exceptions=True)
            if self._handler_tasks:
                await asyncio.gather(*tuple(self._handler_tasks), return_exceptions=True)
            await self._emit_recursive('shutdown')
            for sig in installed:
                try:
                    loop.remove_signal_handler(sig)
                except (NotImplementedError, RuntimeError):
                    pass
            if close_bots:
                for bot in bots:
                    if id(bot) not in self._closed_bots:
                        await bot.close()
                        self._closed_bots.add(id(bot))

    def run_polling(self, *bots: Bot[object], **kwargs: object) -> None:
        """Run :meth:`start_polling` through ``asyncio.run``."""
        asyncio.run(self.start_polling(*bots, **kwargs))

    async def start_webhook(self, *bots: Bot[object], base_url: str, host: str='0.0.0.0', port: int=8080, path_prefix: str='/webhook', secrets: Sequence[str] | None=None, ssl_context: object | None=None, allowed_updates: Sequence[str] | None=None, drop_pending_updates: bool=False, manage_registration: bool=True, delete_on_shutdown: bool=False, max_connections: int | None=None, handle_in_background: bool=True) -> None:
        """Serve Telegram, Bale and Rubika webhooks from one aiohttp app.

        Each bot receives a non-token URL of ``{path_prefix}/{platform}/{secret}``.
        Rubika's confirmed inline endpoint is registered at the additional
        ``/inline`` path.
        """
        if not bots:
            raise ValueError('start_webhook() requires at least one bot')
        if secrets is not None and len(secrets) != len(bots):
            raise ValueError('secrets must contain exactly one entry per bot')
        from aiohttp import web
        import secrets as secrets_module
        from peyk.webhook.aiohttp_server import MultiBotRequestHandler, SimpleRequestHandler, _RouteEntry, setup_application
        from peyk.webhook.processor import MAX_DEFAULT_BODY_SIZE
        from peyk.webhook.registrars import RubikaWebhookRegistrar, WebhookOptions, registrar_for
        prefix = '/' + path_prefix.strip('/')
        origin = base_url.rstrip('/')
        app = web.Application()
        entries: dict[str, _RouteEntry] = {}
        registrations: list[tuple[object, Bot[object]]] = []
        self._bots = list(bots)
        generated: list[str] = []
        for index, bot in enumerate(bots):
            self._warn_unsupported_observers(bot)
            await bot.me()
            secret = secrets[index] if secrets is not None else secrets_module.token_urlsafe(32)
            generated.append(secret)
            key = f'{bot.platform}/{secret}'
            normal_path = f'{prefix}/{bot.platform}/{secret}'
            handler = SimpleRequestHandler(self, bot, normal_path, secret, handle_in_background=handle_in_background)
            inline_handler = None
            if bot.platform == 'rubika':
                inline_handler = SimpleRequestHandler(self, bot, f'{normal_path}/inline', secret, handle_in_background=handle_in_background, endpoint_type='ReceiveInlineMessage')
            entries[key] = _RouteEntry(handler, inline_handler)
            if manage_registration:
                registrar = registrar_for(bot)
                if allowed_updates is not None:
                    bot_allowed_updates = list(allowed_updates)
                elif bot.platform == 'telegram':
                    bot_allowed_updates = self.resolve_used_update_types()
                else:
                    bot_allowed_updates = None
                options = WebhookOptions(allowed_updates=bot_allowed_updates, drop_pending_updates=drop_pending_updates, max_connections=max_connections)
                await registrar.install(bot, f'{origin}{normal_path}', secret, options)
                if bot.platform == 'rubika':
                    await registrar.install_inline(bot, f'{origin}{normal_path}/inline')
                registrations.append((registrar, bot))
        router_handler = MultiBotRequestHandler(entries)
        app.router.add_route('*', f'{prefix}/{{platform}}/{{key}}', router_handler)
        setup_application(app, self)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port, ssl_context=ssl_context)
        await site.start()
        try:
            await asyncio.Event().wait()
        finally:
            await router_handler.shutdown()
            if manage_registration and delete_on_shutdown:
                for registrar, bot in registrations:
                    await registrar.uninstall(bot)
            await runner.cleanup()
            for bot in bots:
                await bot.close()

    def run_webhook(self, *bots: Bot[object], **kwargs: object) -> None:
        """Run :meth:`start_webhook` through ``asyncio.run`` for Windows-safe automation."""
        asyncio.run(self.start_webhook(*bots, **kwargs))

    async def stop_polling(self) -> None:
        """Request graceful polling shutdown after the current batch."""
        self._polling_stop.set()

async def _poll_bot(dispatcher: Dispatcher, bot: Bot[object], poller: object, semaphore: asyncio.Semaphore, handle_as_tasks: bool, stop: asyncio.Event) -> None:
    from .polling import Poller
    delay = 0.5
    while not stop.is_set():
        try:
            updates = await poller.fetch()
            delay = 0.5
            for raw in updates:
                if stop.is_set():
                    break
                if handle_as_tasks:
                    task = asyncio.create_task(_handle_one(dispatcher, bot, raw, semaphore))
                    dispatcher._handler_tasks.add(task)
                    task.add_done_callback(dispatcher._handler_tasks.discard)
                else:
                    await dispatcher.feed_raw_update(bot, raw)
        except RateLimitedError as exc:
            await _sleep_or_stop(stop, max(0.0, exc.retry_after_seconds or delay))
        except (NetworkError, TimeoutError_, OSError) as exc:
            logger.warning('%s polling network error: %s', bot.platform, exc)
            await _sleep_or_stop(stop, _jitter(delay))
            delay = min(delay * 2, 30.0)
        except HTTPStatusError as exc:
            if exc.status_code in {401, 403}:
                logger.error('%s polling stopped: authentication/authorization failed', bot.platform)
                return
            logger.warning('%s polling HTTP error %s', bot.platform, exc.status_code)
            await _sleep_or_stop(stop, _jitter(delay))
            delay = min(delay * 2, 30.0)
        except TransportError as exc:
            if _looks_like_auth_error(exc):
                logger.error('%s polling stopped: authentication failed: %s', bot.platform, exc)
                return
            logger.exception('%s polling transport error', bot.platform)
            await _sleep_or_stop(stop, _jitter(delay))
            delay = min(delay * 2, 30.0)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception('%s polling failed unexpectedly', bot.platform)
            await _sleep_or_stop(stop, _jitter(delay))
            delay = min(delay * 2, 30.0)

async def _handle_one(dispatcher: Dispatcher, bot: Bot[object], raw: object, semaphore: asyncio.Semaphore) -> None:
    async with semaphore:
        await dispatcher.feed_raw_update(bot, raw)

async def _sleep_or_stop(stop: asyncio.Event, seconds: float) -> None:
    if seconds <= 0:
        return
    try:
        await asyncio.wait_for(stop.wait(), timeout=seconds)
    except asyncio.TimeoutError:
        return

def _jitter(delay: float) -> float:
    return delay * (0.5 + random.random() * 0.5)

def _looks_like_auth_error(exc: BaseException) -> bool:
    for attr in ('error_code', 'status_code'):
        value = getattr(exc, attr, None)
        if value in {401, 403, '401', '403'}:
            return True
    return False
