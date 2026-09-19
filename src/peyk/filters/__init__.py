"""Aiogram-style platform-neutral filters."""
from magic_filter import MagicFilter
F = MagicFilter()
from .base import BaseFilter, and_f, or_f, invert_f, normalize_filter
from .command import Command, CommandStart, CommandObject
from .callback_data import CallbackData, CallbackDataEquals, CallbackDataStartsWith
from .chat_type import ChatTypeFilter, ChatType
from .state import StateFilter
from .magic_data import MagicData
from .exception import ExceptionTypeFilter, ExceptionMessageFilter
from .platform import PlatformFilter, SupportsFilter
from .text import TextEquals, TextContains

__all__ = ["F", "BaseFilter", "and_f", "or_f", "invert_f", "normalize_filter", "Command", "CommandStart", "CommandObject", "CallbackData", "CallbackDataEquals", "CallbackDataStartsWith", "ChatTypeFilter", "ChatType", "StateFilter", "MagicData", "ExceptionTypeFilter", "ExceptionMessageFilter", "PlatformFilter", "SupportsFilter", "TextEquals", "TextContains"]
