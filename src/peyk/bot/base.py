"""Platform-neutral Bot facade for Phase 2."""
from __future__ import annotations
import asyncio
import logging
import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable, Callable, Generic, Literal, Optional, ParamSpec, Protocol, Sequence, TypeVar, Union, cast
from peyk.platform_core.capabilities import CapabilitySet, Feature, SupportLevel, get_capabilities
from peyk.platform_core.errors import UnsupportedFeatureError
from peyk.platform_core.contracts import IncomingBotMembershipChange, IncomingChatMemberStatusUpdate, IncomingMessageDeleted, IncomingPreCheckoutQuery, IncomingShippingQuery
from peyk.platforms.bale.types import Update as BaleUpdate
from peyk.platforms.rubika.types import Update as RubikaUpdate, InlineMessage
from peyk.platforms.bale.types import WebhookInfo as BaleWebhookInfo
from peyk.platforms.telegram.types import WebhookInfo as TelegramWebhookInfo
from peyk.platforms.telegram.types import Update as TelegramUpdate
from peyk.platform_core.adapters import bale as bale_adapter, rubika as rubika_adapter, telegram as telegram_adapter
from peyk.transport import RetryPolicy, Session
from peyk.types import CallbackQuery, Chat, ChatMember, File, Message, User
from peyk.utils.keyboard_builder import KeyboardBuilder
from peyk.keyboard import InlineKeyboard, ReplyKeyboard, KeyboardRemove, ForceReply, InlineKeyboardBuilder, ReplyKeyboardBuilder
from peyk.bot.policy import UnsupportedPolicy, StyleFallback
from peyk.bot.errors import BotNotBoundError, InvalidTokenError
from peyk.formatting import Text, resolve_text
from peyk.platform_core.contracts import PlatformCapabilities
from peyk.platform_core.enums import ParseMode
from peyk.bot import strategies
if TYPE_CHECKING:
    from peyk.filters.base import BaseFilter
    from peyk.dispatcher.router import Router

class ClientLifecycle(Protocol):
    """ClientLifecycle provides the bot API surface used by peyk."""

    async def close(self) -> None:
        """Performs the close operation for the bot client."""
        ...
ClientT = TypeVar('ClientT', bound=ClientLifecycle, covariant=True)
HandlerP = ParamSpec('HandlerP')
HandlerR = TypeVar('HandlerR')
Handler = Callable[HandlerP, HandlerR]
StartupCallback = Callable[[], Awaitable[None] | None]
PlatformLiteral = Literal['bale', 'telegram', 'rubika']
PlatformUpdate = Union[TelegramUpdate, BaleUpdate, RubikaUpdate, InlineMessage]
NormalizedEvent = Union[Message, CallbackQuery, IncomingChatMemberStatusUpdate, IncomingPreCheckoutQuery, IncomingShippingQuery, IncomingMessageDeleted, IncomingBotMembershipChange, TelegramUpdate, BaleUpdate, RubikaUpdate]

@dataclass(frozen=True)
class BotDefaults:
    """Defaults applied only when the active capability registry confirms them."""
    parse_mode: ParseMode | str | None = None
    link_preview: Optional[bool] = None
    protect_content: Optional[bool] = None
    style_fallback: StyleFallback = StyleFallback.NONE

