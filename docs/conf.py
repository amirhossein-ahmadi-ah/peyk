"""Sphinx configuration for the Peyk documentation."""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, os.fspath(SRC_DIR))

project = "peyk"
author = "peyk contributors"
release = "1.0.0"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autosummary_generate = True
autosummary_imported_members = False
# Recursive autosummary creates many leaf pages that are linked from the
# generated index pages rather than appearing as explicit hand-written
# toctree entries, so "toc.not_included" is intentional.
#
# "ref.python" silences "more than one target found for cross-reference":
# the Telegram/Bale/Rubika packages each define their own Message, User,
# File, Chat... so a bare ``Message`` in a docstring is inherently ambiguous.
# To keep real broken references visible, qualify the name in the docstring
# (e.g. :class:`peyk.types.Message`) and drop this entry.
suppress_warnings = [
    "toc.not_included",
    "autosummary.import_cycle",
    "ref.python",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "signature"
autodoc_class_signature = "mixed"
autodoc_preserve_defaults = True

# S1 established Google-style docstrings.  Keep Napoleon deliberately
# explicit so the documentation contract is not dependent on Sphinx defaults.
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_use_ivar = True

# Furo gives the clean, modern navigation and typography expected by this
# project and is closer in spirit to docs.aiogram.dev than the bare Sphinx
# theme.  It remains a normal Sphinx theme, so no source restructuring is
# required to switch themes later.
#
# The look (palette, radii, landing-page cards) is layered on top of Furo via
# the CSS variables below plus ``_static/custom.css``; both are derived from the
# logo's blue -> cyan gradient with the orange kept for the logo only.
html_theme = "furo"
html_title = "peyk documentation"
html_static_path = ["_static"]
# ONE logo only.  Furo renders ``html_logo`` *and* ``light_logo``/``dark_logo``
# when both are configured, which is what produced two big logos in the
# sidebar.  The logo is a transparent SVG, so it works on light and dark alike.
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"

_FONT_SANS = (
    "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI Variable', "
    "'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
)
_FONT_MONO = (
    "'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, 'SF Mono', "
    "Menlo, Consolas, 'Liberation Mono', monospace"
)

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_css_variables": {
        "font-stack": _FONT_SANS,
        "font-stack--monospace": _FONT_MONO,
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f7f9fc",
        "color-background-hover": "#eef3fd",
        "color-background-hover--transparent": "#eef3fd00",
        "color-background-border": "#e4e9f2",
        "color-foreground-primary": "#0f172a",
        "color-foreground-secondary": "#4b5a70",
        "color-foreground-muted": "#66758c",
        "color-foreground-border": "#9aa8bd",
        "color-sidebar-background": "#f7f9fc",
        "color-sidebar-background-border": "#e4e9f2",
        "color-sidebar-caption-text": "#66758c",
        "color-sidebar-link-text": "#334155",
        "color-sidebar-link-text--top-level": "#0f172a",
        "color-sidebar-item-background--hover": "#e9effc",
        "color-sidebar-item-background--current": "#e3ebfd",
        "color-sidebar-search-background": "#ffffff",
        "color-sidebar-search-background--focus": "#ffffff",
        "color-sidebar-search-border": "#dbe2ee",
        "color-sidebar-search-icon": "#66758c",
        "color-sidebar-search-text": "#0f172a",
        "color-toc-item-text--active": "#2563eb",
        "color-link": "#2563eb",
        "color-link--hover": "#1d4ed8",
        "color-link-underline": "transparent",
        "color-link-underline--hover": "#2563eb",
        "color-link--visited": "#2563eb",
        "color-link-underline--visited": "transparent",
        "color-link--visited--hover": "#1d4ed8",
        "color-link-underline--visited--hover": "#2563eb",
        "color-inline-code-background": "#eef2f8",
        "color-code-background": "#f6f8fc",
        "color-code-foreground": "#1e293b",
        "color-highlight-on-target": "#fff4cc",
        "color-api-name": "#1d4ed8",
        "color-api-pre-name": "#4b5a70",
        "color-api-background": "#f3f6fc",
        "color-api-background-hover": "#eaf0fb",
        "color-table-header-background": "#f3f6fb",
        "color-table-border": "#e4e9f2",
        # peyk-specific tokens used by custom.css
        "peyk-cyan": "#06b6d4",
        "peyk-accent-soft": "rgba(37, 99, 235, 0.09)",
    },
    "dark_css_variables": {
        "font-stack": _FONT_SANS,
        "font-stack--monospace": _FONT_MONO,
        "color-brand-primary": "#5b9bff",
        "color-brand-content": "#7fb0ff",
        "color-background-primary": "#0b1020",
        "color-background-secondary": "#0e1528",
        "color-background-hover": "#141d36",
        "color-background-hover--transparent": "#141d3600",
        "color-background-border": "#1d2845",
        "color-foreground-primary": "#e7ecf6",
        "color-foreground-secondary": "#a3b1c9",
        "color-foreground-muted": "#7f8fab",
        "color-foreground-border": "#4a5a7a",
        "color-sidebar-background": "#0e1528",
        "color-sidebar-background-border": "#1d2845",
        "color-sidebar-caption-text": "#7f8fab",
        "color-sidebar-link-text": "#b8c4d9",
        "color-sidebar-link-text--top-level": "#e7ecf6",
        "color-sidebar-item-background--hover": "#16203d",
        "color-sidebar-item-background--current": "#182645",
        "color-sidebar-search-background": "#0b1020",
        "color-sidebar-search-background--focus": "#0b1020",
        "color-sidebar-search-border": "#24314f",
        "color-sidebar-search-icon": "#7f8fab",
        "color-sidebar-search-text": "#e7ecf6",
        "color-toc-item-text--active": "#7fb0ff",
        "color-link": "#7fb0ff",
        "color-link--hover": "#a6c8ff",
        "color-link-underline": "transparent",
        "color-link-underline--hover": "#7fb0ff",
        "color-link--visited": "#7fb0ff",
        "color-link-underline--visited": "transparent",
        "color-link--visited--hover": "#a6c8ff",
        "color-link-underline--visited--hover": "#7fb0ff",
        "color-inline-code-background": "#141d38",
        "color-code-background": "#0f1730",
        "color-code-foreground": "#dbe4f5",
        "color-highlight-on-target": "#3d3210",
        "color-api-name": "#8dbaff",
        "color-api-pre-name": "#a3b1c9",
        "color-api-background": "#0f1730",
        "color-api-background-hover": "#141d38",
        "color-table-header-background": "#0f1730",
        "color-table-border": "#1d2845",
        "peyk-cyan": "#22d3ee",
        "peyk-accent-soft": "rgba(91, 155, 255, 0.12)",
    },
    # NOTE: replace YOUR_GITHUB_USERNAME once the repo is pushed, so the
    # "Edit this page" / "View source" links in the built docs are correct.
    "source_repository": "https://github.com/amirhossein-ahmadi-ah/peyk/",
    "source_branch": "main",
    "source_directory": "docs/",
}

