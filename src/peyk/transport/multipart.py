"""Helpers for building `multipart/form-data` bodies.

Thin wrapper around `aiohttp.FormData` so callers pass a plain mapping of
string fields and `FilePayload`s instead of learning `FormData`'s API
directly. File content can be raw `bytes` or a file-like/stream object
(anything `aiohttp`'s multipart writer accepts) — streams are handed to
`aiohttp` as-is rather than read fully into memory here, so a future
adapter can upload a large file without buffering the whole thing.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import IO, Mapping, Optional, Union
import aiohttp
FileContent = Union[bytes, IO[bytes]]

@dataclass(frozen=True)
class FilePayload:
    """A single file part for a multipart request.

    Attributes:
        content: Raw `bytes`, or a file-like/stream object opened in binary
            mode. Streams are not read here — they're passed through to
            `aiohttp`'s multipart writer, which reads them in chunks while
            sending.
        filename: Filename reported in the part's `Content-Disposition`.
        content_type: The part's `Content-Type`. Defaults to
            `application/octet-stream`.
    """
    content: FileContent
    filename: str
    content_type: str = 'application/octet-stream'

def build_multipart_body(fields: Optional[Mapping[str, str]]=None, files: Optional[Mapping[str, FilePayload]]=None) -> aiohttp.FormData:
    """Performs the build multipart body operation for the transport client.

Args:
    fields: Value used by this operation.
    files: Value used by this operation.

Returns:
    Result produced by the transport operation."""
    'Build an `aiohttp.FormData` body from plain fields and file payloads.\n    \n        `fields` become regular form fields (name -> string value). `files`\n        become file parts, each keyed by its multipart field name. Both `bytes`\n        and file-like/stream `FilePayload.content` values are supported and\n        passed straight to `aiohttp.FormData.add_field`, which streams\n        file-like objects rather than reading them eagerly.\n        \n    \n    Args:\n        fields: Value of the declared parameter type.\n        files: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``aiohttp.FormData``).\n    '
    form = aiohttp.FormData()
    for name, value in (fields or {}).items():
        form.add_field(name, value)
    for name, payload in (files or {}).items():
        form.add_field(name, payload.content, filename=payload.filename, content_type=payload.content_type)
    return form
