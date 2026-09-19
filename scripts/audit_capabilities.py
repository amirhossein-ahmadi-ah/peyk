"""Audit the declarative capability registry and generate capability reports."""
from __future__ import annotations

import argparse
import dataclasses
import importlib
import inspect
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DOCS = ROOT / "docs"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from peyk.platform_core.capabilities import (  # noqa: E402
    CAPABILITY_MATRIX, Feature, PLATFORM_SPECIFIC_METHODS, SupportLevel,
)
from peyk.platforms.bale.client import BaleClient  # noqa: E402
from peyk.platforms.telegram.client import TelegramClient  # noqa: E402
from peyk.platforms.rubika.client import RubikaClient  # noqa: E402

CLIENTS = {"telegram": TelegramClient, "bale": BaleClient, "rubika": RubikaClient}
SYMBOLS = {
    SupportLevel.FULL: "✅", SupportLevel.PARTIAL: "🟡", SupportLevel.EMULATED: "🔁",
    SupportLevel.NONE: "❌", SupportLevel.UNKNOWN: "❓",
}


def _resolve_method(ref: str) -> bool:
    if "." not in ref:
        return False
    class_name, method_name = ref.rsplit(".", 1)
    candidates = [
        "peyk.platforms.telegram.client", "peyk.platforms.bale.client", "peyk.platforms.rubika.client",
        "peyk.platforms._telegram_like.base_client",
    ]
    for module_name in candidates:
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name, None)
        if cls is not None and hasattr(cls, method_name):
            return callable(getattr(cls, method_name))
    return False


def _resolve_type_field(ref: str) -> bool:
    if "." not in ref:
        return False
    class_name, field_name = ref.rsplit(".", 1)
    class_name = class_name.rsplit(".", 1)[-1]
    modules = [
        "peyk.platforms.telegram.types", "peyk.platforms.bale.types", "peyk.platforms.rubika.types",
    ]
    for module_name in modules:
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name, None)
        if cls is not None and dataclasses.is_dataclass(cls):
            return field_name in {f.name for f in dataclasses.fields(cls)}
    return False


def _resolve_doc(ref: str) -> bool:
    return ref == "docs/decisions.md" and (ROOT / ref).is_file()


def _resolve_test(ref: str) -> bool:
    return ref.startswith("tests/") and (ROOT / ref).is_file()


def _method_names(cls: type[object]) -> set[str]:
    return {
        name for base in cls.__mro__ for name, value in base.__dict__.items()
        if not name.startswith("_") and inspect.iscoroutinefunction(value)
    }


def _button_fields(platform: str) -> set[str]:
    modules = {
        "telegram": ("peyk.platforms.telegram.types", ("InlineKeyboardButton", "KeyboardButton")),
        "bale": ("peyk.platforms.bale.types", ("InlineKeyboardButton", "KeyboardButton")),
        "rubika": ("peyk.platforms.rubika.types", ("Button", "ButtonSelection", "ButtonCalendar", "ButtonNumberPicker", "ButtonStringPicker", "ButtonLocation", "ButtonTextbox")),
    }
    module_name, classes = modules[platform]
    module = importlib.import_module(module_name)
    return {f"field:{cls.__name__}.{field.name}" for cls in [getattr(module, n) for n in classes] for field in dataclasses.fields(cls)}


def _evidence_refs():
    for platform, caps in CAPABILITY_MATRIX.platforms.items():
        for feature, support in caps.features.items():
            for kind, ref in support.evidence:
                yield platform, feature, support, kind, ref


