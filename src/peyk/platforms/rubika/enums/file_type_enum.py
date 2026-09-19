from __future__ import annotations

class FileTypeEnum:
    """Provide the documented Rubika constant values for ``FileTypeEnum``.

    The class preserves the existing public fields and wire-format behavior.
    """
    FILE = "File"       # up to 50 MB
    IMAGE = "Image"     # jpg/gif/png/webp, up to 10 MB
    VOICE = "Voice"     # mp3
    VIDEO = "Video"     # mp4, up to 50 MB
    MUSIC = "Music"     # mp3
    GIF = "Gif"