class Bot(Generic[ClientT]):
    """Unified async bot facade over one audited platform client.

    Example:
        .. code-block:: python

            bot = Bot("TOKEN", platform="telegram")

            @bot.command("start")
            async def start(message):
                await bot.send_message(message.chat.id, "Hello")

            bot.run()
    """

    def __init__(self, token: str, *, platform: PlatformLiteral, defaults: Optional[BotDefaults]=None, on_unsupported: UnsupportedPolicy=UnsupportedPolicy.DEFAULT, session: Optional[Session]=None, retry_policy: Optional[RetryPolicy]=None, logger: Optional[logging.Logger]=None, base_url: Optional[str]=None) -> None:
        self.platform: PlatformLiteral = platform
        self.capabilities: CapabilitySet = get_capabilities(platform)
        self.defaults = defaults or BotDefaults()
        self.on_unsupported = on_unsupported
        self._warned: set[tuple[str, Feature]] = set()
        self._me: Optional[User] = None
        self._client_cls = {'telegram': strategies.TELEGRAM_CLIENT, 'bale': strategies.BALE_CLIENT, 'rubika': strategies.RUBIKA_CLIENT}[platform]
        self._token = token
        self._session = session
        self._retry_policy = retry_policy
        self._client_logger = logger
        self._base_url = base_url
        self._client: ClientT | None = None
        from peyk.dispatcher.router import Router
        self.router: Router = Router(name=f'{platform}_bot')
        self._logger = logger or logging.getLogger(f'peyk.bot.{platform}')

    @property
    def client(self) -> ClientT:
        """Return the lazily-created raw platform client."""
        if self._client is None:
            self._client = cast(ClientT, self._client_cls(self._token, self._session, retry_policy=self._retry_policy, logger=self._client_logger, base_url=self._base_url))
        return self._client

    @property
    def token(self) -> str:
        """Return the bot token this bot was created with (read-only)."""
        return self._token

    def supports(self, feature: Feature) -> bool:
        """Return whether the audited capability is usable."""
        return self.capabilities.supports(feature)

    def __getattr__(self, name: str) -> object:
        """Fall back to the raw platform client for platform-specific operations.

        The neutral surface defined above this point only wraps the handful
        of methods that make sense across Telegram, Bale *and* Rubika at
        once. Everything else the audited client for the active platform
        exposes (Telegram gifts/stories/business/passport, Bale sticker-set
        management, Rubika-only calls, ...) is reached transparently through
        ``bot.<method>(...)`` instead of forcing ``bot.client.<method>(...)``
        for those. Python only calls ``__getattr__`` once normal attribute
        lookup (instance dict, then the class and its bases) has already
        failed, so this never shadows a method defined above - it only fills
        in names the neutral facade does not define itself.

        A name that does not exist on the active platform's client still
        raises a plain ``AttributeError`` naming the platform, so a typo or
        a genuinely wrong-platform call fails immediately and clearly rather
        than resolving to ``None``.
        """
        if name.startswith('_') or name in {'client', 'platform'}:
            raise AttributeError(name)
        client = self.client
        attr = getattr(client, name, None)
        if attr is None or not callable(attr):
            raise AttributeError(f"'{type(self).__name__}' has no attribute {name!r} on platform {self.platform!r}")
        return attr

    async def __aenter__(self) -> 'Bot[ClientT]':
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying client/session when it has been initialized."""
        if self._client is not None:
            await self._client.close()

    async def set_webhook(self, url: str, *, max_connections: int | None=None, allowed_updates: Sequence[str] | None=None, drop_pending_updates: bool | None=None, secret_token: str | None=None) -> bool:
        """Set the platform webhook after checking its audited capabilities.

        ``secret_token`` is enforceable by Telegram only. Bale and Rubika use
        the framework-level path secret instead and therefore reject this
        platform-specific option rather than silently ignoring it.
        """
        if not self.supports(Feature.WEBHOOK):
            raise UnsupportedFeatureError(Feature.WEBHOOK, self.platform, self.capabilities.get(Feature.WEBHOOK))
        if secret_token is not None and self.platform != 'telegram':
            raise UnsupportedFeatureError(Feature.WEBHOOK_SECRET_HEADER, self.platform, self.capabilities.get(Feature.WEBHOOK_SECRET_HEADER))
        if self.platform == 'telegram':
            return await self.client.set_webhook(url, max_connections=max_connections, allowed_updates=list(allowed_updates) if allowed_updates is not None else None, drop_pending_updates=drop_pending_updates, secret_token=secret_token)
        if max_connections is not None or allowed_updates is not None or drop_pending_updates is not None:
            raise UnsupportedFeatureError(Feature.WEBHOOK, self.platform, self.capabilities.get(Feature.WEBHOOK))
        if self.platform == 'bale':
            return await self.client.set_webhook(url)
        return await self.client.update_bot_endpoints(url)

    async def delete_webhook(self, *, drop_pending_updates: bool | None=None) -> bool:
        """Remove the configured webhook when the platform exposes that operation."""
        if not self.supports(Feature.WEBHOOK):
            raise UnsupportedFeatureError(Feature.WEBHOOK, self.platform, self.capabilities.get(Feature.WEBHOOK))
        if self.platform == 'telegram':
            return await self.client.delete_webhook(drop_pending_updates=drop_pending_updates)
        if self.platform == 'bale':
            if drop_pending_updates is not None:
                raise UnsupportedFeatureError(Feature.WEBHOOK, self.platform, self.capabilities.get(Feature.WEBHOOK))
            return await self.client.delete_webhook()
        return await self.client.update_bot_endpoints('', type='ReceiveUpdate')

    async def get_webhook_info(self) -> TelegramWebhookInfo | BaleWebhookInfo:
        """Return the native webhook-info model where the platform exposes it."""
        if self.platform not in {'telegram', 'bale'}:
            raise UnsupportedFeatureError(Feature.WEBHOOK, self.platform, self.capabilities.get(Feature.WEBHOOK))
        return await self.client.get_webhook_info()

    async def me(self) -> User:
        """Fetch and cache the neutral authenticated bot identity."""
        if self._me is None:
            self._me = await strategies.get_me(self)
        return self._me

    @property
    def id(self) -> int | str:
        """Return the authenticated bot ID after :meth:`me` has been fetched."""
        if self._me is None:
            raise BotNotBoundError('Bot identity is unavailable; call await bot.me() first.')
        return self._me.id

    def normalize_update(self, raw: PlatformUpdate) -> NormalizedEvent:
        """Normalize a raw platform update and bind supported events to this bot."""
        if self.platform == 'rubika' and isinstance(raw, InlineMessage):
            return cast(NormalizedEvent, self._bind(rubika_adapter.normalize_inline_message(raw)))
        adapter = cast(Callable[[PlatformUpdate], NormalizedEvent], {'telegram': telegram_adapter.normalize_update, 'bale': bale_adapter.normalize_update, 'rubika': rubika_adapter.normalize_update}[self.platform])
        return cast(NormalizedEvent, self._bind(adapter(raw)))

    def _bind(self, value: NormalizedEvent) -> NormalizedEvent:
        if isinstance(value, Message):
            return Message(**{name: getattr(value, name) for name in value.__dataclass_fields__ if name != 'bot'}, bot=self)
        if isinstance(value, CallbackQuery):
            message = self._bind(value.message) if value.message is not None else None
            return CallbackQuery(**{name: getattr(value, name) for name in value.__dataclass_fields__ if name not in {'bot', 'message'}}, message=cast(Optional[Message], message), bot=self)
        return value

    def command(self, *names: str, prefix: str='/') -> Callable[[Handler[HandlerP, HandlerR]], Handler[HandlerP, HandlerR]]:
        """Register one handler for one or more command names.

        Each alias is registered independently so all aliases share the exact
        original Python callable and its type signature. This delegates to
        :meth:`peyk.dispatcher.router.Router.command` on the bot's router.
        """
        return self.router.command(*names, prefix=prefix)

    def message(self, *filters: object) -> Callable[[Handler[HandlerP, HandlerR]], Handler[HandlerP, HandlerR]]:
        """Register a message handler on the bot's plain router."""

        def decorator(handler: Handler[HandlerP, HandlerR]) -> Handler[HandlerP, HandlerR]:
            """Performs the decorator operation for the bot client.

Args:
    handler: Value used by this operation.

Returns:
    Result produced by the bot operation."""
            self.router.message(*filters)(handler)
            return handler
        return decorator

    def callback_query(self, *filters: object) -> Callable[[Handler[HandlerP, HandlerR]], Handler[HandlerP, HandlerR]]:
        """Register a callback-query handler on the bot's plain router."""

        def decorator(handler: Handler[HandlerP, HandlerR]) -> Handler[HandlerP, HandlerR]:
            """Performs the decorator operation for the bot client.

Args:
    handler: Value used by this operation.

Returns:
    Result produced by the bot operation."""
            self.router.callback_query(*filters)(handler)
            return handler
        return decorator

    def callback(self, data: str, *, prefix: bool=False) -> Callable[[Handler[HandlerP, HandlerR]], Handler[HandlerP, HandlerR]]:
        """Register a callback handler for exact data or a data prefix."""
        from peyk.filters.callback_data import CallbackDataEquals, CallbackDataStartsWith
        predicate = CallbackDataStartsWith(data) if prefix else CallbackDataEquals(data)
        return self.callback_query(predicate)

    def on_startup(self, callback: StartupCallback) -> StartupCallback:
        """Register a startup callback using the bare-decorator form."""
        return self.router.startup()(callback)

    def on_shutdown(self, callback: StartupCallback) -> StartupCallback:
        """Register a shutdown callback using the bare-decorator form."""
        return self.router.shutdown()(callback)

    def include_router(self, router: 'Router') -> 'Router':
        """Include another router in the bot's router tree."""
        return self.router.include_router(router)

    def _has_handlers(self) -> bool:
        """Return whether this bot router subtree contains registered handlers."""
        return self.router.has_handlers()

    async def run_async(self, **polling_options: object) -> None:
        """Validate the token, log startup, and run automatic polling asynchronously."""
        try:
            me = await self.me()
        except Exception as exc:
            if _is_invalid_token(exc):
                raise InvalidTokenError(self.platform, str(exc)) from exc
            raise
        name = me.username or me.first_name or str(me.id)
        self._logger.info('Bot @%s started on %s (polling)', name, self.platform.capitalize())
        if not self._has_handlers():
            self._logger.warning('No handlers registered for bot on %s', self.platform)
        from peyk.dispatcher import Dispatcher
        dispatcher = Dispatcher(name=f'{self.platform}_simple')
        dispatcher.include_router(self.router)
        await dispatcher.start_polling(self, **polling_options)

    def run(self, **polling_options: object) -> None:
        """Run this bot's router with automatic polling in a blocking call."""
        asyncio.run(self.run_async(**polling_options))

    def _unsupported(self, feature: Feature, *, cosmetic: bool=False) -> bool:
        support = self.capabilities.get(feature)
        if support.level not in {SupportLevel.NONE, SupportLevel.UNKNOWN}:
            return True
        if not cosmetic or self.on_unsupported is UnsupportedPolicy.RAISE:
            raise UnsupportedFeatureError(feature, self.platform, support)
        if self.on_unsupported is UnsupportedPolicy.STRIP:
            return False
        if (self.platform, feature) not in self._warned:
            warnings.warn(f'{feature.value} is {support.level.value} on {self.platform}; degrading this operation.', RuntimeWarning, stacklevel=3)
            self._warned.add((self.platform, feature))
        return False

    def _resolve_markup(self, reply_markup: object | None) -> object | None:
        """Render neutral keyboard IR against this bot's platform at send time."""
        if reply_markup is None:
            return None
        if isinstance(reply_markup, KeyboardBuilder):
            return reply_markup.build(self.capabilities)
        if isinstance(reply_markup, InlineKeyboardBuilder | ReplyKeyboardBuilder):
            reply_markup = reply_markup.as_markup()
        from peyk.keyboard.render import telegram, bale, rubika
        if isinstance(reply_markup, InlineKeyboard):
            return {'telegram': telegram.inline_keyboard, 'bale': bale.inline_keyboard, 'rubika': rubika.inline_keyboard}[self.platform](reply_markup, self.capabilities, (self.on_unsupported, self.defaults.style_fallback))
        if isinstance(reply_markup, ReplyKeyboard):
            return {'telegram': telegram.reply_keyboard, 'bale': bale.reply_keyboard, 'rubika': rubika.reply_keyboard}[self.platform](reply_markup, self.capabilities, (self.on_unsupported, self.defaults.style_fallback))
        if isinstance(reply_markup, KeyboardRemove):
            return {'telegram': telegram.remove_keyboard, 'bale': bale.remove_keyboard, 'rubika': rubika.remove_keyboard}[self.platform](reply_markup, self.capabilities, (self.on_unsupported, self.defaults.style_fallback))
        if isinstance(reply_markup, ForceReply):
            return {'telegram': telegram.force_reply, 'bale': bale.force_reply, 'rubika': rubika.force_reply}[self.platform](reply_markup, self.capabilities, (self.on_unsupported, self.defaults.style_fallback))
        return reply_markup

    def _send_kwargs(self, kwargs: dict[str, object]) -> dict[str, object]:
        result = dict(kwargs)
        if self.defaults.link_preview is not None and self.capabilities.supports(Feature.LINK_PREVIEW_CONTROL):
            result.setdefault('link_preview_options', {'is_disabled': not self.defaults.link_preview})
        if self.defaults.protect_content is not None and self.capabilities.supports(Feature.PROTECT_CONTENT):
            result.setdefault('protect_content', self.defaults.protect_content)
        if 'reply_markup' in result:
            result['reply_markup'] = self._resolve_markup(result['reply_markup'])
        return result

    def _text_caps(self) -> PlatformCapabilities:
        from peyk.platform_core.capabilities.legacy import legacy_capabilities
        return legacy_capabilities(self.platform)

    def _parse_mode_or_degrade(self, value: object | None) -> str | None:
        if value is None:
            return None
        mode = value.value if isinstance(value, ParseMode) else str(value)
        supported = {item.lower() for item in self._text_caps().supported_parse_modes}
        if mode.lower() in supported:
            return mode
        if self.on_unsupported is UnsupportedPolicy.RAISE:
            raise UnsupportedFeatureError(Feature.ENTITIES_FORMATTING, self.platform, self.capabilities.get(Feature.ENTITIES_FORMATTING))
        key = (self.platform, Feature.ENTITIES_FORMATTING)
        if key not in self._warned:
            warnings.warn(f'parse_mode is not supported on {self.platform}; sending unparsed text.', RuntimeWarning, stacklevel=3)
            self._warned.add(key)
        return None

    def _resolve_content(self, content: str | 'RichText' | Text, *, explicit_parse_mode: object | None=None) -> dict[str, object]:
        mode = self.defaults.parse_mode
        if explicit_parse_mode is not None:
            mode = self._parse_mode_or_degrade(explicit_parse_mode)
        elif mode is not None:
            mode = self._parse_mode_or_degrade(mode)
        defaults = BotDefaults(parse_mode=mode, link_preview=self.defaults.link_preview, protect_content=self.defaults.protect_content, style_fallback=self.defaults.style_fallback)
        text, native = resolve_text(content, self._text_caps(), self.on_unsupported, defaults)
        if explicit_parse_mode is not None and mode is None:
            native.pop('parse_mode', None)
        elif explicit_parse_mode is not None and mode is not None:
            native['parse_mode'] = mode
        return {'text': text, **native}

    @staticmethod
    def _pop_caption(kwargs: dict[str, object]) -> tuple[object | None, dict[str, object]]:
        result = dict(kwargs)
        return (result.pop('caption', None), result)

    def _resolve_caption(self, caption: object | None, kwargs: dict[str, object]) -> dict[str, object]:
        if caption is None:
            return kwargs
        if not isinstance(caption, (str, Text)):
            from peyk.utils.text_formatting import RichText
            if not isinstance(caption, RichText):
                raise TypeError('caption must be str, RichText, or Text')
        explicit = kwargs.pop('parse_mode', None)
        resolved = self._resolve_content(caption, explicit_parse_mode=explicit)
        kwargs['caption'] = resolved.pop('text')
        if 'parse_mode' in resolved:
            kwargs['parse_mode'] = resolved['parse_mode']
        if 'metadata' in resolved:
            if self.platform == 'rubika':
                if self.on_unsupported is UnsupportedPolicy.RAISE:
                    raise UnsupportedFeatureError(Feature.ENTITIES_FORMATTING, self.platform, self.capabilities.get(Feature.ENTITIES_FORMATTING))
                key = (self.platform, Feature.ENTITIES_FORMATTING)
                if key not in self._warned:
                    warnings.warn('Rubika media captions have no confirmed metadata parameter; sending plain caption text.', RuntimeWarning, stacklevel=3)
                    self._warned.add(key)
            else:
                kwargs['metadata'] = resolved['metadata']
        return kwargs

    async def send_message(self, chat_id: int | str, text: str | 'RichText' | Text, *, reply_to_message_id: int | str | None=None, reply_markup: object | None=None, parse_mode: ParseMode | str | None=None, **kwargs: object) -> Message:
        """Send plain or composable text and resolve formatting for the active platform."""
        self._unsupported(Feature.TEXT)
        args = self._send_kwargs(kwargs)
        resolved = self._resolve_content(text, explicit_parse_mode=parse_mode)
        args.update({key: value for key, value in resolved.items() if key != 'text'})
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = self._resolve_markup(reply_markup)
        return await strategies.send_message(self, chat_id, resolved['text'], **args)

    async def send_photo(self, chat_id: int | str, photo: object, *, caption: str | 'RichText' | Text | None=None, parse_mode: ParseMode | str | None=None, **kwargs: object) -> Message:
        """Sends photo through the bot API.

Args:
    chat_id: Identifier of the target chat.
    photo: Photo input supplied to the operation.
    caption: Value used by this operation.
    parse_mode: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.PHOTO)
        args = self._send_kwargs(kwargs)
        if caption is not None:
            args = self._resolve_caption(caption, args | ({'parse_mode': parse_mode} if parse_mode is not None else {}))
        return await strategies.send_photo(self, chat_id, photo, **args)

    async def send_video(self, chat_id: int | str, video: object, *, caption: str | 'RichText' | Text | None=None, parse_mode: ParseMode | str | None=None, **kwargs: object) -> Message:
        """Sends video through the bot API.

