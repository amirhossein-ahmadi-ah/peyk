"""Telegram RevenueWithdrawalStateType string-domain enum."""

from enum import StrEnum


class RevenueWithdrawalStateType(StrEnum):
    """Telegram revenue-withdrawal-state discriminator values."""

    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
