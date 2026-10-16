"""Soroush Plus (Splus) platform public API.

Splus is Telegram-shaped, so incoming updates and outgoing objects use the
Telegram models from :mod:`peyk.platforms.telegram`; only the client, the
error type and the deliverable update kinds are Splus-specific.
"""
from .client import BASE_URL, SPLUS_METHODS, SPLUS_UPDATE_TYPES, SplusClient
from .errors import SplusAPIError

__all__ = ["BASE_URL", "SPLUS_METHODS", "SPLUS_UPDATE_TYPES", "SplusAPIError", "SplusClient"]