Args:
    chat_id: Identifier of the target chat.
    video: Video input supplied to the operation.
    caption: Value used by this operation.
    parse_mode: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.VIDEO)
        args = self._send_kwargs(kwargs)
        if caption is not None:
            args = self._resolve_caption(caption, args | ({'parse_mode': parse_mode} if parse_mode is not None else {}))
        return await strategies.send_video(self, chat_id, video, **args)

    async def send_audio(self, chat_id: int | str, audio: object, *, caption: str | 'RichText' | Text | None=None, parse_mode: ParseMode | str | None=None, **kwargs: object) -> Message:
        """Sends audio through the bot API.

Args:
    chat_id: Identifier of the target chat.
    audio: Audio input supplied to the operation.
    caption: Value used by this operation.
    parse_mode: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.AUDIO)
        args = self._send_kwargs(kwargs)
        if caption is not None:
            args = self._resolve_caption(caption, args | ({'parse_mode': parse_mode} if parse_mode is not None else {}))
        return await strategies.send_audio(self, chat_id, audio, **args)

    async def send_voice(self, chat_id: int | str, voice: object, *, caption: str | 'RichText' | Text | None=None, parse_mode: ParseMode | str | None=None, **kwargs: object) -> Message:
        """Sends voice through the bot API.

Args:
    chat_id: Identifier of the target chat.
    voice: Voice input supplied to the operation.
    caption: Value used by this operation.
    parse_mode: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.VOICE)
        args = self._send_kwargs(kwargs)
        if caption is not None:
            args = self._resolve_caption(caption, args | ({'parse_mode': parse_mode} if parse_mode is not None else {}))
        return await strategies.send_voice(self, chat_id, voice, **args)

    async def send_document(self, chat_id: int | str, document: object, *, caption: str | 'RichText' | Text | None=None, parse_mode: ParseMode | str | None=None, **kwargs: object) -> Message:
        """Sends document through the bot API.

Args:
    chat_id: Identifier of the target chat.
    document: Document input supplied to the operation.
    caption: Value used by this operation.
    parse_mode: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.DOCUMENT)
        args = self._send_kwargs(kwargs)
        if caption is not None:
            args = self._resolve_caption(caption, args | ({'parse_mode': parse_mode} if parse_mode is not None else {}))
        return await strategies.send_document(self, chat_id, document, **args)

    async def edit_message_text(self, chat_id: int | str, message_id: int | str, text: str | 'RichText' | Text, *, parse_mode: ParseMode | str | None=None, **kwargs: object) -> Message:
        """Edits message text through the bot API.

