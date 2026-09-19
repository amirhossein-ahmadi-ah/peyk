from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from peyk.bot import Bot
from peyk.platform_core.capabilities import Feature
from peyk.platform_core.errors import UnsupportedFeatureError
from peyk.platforms.rubika.enums import UpdateEndpointTypeEnum

@dataclass(frozen=True)
class WebhookOptions:
    """Platform-neutral webhook registration options."""
    allowed_updates: list[str] | None = None
    drop_pending_updates: bool = False
    max_connections: int | None = None

class WebhookRegistrar(Protocol):
    """Register and remove a webhook for one platform."""

    async def install(self, bot: Bot[object], url: str, secret: str, options: WebhookOptions) -> None:
        """Provides the install operation for the peyk integration.

Args:
    bot: Value used by this operation.
    url: Value used by this operation.
    secret: Value used by this operation.
    options: Value used by this operation."""
        ...

    async def uninstall(self, bot: Bot[object]) -> None:
        """Provides the uninstall operation for the peyk integration.

Args:
    bot: Value used by this operation."""
        ...

class TelegramWebhookRegistrar:
    """TelegramWebhookRegistrar defines a public API type for peyk."""

    async def install(self, bot: Bot[object], url: str, secret: str, options: WebhookOptions) -> None:
        """Provides the install operation for the peyk integration.

Args:
    bot: Value used by this operation.
    url: Value used by this operation.
    secret: Value used by this operation.
    options: Value used by this operation."""
        await bot.client.set_webhook(url, max_connections=options.max_connections, allowed_updates=options.allowed_updates, drop_pending_updates=options.drop_pending_updates, secret_token=secret)

    async def uninstall(self, bot: Bot[object]) -> None:
        """Provides the uninstall operation for the peyk integration.

Args:
    bot: Value used by this operation."""
        await bot.client.delete_webhook(drop_pending_updates=False)

class BaleWebhookRegistrar:
    """BaleWebhookRegistrar defines a public API type for peyk."""

    async def install(self, bot: Bot[object], url: str, secret: str, options: WebhookOptions) -> None:
        """Provides the install operation for the peyk integration.

Args:
    bot: Value used by this operation.
    url: Value used by this operation.
    secret: Value used by this operation.
    options: Value used by this operation."""
        if options.allowed_updates is not None or options.drop_pending_updates or options.max_connections is not None:
            raise UnsupportedFeatureError(Feature.WEBHOOK, bot.platform, bot.capabilities.get(Feature.WEBHOOK))
        await bot.client.set_webhook(url)

    async def uninstall(self, bot: Bot[object]) -> None:
        """Provides the uninstall operation for the peyk integration.

Args:
    bot: Value used by this operation."""
        await bot.client.delete_webhook()

class RubikaWebhookRegistrar:
    """RubikaWebhookRegistrar defines a public API type for peyk."""

    async def install(self, bot: Bot[object], url: str, secret: str, options: WebhookOptions) -> None:
        """Provides the install operation for the peyk integration.

Args:
    bot: Value used by this operation.
    url: Value used by this operation.
    secret: Value used by this operation.
    options: Value used by this operation."""
        if options.allowed_updates is not None or options.drop_pending_updates or options.max_connections is not None:
            raise UnsupportedFeatureError(Feature.WEBHOOK, bot.platform, bot.capabilities.get(Feature.WEBHOOK))
        await bot.client.update_bot_endpoints(url, type=UpdateEndpointTypeEnum.RECEIVE_UPDATE)

    async def uninstall(self, bot: Bot[object]) -> None:
        """Provides the uninstall operation for the peyk integration.

Args:
    bot: Value used by this operation."""
        await bot.client.update_bot_endpoints('', type=UpdateEndpointTypeEnum.RECEIVE_UPDATE)

    async def install_inline(self, bot: Bot[object], url: str) -> None:
        """Provides the install inline operation for the peyk integration.

Args:
    bot: Value used by this operation.
    url: Value used by this operation."""
        await bot.client.update_bot_endpoints(url, type=UpdateEndpointTypeEnum.RECEIVE_INLINE_MESSAGE)

def registrar_for(bot: Bot[object]) -> WebhookRegistrar:
    """Return the audited registrar for ``bot.platform``."""
    if not bot.supports(Feature.WEBHOOK):
        raise UnsupportedFeatureError(Feature.WEBHOOK, bot.platform, bot.capabilities.get(Feature.WEBHOOK))
    return {'telegram': TelegramWebhookRegistrar(), 'bale': BaleWebhookRegistrar(), 'rubika': RubikaWebhookRegistrar()}[bot.platform]