def audit() -> list[str]:
    errors: list[str] = []
    for platform, feature, support, kind, ref in _evidence_refs():
        ok = {"method": _resolve_method, "type_field": _resolve_type_field, "doc": _resolve_doc, "test": _resolve_test}.get(kind, lambda _: False)(ref)
        if not ok:
            errors.append(f"unresolved evidence: {platform} {feature.value}: {kind} {ref}")

    for platform, caps in CAPABILITY_MATRIX.platforms.items():
        cls = CLIENTS[platform]
        mapped = {ref.rsplit(".", 1)[-1] for ev_platform, _, _, kind, ref in _evidence_refs() if ev_platform == platform and kind == "method" and "." in ref}
        specific = set(PLATFORM_SPECIFIC_METHODS[platform])
        missing = _method_names(cls) - mapped - specific
        if missing:
            errors.append(f"unmapped public coroutine methods on {platform}: {sorted(missing)}")

        fields = _button_fields(platform)
        mapped_fields = {f"field:{ref.rsplit('.',1)[0]}.{ref.rsplit('.',1)[1]}" for ev_platform, _, _, kind, ref in _evidence_refs() if ev_platform == platform and kind == "type_field"}
        missing_fields = fields - mapped_fields - specific
        if missing_fields:
            errors.append(f"unmapped keyboard-button fields on {platform}: {sorted(missing_fields)}")

        candidate_methods = {
            "messaging.venue": ("send_venue",), "messaging.poll": ("send_poll",), "messaging.dice": ("send_dice",),
            "telegram.games": ("send_game", "set_game_score", "get_game_high_scores"),
            "telegram.passport": ("set_passport_data_errors",), "telegram.business": ("get_business_connection",),
            "telegram.stories": ("post_story",), "telegram.gifts": ("send_gift", "get_available_gifts"),
            "telegram.stars": ("get_my_star_balance",),
            "keyboards.button.color_style": ("style",), "keyboards.button.icon_emoji": ("icon_custom_emoji_id",),
            "keyboards.button.request_poll": ("request_poll",), "keyboards.button.request_users": ("request_users",),
            "keyboards.button.request_chat": ("request_chat",), "keyboards.button.pay": ("pay",),
            "keyboards.button.switch_inline": ("switch_inline_query",), "keyboards.button.login_url": ("login_url",),
        }
        for feature, support in caps.features.items():
            if support.level is SupportLevel.NONE:
                # A NONE claim is allowed only if its evidence does not resolve to an implementation.
                for kind, ref in support.evidence:
                    if kind == "method" and _resolve_method(ref):
                        errors.append(f"NONE claim resolves to implementation: {platform} {feature.value}: {ref}")
                    if kind == "type_field" and _resolve_type_field(ref):
                        errors.append(f"NONE claim resolves to field: {platform} {feature.value}: {ref}")
                for candidate in candidate_methods.get(feature.value, ()):
                    if hasattr(cls, candidate):
                        errors.append(f"NONE claim has matching client attribute: {platform} {feature.value}: {candidate}")
                if feature.value.startswith("keyboards.button."):
                    for field in _button_fields(platform):
                        if field.rsplit(".", 1)[-1] in candidate_methods.get(feature.value, ()):
                            errors.append(f"NONE claim has matching keyboard field: {platform} {feature.value}: {field}")
    return errors


def generate_docs() -> tuple[str, str]:
    platforms = tuple(CAPABILITY_MATRIX.platforms)
    lines = ["# Capability matrix", "", "Generated by `scripts/audit_capabilities.py` from the audited registry.", "", "| Feature | " + " | ".join(platforms) + " |", "|---|" + "---|" * len(platforms)]
    for feature in Feature:
        cells = []
        for platform in platforms:
            support = CAPABILITY_MATRIX.for_platform(platform).get(feature)
            note = support.note.replace("|", "\\|")
            cells.append(f"{SYMBOLS[support.level]} {note}" if note else SYMBOLS[support.level])
        lines.append(f"| `{feature.value}` | " + " | ".join(cells) + " |")
    todo = ["# Capability audit TODO", "", "UNKNOWN or low-confidence items from the audited registry. Each item has a concrete live-token probe suggestion.", ""]
    for platform, caps in CAPABILITY_MATRIX.platforms.items():
        for feature, support in caps.features.items():
            if support.level is SupportLevel.UNKNOWN or support.confidence == "low":
                todo.append(f"- **{platform} / `{feature.value}`** — {support.note or 'Needs evidence.'} Probe: issue the smallest platform API request that directly exercises this feature with a live bot token and record the response schema/error.")
    todo.extend([
        "",
        "## Phase 9 webhook live probes",
        "",
        "- Rubika `GetSelectionItem` and `SearchSelectionItems` endpoint types are not registered by Peyk. Live-probe their request/response bodies before adding support.",
        "- Rubika webhook payloads are parsed only from repository-confirmed `Update` and `InlineMessage` models. A live probe should record any additional webhook event shapes before expanding the parser.",
        "- Telegram self-signed certificate upload is intentionally not exposed because the audited `set_webhook` client signature has no `certificate` parameter.",
    ])
    return "\n".join(lines) + "\n", "\n".join(todo) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = audit()
    matrix, todo = generate_docs()
    matrix_path, todo_path = DOCS / "capabilities.md", DOCS / "capabilities_todo.md"
    if args.check:
        if matrix_path.read_text(encoding="utf-8") != matrix or todo_path.read_text(encoding="utf-8") != todo:
            errors.append("generated capability docs are stale")
    else:
        matrix_path.write_text(matrix, encoding="utf-8")
        todo_path.write_text(todo, encoding="utf-8")
    print("Platform capability counts")
    for platform, caps in CAPABILITY_MATRIX.platforms.items():
        counts = {level: sum(s.level is level for s in caps.features.values()) for level in SupportLevel}
        print(platform, " ".join(f"{level.value}={counts[level]}" for level in SupportLevel))
        print("missing:", ", ".join(f.value for f in CAPABILITY_MATRIX.missing_on(platform)) or "none")
    print("unmapped methods = 0" if not any("unmapped public coroutine" in e for e in errors) else "unmapped methods > 0")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
