from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from peyk.platform_core.adapters import BALE_CAPABILITIES, RUBIKA_CAPABILITIES, TELEGRAM_CAPABILITIES
from peyk.platform_core.capabilities import Feature, SupportLevel, get_capabilities


def test_legacy_d1_regression_values_are_unchanged() -> None:
    assert TELEGRAM_CAPABILITIES.supports_topics is True
    assert TELEGRAM_CAPABILITIES.supports_scheduled_messages is False
    assert TELEGRAM_CAPABILITIES.update_delivery == "both"
    assert TELEGRAM_CAPABILITIES.supported_parse_modes == ["Markdown", "MarkdownV2", "HTML"]
    assert TELEGRAM_CAPABILITIES.callback_data_max_bytes == 64
    assert TELEGRAM_CAPABILITIES.supports_payments is True
    assert TELEGRAM_CAPABILITIES.supports_admin_detection is True
    assert TELEGRAM_CAPABILITIES.supports_chat_member_status_updates is True

    assert BALE_CAPABILITIES.supports_topics is False
    assert BALE_CAPABILITIES.supports_scheduled_messages is False
    assert BALE_CAPABILITIES.update_delivery == "both"
    assert BALE_CAPABILITIES.supported_parse_modes == []
    assert BALE_CAPABILITIES.callback_data_max_bytes == 64
    assert BALE_CAPABILITIES.supports_payments is True
    assert BALE_CAPABILITIES.supports_admin_detection is True
    assert BALE_CAPABILITIES.supports_chat_member_status_updates is False

    assert RUBIKA_CAPABILITIES.supports_topics is False
    assert RUBIKA_CAPABILITIES.supports_scheduled_messages is False
    assert RUBIKA_CAPABILITIES.update_delivery == "both"
    assert RUBIKA_CAPABILITIES.supported_parse_modes == []
    assert RUBIKA_CAPABILITIES.callback_data_max_bytes is None
    assert RUBIKA_CAPABILITIES.supports_payments is False
    assert RUBIKA_CAPABILITIES.supports_admin_detection is False
    assert RUBIKA_CAPABILITIES.supports_chat_member_status_updates is False


def test_registry_api_and_known_three_state_cases() -> None:
    assert get_capabilities("bale").get(Feature.POLL).level is SupportLevel.NONE
    assert get_capabilities("rubika").get(Feature.PHOTO).level is SupportLevel.EMULATED
    assert get_capabilities("rubika").get(Feature.CALLBACK_DATA_LIMIT).level is SupportLevel.UNKNOWN
    assert get_capabilities("telegram").supports(Feature.PHOTO)
    assert Feature.POLL in get_capabilities("bale").features


def test_capability_audit_check_is_clean() -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, str(root / "scripts" / "audit_capabilities.py"), "--check"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "unmapped methods = 0" in result.stdout
