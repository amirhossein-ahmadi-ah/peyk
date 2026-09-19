from __future__ import annotations

import socket

import pytest


def _unused_tcp_port() -> int:
    """An OS-assigned free TCP port on 127.0.0.1 that nothing listens on.

    Binding then immediately closing (without ever calling `listen()`)
    gets us a genuinely free port. Connecting to it afterwards reliably
    yields a connection-refused error on both POSIX and Windows --
    unlike a hardcoded low/reserved port such as 1, which Windows can
    leave hanging (surfacing as a timeout) instead of refusing outright.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture
def refused_connection_url() -> str:
    """A URL nothing is listening on, for connection-refused tests."""
    return f"http://127.0.0.1:{_unused_tcp_port()}/"
