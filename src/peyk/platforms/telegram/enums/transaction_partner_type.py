"""Telegram TransactionPartnerType string-domain enum."""

from enum import StrEnum


class TransactionPartnerType(StrEnum):
    """Telegram transaction-partner discriminator values."""

    USER = "user"
    FRAGMENT = "fragment"
    TELEGRAM_ADS = "telegram_ads"
    OTHER = "other"
    AFFILIATE_PROGRAM = "affiliate_program"
    CHAT = "chat"
    TELEGRAM_API = "telegram_api"
