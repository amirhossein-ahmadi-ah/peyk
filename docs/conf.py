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
# toctree entries.  Treat those links as intentional.  Duplicate objects are
# also expected from the compatibility facades (models/helpers) and the
# canonical one-file API pages.
suppress_warnings = [
    "toc.not_included",
    "duplicate",
    "autosummary.import_cycle",
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
