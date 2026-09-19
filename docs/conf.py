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
html_theme = "furo"
html_title = "peyk documentation"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_favicon = "_static/favicon-32.png"
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_logo": "logo.png",
    "dark_logo": "logo-dark.png",
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
