from enum import Enum

class UpdateDelivery(str, Enum):
    """Supported ways a platform can deliver updates."""
    POLLING = "polling"
    WEBHOOK_ONLY = "webhook_only"
    BOTH = "both"