# Avoid emitting a noisy copyright footer; the project metadata remains the
# authoritative license/source information.
html_show_sourcelink = True
html_copy_source = True
html_css_files = ["custom.css"]

# Keep generated autosummary pages out of the hand-written navigation tree.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The Python standard library is intentionally not configured through
# Intersphinx here: a documentation build should remain fully offline and
# reproducible.  Python types in signatures are rendered directly by
# autodoc/Napoleon.  A future hosted build can add an inventory mapping if
# cross-project links become useful.


# ---------------------------------------------------------------------------
# Duplicate object descriptions
# ---------------------------------------------------------------------------
# "duplicate object description of X, other instance in Y" is emitted by the
# Python domain WITHOUT a warning type, so it can NOT be silenced through
# ``suppress_warnings`` (there is no "duplicate" category).  Peyk deliberately
# documents the same objects from several places (compat facades, the
# one-page ``api_reference`` and the recursive autosummary pages), so drop
# exactly that message with a logging filter instead of failing ``-W`` builds.
import logging


class _DropDuplicateObjectWarnings(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "duplicate object description" not in record.getMessage()


def setup(app):  # noqa: D103 - Sphinx hook
    flt = _DropDuplicateObjectWarnings()
    # Sphinx prefixes module loggers with "sphinx." so the python domain's
    # logger is "sphinx.sphinx.domains.python"; attach to both spellings so
    # this keeps working if that ever changes.
    for name in ("sphinx.domains.python", "sphinx.sphinx.domains.python"):
        logging.getLogger(name).addFilter(flt)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