Args:
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.
    text: Text content supplied to the operation.
    parse_mode: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.EDIT_TEXT)
        args = self._send_kwargs(kwargs)
        resolved = self._resolve_content(text, explicit_parse_mode=parse_mode)
        if self.platform == 'rubika' and 'metadata' in resolved:
            if self.on_unsupported is UnsupportedPolicy.RAISE:
                raise UnsupportedFeatureError(Feature.EDIT_TEXT, self.platform, self.capabilities.get(Feature.EDIT_TEXT))
            key = (self.platform, Feature.EDIT_TEXT)
            if key not in self._warned:
                warnings.warn('Rubika message edits do not accept metadata; sending plain text.', RuntimeWarning, stacklevel=2)
                self._warned.add(key)
            resolved.pop('metadata', None)
        args.update({key: value for key, value in resolved.items() if key != 'text'})
        return await strategies.edit_message_text(self, chat_id, message_id, resolved['text'], **args)

    async def send_contact(self, chat_id: int | str, phone_number: str, first_name: str, **kwargs: object) -> Message:
        """Sends contact through the bot API.

Args:
    chat_id: Identifier of the target chat.
    phone_number: Value used by this operation.
    first_name: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.CONTACT)
        return await strategies.send_contact(self, chat_id, phone_number, first_name, **kwargs)

    async def send_location(self, chat_id: int | str, latitude: float, longitude: float, **kwargs: object) -> Message:
        """Sends location through the bot API.

