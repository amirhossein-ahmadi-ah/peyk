from __future__ import annotations
import warnings
warnings.warn("peyk.dispatcher.filters is deprecated; use peyk.filters", DeprecationWarning, stacklevel=2)
from peyk.filters import *  # noqa: F401,F403
from peyk.filters import F, BaseFilter, Command, CommandStart, CommandObject, CallbackData, ChatTypeFilter, StateFilter, MagicData, ExceptionTypeFilter, ExceptionMessageFilter, PlatformFilter, SupportsFilter, TextEquals, TextContains
from peyk.filters.callback_data import CallbackDataEquals, CallbackDataStartsWith
__all__ = ["F", "BaseFilter", "Command", "CommandStart", "CommandObject", "CallbackData", "ChatTypeFilter", "ChatType", "StateFilter", "MagicData", "ExceptionTypeFilter", "ExceptionMessageFilter", "PlatformFilter", "SupportsFilter", "TextEquals", "TextContains", "CallbackDataEquals", "CallbackDataStartsWith"]
