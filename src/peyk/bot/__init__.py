"""Neutral bot facade and platform-specific Bot shortcuts."""
from .base import Bot, BotDefaults
from .errors import BotNotBoundError, InvalidTokenError
from .policy import UnsupportedPolicy, StyleFallback
from peyk.platforms.bale import BaleClient
from peyk.platforms.telegram import TelegramClient
from peyk.platforms.rubika import RubikaClient

class BaleBot(Bot[BaleClient]):
    """Bot facade fixed to Bale."""

    def __init__(self, token: str, **kwargs: object) -> None:
        super().__init__(token, platform='bale', **kwargs)

    @property
    def client(self) -> BaleClient:
        """Performs the client operation for the bot client.

Returns:
    Result produced by the bot operation."""
        return super().client

class TelegramBot(Bot[TelegramClient]):
    """Bot facade fixed to Telegram."""

    def __init__(self, token: str, **kwargs: object) -> None:
        super().__init__(token, platform='telegram', **kwargs)

    @property
    def client(self) -> TelegramClient:
        """Performs the client operation for the bot client.

Returns:
    Result produced by the bot operation."""
        return super().client

class RubikaBot(Bot[RubikaClient]):
    """Bot facade fixed to Rubika."""

    def __init__(self, token: str, **kwargs: object) -> None:
        super().__init__(token, platform='rubika', **kwargs)

    @property
    def client(self) -> RubikaClient:
        """Performs the client operation for the bot client.

Returns:
    Result produced by the bot operation."""
        return super().client
__all__ = ['BaleBot', 'Bot', 'BotDefaults', 'BotNotBoundError', 'InvalidTokenError', 'RubikaBot', 'TelegramBot', 'UnsupportedPolicy', 'StyleFallback']