Args:
    chat_id: Identifier of the target chat.
    latitude: Value used by this operation.
    longitude: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.LOCATION)
        return await strategies.send_location(self, chat_id, latitude, longitude, **kwargs)

    async def send_poll(self, chat_id: int | str, question: str, options: Sequence[str], **kwargs: object) -> Message:
        """Sends poll through the bot API.

Args:
    chat_id: Identifier of the target chat.
    question: Value used by this operation.
    options: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.POLL)
        return await strategies.send_poll(self, chat_id, question, options, **kwargs)

    async def edit_message_reply_markup(self, chat_id: int | str, message_id: int | str, **kwargs: object) -> Message:
        """Edits message reply markup through the bot API.

Args:
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.EDIT_MARKUP)
        return await strategies.edit_message_reply_markup(self, chat_id, message_id, **kwargs)

    async def delete_message(self, chat_id: int | str, message_id: int | str) -> bool:
        """Removes message through the bot API.

Args:
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.DELETE)
        return await strategies.delete_message(self, chat_id, message_id)

    async def forward_message(self, chat_id: int | str, from_chat_id: int | str, message_id: int | str) -> Message:
        """Performs the forward message operation for the bot client.

Args:
    chat_id: Identifier of the target chat.
    from_chat_id: Value used by this operation.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.FORWARD)
        return await strategies.forward_message(self, chat_id, from_chat_id, message_id)

    async def send_media_group(self, chat_id: int | str, media: Sequence[object], **kwargs: object) -> list[Message]:
        """Send a media group when the active platform advertises album support."""
        self._unsupported(Feature.MEDIA_GROUP)
        return await strategies.send_media_group(self, chat_id, media, **kwargs)

    async def answer_callback_query(self, callback_query_id: str, *, text: Optional[str]=None, show_alert: bool=False) -> bool:
        """Answers the callback query request through the bot API.

Args:
    callback_query_id: Identifier of the callback query.
    text: Text content supplied to the operation.
    show_alert: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        if not self._unsupported(Feature.CALLBACK_ANSWER, cosmetic=True):
            return False
        if show_alert and (not self.capabilities.supports(Feature.CALLBACK_ALERT_TOAST)):
            self._unsupported(Feature.CALLBACK_ALERT_TOAST, cosmetic=True)
            show_alert = False
        return await strategies.answer_callback_query(self, callback_query_id, text=text, show_alert=show_alert)

    async def _unsupported_callback_answer(self, *, text: Optional[str], show_alert: bool) -> bool:
        self._unsupported(Feature.CALLBACK_ANSWER, cosmetic=True)
        return False

    async def send_chat_action(self, chat_id: int | str, action: str) -> bool:
        """Sends chat action through the bot API.

