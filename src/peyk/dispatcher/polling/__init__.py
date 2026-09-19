from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol, TypeVar
from peyk.bot import Bot
from peyk.platform_core.capabilities import Feature
from peyk.platforms.bale.types import Update as BaleUpdate
from peyk.platforms.rubika.types import Update as RubikaUpdate
from peyk.platforms.telegram.types import Update as TelegramUpdate
RawT = TypeVar('RawT')

class Poller(Protocol[RawT]):
    """Fetch raw updates while owning the platform-specific offset."""

    async def fetch(self) -> Sequence[RawT]:
        """Performs the fetch operation for the dispatcher client.

Returns:
    Result produced by the dispatcher operation."""
        ...

class TelegramPoller:
    """TelegramPoller provides the dispatcher API surface used by peyk."""

    def __init__(self, bot: Bot[object], timeout: int, allowed_updates: Sequence[str] | None) -> None:
        self.bot = bot
        self.timeout = timeout
        self.allowed_updates = list(allowed_updates) if allowed_updates is not None else None
        self.offset: int | None = None

    async def fetch(self) -> Sequence[TelegramUpdate]:
        """Performs the fetch operation for the dispatcher client.

Returns:
    Result produced by the dispatcher operation."""
        updates = await self.bot.client.get_updates(offset=self.offset, timeout=self.timeout, allowed_updates=self.allowed_updates)
        if updates:
            self.offset = updates[-1].update_id + 1
        return updates

class BalePoller:
    """BalePoller provides the dispatcher API surface used by peyk."""

    def __init__(self, bot: Bot[object], timeout: int, allowed_updates: Sequence[str] | None) -> None:
        self.bot = bot
        self.timeout = timeout
        self.allowed_updates = allowed_updates
        self.offset: int | None = None

    async def fetch(self) -> Sequence[BaleUpdate]:
        """Performs the fetch operation for the dispatcher client.

Returns:
    Result produced by the dispatcher operation."""
        updates = await self.bot.client.get_updates(offset=self.offset, timeout=self.timeout)
        if updates:
            self.offset = updates[-1].update_id + 1
        return updates

class RubikaPoller:
    """RubikaPoller provides the dispatcher API surface used by peyk."""

    def __init__(self, bot: Bot[object], timeout: int, allowed_updates: Sequence[str] | None) -> None:
        self.bot = bot
        self.timeout = timeout
        self.allowed_updates = allowed_updates
        self.offset_id: str | None = None

    async def fetch(self) -> Sequence[RubikaUpdate]:
        """Performs the fetch operation for the dispatcher client.

Returns:
    Result produced by the dispatcher operation."""
        updates, next_offset = await self.bot.client.get_updates(offset_id=self.offset_id)
        self.offset_id = next_offset
        return updates

async def prepare_polling(bot: Bot[object], *, skip_updates: bool) -> None:
    """Clear supported webhooks before polling when requested.

    Rubika's endpoint-update parameters are intentionally not touched: the
    project decisions mark their semantics as low-confidence.
    """
    if bot.platform not in {'telegram', 'bale'}:
        return
    info = await bot.client.get_webhook_info()
    url = getattr(info, 'url', '')
    if skip_updates:
        if bot.platform == 'telegram':
            await bot.client.delete_webhook(drop_pending_updates=True)
        else:
            await bot.client.delete_webhook()
    elif url:
        if bot.platform == 'telegram':
            await bot.client.delete_webhook(drop_pending_updates=False)
        else:
            await bot.client.delete_webhook()

def make_poller(bot: Bot[object], timeout: int, allowed_updates: Sequence[str] | None) -> Poller[object]:
    """Performs the make poller operation for the dispatcher client.

Args:
    bot: Value used by this operation.
    timeout: Maximum time to wait for the operation.
    allowed_updates: Value used by this operation.

Returns:
    Result produced by the dispatcher operation."""
    if bot.platform == 'telegram':
        return TelegramPoller(bot, timeout, allowed_updates)
    if bot.platform == 'bale':
        return BalePoller(bot, timeout, allowed_updates)
    if bot.platform == 'rubika':
        return RubikaPoller(bot, timeout, allowed_updates)
    raise ValueError(f'unsupported polling platform: {bot.platform}')
__all__ = ['BalePoller', 'Poller', 'RubikaPoller', 'TelegramPoller', 'make_poller', 'prepare_polling']
