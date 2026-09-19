"""Bot-specific errors."""

class BotNotBoundError(RuntimeError):
    """Raised when an inbound event action is used without a bound bot."""


from peyk.transport.errors import HTTPStatusError


class InvalidTokenError(HTTPStatusError):
    """Raised when a platform rejects the configured bot token."""

    def __init__(self, platform: str, detail: str = "") -> None:
        message = f"{platform.capitalize()} rejected the token"
        if detail:
            message += f": {detail}"
        super().__init__(message, status_code=401, body=b"")
        self.platform = platform