Args:
    chat_id: Identifier of the target chat.
    action: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.CHAT_ACTIONS)
        return await strategies.send_chat_action(self, chat_id, action)

    async def get_chat(self, chat_id: int | str) -> Chat:
        """Retrieves chat from the bot API.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.TITLE, cosmetic=True) if False else None
        return await strategies.get_chat(self, chat_id)

    async def get_chat_member(self, chat_id: int | str, user_id: int) -> ChatMember:
        """Retrieves chat member from the bot API.

Args:
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
        return await strategies.get_chat_member(self, chat_id, user_id)

    async def get_chat_administrators(self, chat_id: int | str) -> list[ChatMember]:
        """Retrieves the list of chat administrators through the bot API.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.ADMINISTRATORS)
        return await strategies.get_chat_administrators(self, chat_id)
    get_chat_admins = get_chat_administrators

    async def ban_chat_member(self, chat_id: int | str, user_id: int) -> bool:
        """Performs the ban chat member operation for the bot client.

Args:
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.BAN)
        return await strategies.ban_chat_member(self, chat_id, user_id)

    async def unban_chat_member(self, chat_id: int | str, user_id: int) -> bool:
        """Performs the unban chat member operation for the bot client.

Args:
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
        self._unsupported(Feature.UNBAN)
        return await strategies.unban_chat_member(self, chat_id, user_id)

    async def create_chat_invite_link(self, chat_id: int | str, *, name: str | None=None, expire_date: int | None=None, member_limit: int | None=None, creates_join_request: bool | None=None) -> str:
        """Create an invite link for a chat and return its URL.

        ``name``, ``expire_date``, ``member_limit`` and ``creates_join_request``
        are enforceable by Telegram only. Bale's ``createChatInviteLink`` takes
        just the chat ID, so those options are rejected there rather than
        silently ignored. The bot must be an administrator of the chat.

        Example:
            .. code-block:: python

                link = await bot.create_chat_invite_link(chat_id)
        """
        self._unsupported(Feature.INVITE_LINKS)
        if self.platform == 'telegram':
            created = await self.client.create_chat_invite_link(chat_id, name=name, expire_date=expire_date, member_limit=member_limit, creates_join_request=creates_join_request)
            return created.invite_link
        if name is not None or expire_date is not None or member_limit is not None or creates_join_request is not None:
            raise UnsupportedFeatureError(Feature.INVITE_LINKS, self.platform, self.capabilities.get(Feature.INVITE_LINKS))
        result = await self.client.create_chat_invite_link(chat_id)
        return _invite_link_url(result)

    async def get_file(self, file_id: str) -> File:
        """Return a neutral file descriptor."""
        self._unsupported(Feature.GET_FILE)
        return await strategies.get_file(self, file_id)

    async def download(self, file_id: str) -> bytes:
        """Download file bytes using the platform-specific file descriptor/URL."""
        self._unsupported(Feature.GET_FILE)
        return await strategies.download(self, file_id)

def _invite_link_url(result: object) -> str:
    """Extract the invite URL from Bale's ``{"invite_link": ...}`` (or bare string) result."""
    if isinstance(result, dict):
        link = result.get('invite_link')
        if isinstance(link, str) and link:
            return link
    elif isinstance(result, str) and result:
        return result
    raise ValueError(f'Unexpected invite link response: {result!r}')

def _is_invalid_token(exc: BaseException) -> bool:
    """Recognize the audited HTTP authentication failure shape."""
    from peyk.transport.errors import HTTPStatusError
    if isinstance(exc, HTTPStatusError) and exc.status_code in {401, 403}:
        return True
    code = getattr(exc, 'error_code', None)
    description = str(getattr(exc, 'description', '')).lower()
    return code in {401, '401'} or description in {'unauthorized', 'invalid token', 'invalid bot token'}
