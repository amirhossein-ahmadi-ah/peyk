from enum import Enum

class ChatTypeValue(str, Enum):
    """Canonical normalized chat-type values."""
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
