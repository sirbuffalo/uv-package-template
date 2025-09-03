# Repository Guidelines

## Project Structure & Modules

- `src/uv_package_template/`: package code (`__main__.py`, `env_vars.py`, `example_app_logic.py`, `setup_logging.py`).
- `tests/`: pytest tests (configured via `tool.pytest.ini_options`).
- `pyproject.toml`: metadata, scripts, ruff/mypy/pytest config, Poe tasks.
- `.github/workflows/`: CI (ruff, mypy, pytest) and reusable deploy workflow.

## Build, Test, and Dev Commands

- Setup dev env: `uv sync` (installs dev tools).
- Lint: `poe lint` (ruff check).
- Format: `poe fmt` (ruff format).
- Type check: `poe typecheck` (mypy with cache).
- Test: `poe test` (pytest, quiet).
- All checks: `poe check` (lint → typecheck → test). Run before pushing.
- Run CLI: `poe run` (or without poe: `uv run main` or `uv run python -m uv_package_template`.)
- Build: `uv build` (hatchling). Publish: `uv publish`.

## Coding Style & Naming

- Python 3.13, line length 100, single quotes, spaces for indent (ruff formatter).
- Imports: isort via ruff; combine `as` imports and sort within sections.
- Types: `disallow_untyped_defs = true`; prefer explicit return types.
- Package under `src/uv_package_template`; tests mirror modules where practical.

## Testing Guidelines

- Framework: pytest. Test paths: `tests/`. Import root: `src/`.
- Name tests `test_*.py`; use fixtures like `monkeypatch`/`caplog` (see existing tests).
- Avoid import‑time side effects; configure env/logging at runtime (done in `__main__.py`).
- Run locally: `poe test`. Add focused tests for new behaviors.

## Commit & Pull Requests

- Commit style: imperative, concise, present tense (e.g., "Add ruff config", "Fix CLI exit"). Group related changes.
- Before PR: `poe check` must pass; update docs as needed.
- PR description: what/why, notable decisions, linked issues (e.g., `Closes #123`). Include logs/screenshots for CLI output changes.

## Security & Configuration

- Secrets via env; example: `.env` with `EXAMPLE_API_TOKEN=...`. Optional loader installed with `--extra env`.
- Do not commit secrets or real tokens. `.env` is present locally and excluded from builds.
- Logging writes to `app.log` (rotating). Avoid logging secrets.

## Architecture Notes

- CLI (`main` in `__main__.py`) defers optional `.env` loading and uses `EXAMPLE_API_TOKEN` via `env_vars.load_or_die`. Core logic lives in `example_app_logic.some_app_logic`. Keep side effects out of `__init__.py`. Logging is configured at runtime inside `main()`.
