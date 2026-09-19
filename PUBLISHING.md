# Publishing `peyk` — step by step

This is a one-time setup. After it's done once, every future release is just:
edit code → push to `main` (docs auto-update) → create a GitHub Release
(package auto-publishes to PyPI). No manual `twine upload`, no stored PyPI
password/token.

---

## 0. Before you start: replace the placeholder GitHub username

Three files currently say `YOUR_GITHUB_USERNAME` as a placeholder:

- `pyproject.toml` (the `[project.urls]` section)
- `docs/conf.py` (the `source_repository` theme option)

Find-and-replace `YOUR_GITHUB_USERNAME` with your real GitHub username/org in
both files before your first push.

If you'd rather the `LICENSE` file say your real name instead of "peyk
contributors" as the copyright holder, edit that too — it's a one-line change
at the top of `LICENSE`.

---

## 1. Push the code to GitHub

```bash
cd peyk
git init
git add .
git commit -m "Initial public release of peyk 1.0.0"
git branch -M main
```

Now create a new, empty repository on GitHub named `peyk` (github.com → New
repository → do **not** initialize it with a README/license/gitignore, since
this project already has all three):

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/peyk.git
git push -u origin main
```

---

## 2. Turn on GitHub Pages for the docs

In your new repo on GitHub: **Settings → Pages → Build and deployment →
Source → select "GitHub Actions"** (not "Deploy from a branch").

That's it — the `docs.yml` workflow already in `.github/workflows/` will now
build the Sphinx docs and publish them automatically on every push to `main`.
After your first push finishes (check the "Actions" tab), your docs will be
live at:

```
https://YOUR_GITHUB_USERNAME.github.io/peyk/
```

---

## 3. Create a PyPI account

You said you don't have one yet:

1. Go to <https://pypi.org/account/register/> and create an account.
2. Verify your email (PyPI requires this before you can do anything else).
3. **Enable two-factor authentication** — Account settings → Add 2FA. PyPI has
   required 2FA for all publishing accounts since 2024; you cannot publish a
   new project without it. An authenticator app (Google Authenticator, Authy,
   etc.) is the simplest option.

---

## 4. Register a "pending" Trusted Publisher for `peyk`

Normally you link a GitHub repo to a PyPI project *after* the project already
exists on PyPI. Since `peyk` doesn't exist there yet, PyPI supports
registering the link in advance — called a **pending publisher**:

1. Log in to PyPI, go to <https://pypi.org/manage/account/publishing/>.
2. Under "Add a pending publisher," fill in:
   - **PyPI Project Name**: `peyk`
   - **Owner**: your GitHub username/org
   - **Repository name**: `peyk`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi` (must match the `environment: name: pypi`
     already set in `.github/workflows/publish.yml` — don't change one
     without the other)
3. Save it.

This is the *only* PyPI-side setup needed. No API token, no secret to paste
into GitHub — the workflow authenticates itself using GitHub's OIDC identity,
which PyPI now trusts because of the step above.

---

## 5. Cut the 1.0.0 release

Back in your GitHub repo:

1. Go to **Releases → Draft a new release**.
2. **Tag**: `v1.0.0` (create it from `main`).
3. **Title**: `v1.0.0`.
4. Description: you can paste the `## [1.0.0]` section from `CHANGES.md`.
5. Click **Publish release**.

Publishing the release triggers `.github/workflows/publish.yml`, which builds
the package and uploads it to PyPI automatically. Watch the "Actions" tab —
once it's green, `peyk` is live:

```
https://pypi.org/project/peyk/
```

and installable with:

```bash
pip install peyk
```

---

## 6. Future releases

For every future version:

1. Bump the version number in **two** places (they must match):
   - `pyproject.toml` → `version = "..."`
   - `src/peyk/__init__.py` → `__version__ = "..."`
2. Add a new section to `CHANGES.md`.
3. Push to `main` (docs redeploy automatically).
4. Create a new GitHub Release with a matching tag (e.g. `v1.1.0`) → PyPI
   publish triggers automatically.

---

## Troubleshooting

- **Docs workflow fails on first run with warnings-as-errors**: the workflow
  uses `sphinx-build -W` (treat warnings as errors) to keep the docs held to
  a high bar. If something slipped through, temporarily remove `-W` from
  `.github/workflows/docs.yml`, let the docs deploy, then fix the warning at
  your own pace and re-add `-W`.
- **Publish workflow fails with a Trusted Publisher / OIDC error**: double
  check the Owner/Repository/Workflow filename/Environment name in PyPI's
  pending-publisher form exactly match this repo and `publish.yml` — a
  mismatch in any one field (including the `pypi` environment name) will
  cause PyPI to reject the identity token.
- **Version mismatch**: if `pyproject.toml` and `src/peyk/__init__.py` ever
  disagree, `pip show peyk` and `peyk.__version__` will disagree too — always
  bump both together.
