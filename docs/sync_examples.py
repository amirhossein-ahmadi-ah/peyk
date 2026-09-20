#!/usr/bin/env python3
"""مثال‌های صفحه‌ی اصلی (mainpage.html) را از فایل‌های واقعی پوشه‌ی examples/ می‌خواند.

فقط بین دو مارکر زیر در mainpage.html را بازنویسی می‌کند:

    /* EXAMPLES:START ... */
    /* EXAMPLES:END */

اجرا (از ریشه‌ی پروژه):

    uv run python docs/sync_examples.py           # به‌روزرسانی
    uv run python docs/sync_examples.py --check   # فقط بررسی (برای CI)

اگر بخواهی فقط بخشی از یک فایل در صفحه بیاید، داخل همان فایل بنویس:

    # landing:start
    ...
    # landing:end
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

# ── این لیست را ویرایش کن: (id, برچسب تب, فایل داخل examples/) ─────────────
EXAMPLES: list[tuple[str, str, str]] = [
    ("echo", "echo", "echo_bot.py"),
    ("router", "router", "dispatcher_router.py"),
    ("callbacks", "callbacks", "callback_data.py"),
    ("fsm", "FSM", "finite_state_machine.py"),
    ("multi", "multi-platform", "multi_platform.py"),
    ("webhook", "webhook", "webhook.py"),
]

MAX_LINES = 40  # بیشتر از این باشد هشدار می‌دهد (مثال‌ها باید کوتاه بمانند)
START_TAG, END_TAG = "# landing:start", "# landing:end"
BLOCK_RE = re.compile(r"(/\* EXAMPLES:START.*?\*/)(.*?)(/\* EXAMPLES:END \*/)", re.DOTALL)


def find_root() -> Path:
    p = Path(__file__).resolve().parent
    while not (p / "pyproject.toml").exists() and p.parent != p:
        p = p.parent
    return p


def find_html(root: Path) -> Path:
    for p in sorted(root.rglob("mainpage.html")):
        if not {"_build", "node_modules", ".venv"} & set(p.parts):
            return p
    sys.exit("mainpage.html پیدا نشد؛ با --html مسیرش را بده.")


def load_snippet(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    idx = {i for i, ln in enumerate(lines) if ln.strip() in (START_TAG, END_TAG)}
    if idx:
        starts = [i for i in idx if lines[i].strip() == START_TAG]
        ends = [i for i in idx if lines[i].strip() == END_TAG]
        if len(starts) != 1 or len(ends) != 1 or starts[0] > ends[0]:
            sys.exit(f"{path.name}: مارکرهای landing:start / landing:end درست نیستند.")
        lines = lines[starts[0] + 1 : ends[0]]
    code = textwrap.dedent("\n".join(lines)).strip("\n").rstrip()
    if code.count("\n") + 1 > MAX_LINES:
        print(
            f"هشدار: {path.name} بیش از {MAX_LINES} خط است؛ "
            f"با {START_TAG} / {END_TAG} کوتاهش کن.",
            file=sys.stderr,
        )
    return code


def js_string(s: str) -> str:
    out = json.dumps(s, ensure_ascii=False)
    # "<" را escape می‌کنیم تا "</script>" یا "<!--" داخل کد، صفحه را نشکند
    return out.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def build_block(examples_dir: Path) -> str:
    items = []
    for ex_id, label, filename in EXAMPLES:
        src = examples_dir / filename
        if not src.is_file():
            have = ", ".join(sorted(f.name for f in examples_dir.glob("*.py"))) or "(هیچ فایل .py نیست)"
            sys.exit(f"فایل مثال پیدا نشد: {filename} | فایل‌های موجود در {examples_dir}: {have}")
        items.append(
            "    { id: %s, label: %s, file: %s, code:\n      %s }"
            % (
                js_string(ex_id),
                js_string(label),
                js_string(f"examples/{filename}"),
                js_string(load_snippet(src)),
            )
        )
    return "\n  var EXAMPLES = [\n" + ",\n\n".join(items) + "\n  ];\n  "


def main() -> int:
    root = find_root()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--html", type=Path, help="مسیر mainpage.html (پیش‌فرض: جست‌وجو در پروژه)")
    ap.add_argument("--examples", type=Path, default=root / "examples", help="پوشه‌ی examples")
    ap.add_argument("--check", action="store_true", help="فقط بررسی کن؛ اگر قدیمی بود با کد ۱ خارج شو")
    args = ap.parse_args()

    html_path = args.html or find_html(root)
    if not html_path.is_file():
        sys.exit(f"فایل HTML پیدا نشد: {html_path}")
    if not args.examples.is_dir():
        sys.exit(f"پوشه‌ی examples پیدا نشد: {args.examples}")
    raw = html_path.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    html = raw.replace("\r\n", "\n")

    if not BLOCK_RE.search(html):
        sys.exit(
            f"مارکرهای /* EXAMPLES:START */ و /* EXAMPLES:END */ در {html_path} پیدا نشدند "
            "(نسخه‌ی جدید mainpage.html را commit کن)."
        )

    block = build_block(args.examples)
    new = BLOCK_RE.sub(lambda m: m.group(1) + block + m.group(3), html, count=1)
    if crlf:
        new = new.replace("\n", "\r\n")

    if new == raw:
        print("مثال‌ها از قبل به‌روز هستند.")
        return 0
    if args.check:
        print(f"{html_path} با examples/ هم‌خوان نیست؛ sync_examples.py را اجرا کن.", file=sys.stderr)
        return 1
    html_path.write_bytes(new.encode("utf-8"))
    print(f"{len(EXAMPLES)} مثال در {html_path} به‌روز شد.")
    return 0


if __name__ == "__main__":
    sys.exit(main())