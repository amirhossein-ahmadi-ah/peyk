"""Platform-neutral keyboard IR, builders, and native renderers."""
from .ir import ButtonStyle, InlineButton, ReplyButton, InlineKeyboard, ReplyKeyboard, KeyboardRemove, ForceReply
from .builder import InlineKeyboardBuilder, ReplyKeyboardBuilder, MAX_WIDTH, MAX_BUTTONS
from .rubika import *

# aiogram-compatible neutral names.
InlineKeyboardMarkup = InlineKeyboard
InlineKeyboardButton = InlineButton
ReplyKeyboardMarkup = ReplyKeyboard
KeyboardButton = ReplyButton
ReplyKeyboardRemove = KeyboardRemove

__all__ = [
    "ButtonStyle", "InlineButton", "ReplyButton", "InlineKeyboard", "ReplyKeyboard",
    "KeyboardRemove", "ForceReply", "InlineKeyboardBuilder", "ReplyKeyboardBuilder",
    "InlineKeyboardMarkup", "InlineKeyboardButton", "ReplyKeyboardMarkup", "KeyboardButton",
    "ReplyKeyboardRemove", "MAX_WIDTH", "MAX_BUTTONS",
    "Selection", "Calendar", "NumberPicker", "StringPicker", "Location", "CameraImage",
    "CameraVideo", "GalleryImage", "GalleryVideo", "File", "Audio", "RecordAudio",
    "Textbox", "Link", "AskMyPhoneNumber", "AskMyLocation", "Barcode",
]
