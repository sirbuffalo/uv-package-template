# Copilot Instructions for this Repository

This file guides AI coding assistants working in this repo. Follow these rules to keep changes consistent, typed, linted, and testable.

## Project quick facts
- Language/runtime: Python 3.13 (src layout under `src/`)
- Package: `uv_package_template`
- Tooling: uv (env/pkg), poe (tasks), ruff (lint+fmt), mypy (types), pytest (tests), hatchling (build)
- CI: GitHub Actions runs ruff + mypy + pytest
- Entrypoints: `main` via `[project.scripts]` (see `src/uv_package_template/__main__.py`)

## How to run locally
- Setup env (dev tools): `uv sync`
- Dev tasks (via Poe; see `pyproject.toml`):
  - Lint: `poe lint`
  - Format: `poe fmt`
  - Typecheck: `poe typecheck`
  - Test: `poe test`
  - Fast checks: `poe fast`
  - All checks: `poe full`
  - Install hooks: `poe install-hooks`
- Example run: `poe run` (or without poe: `uv run main` or `uv run python -m uv_package_template`)

## Style and conventions
- Formatting: ruff formatter, single quotes, 100 char line length, spaces for indent
- Imports: isort via ruff; combine `as` imports; sort within sections
- Types: prefer explicit return types; `disallow_untyped_defs = true`; keep public APIs typed
- Logging: use `configure_logging()` and `get_logger()` from `setup_logging.py`; avoid import-time logging setup outside that module
- Side effects: avoid import-time side effects (no env reads, file I/O, or logging config at import)
- Env config: `env_vars.load_or_die`; required var example: `EXAMPLE_API_TOKEN`
- Package layout: keep code in `src/uv_package_template/`; keep tests in `tests/`

## Testing
- Framework: pytest; root import path includes `src/`
- Write focused tests for new behavior; mirror module names when practical
- Use fixtures as in existing tests: `monkeypatch`, `caplog`
- Ensure `poe full` passes before proposing changes

## Architecture notes (apply when implementing features)
- Keep `__init__.py` free of side effects
- Dependency injection over global reads: pass config (e.g., tokens) as function args
- CLI:
  - Keep orchestration in `src/uv_package_template/__main__.py`
  - Env handling lives in `env_vars.load_or_die` which defers optional `python-dotenv` import; treat absence as no-op
  - Validate required env (e.g., `EXAMPLE_API_TOKEN`); exit non-zero on missing values
- Logging:
  - Use the provided rotating file + console configuration
  - Do not log secrets in real features (the example logs a token for demonstration only)

## Do / Don’t
- DO:
  - Add/adjust tests with new behavior (happy path + 1-2 edge cases)
  - Maintain typing and satisfy mypy
  - Run lint/format/typecheck/tests and keep them green
  - Keep functions small and side-effect aware; prefer pure logic in modules and I/O in CLI
- DON’T:
  - Introduce import-time side effects
  - Read env vars in library code; do it in CLI and pass values down
  - Bypass ruff/mypy/pytest or commit broken checks
  - Log secrets or embed credentials; use env vars and document them

## Common tasks for assistants
- Adding a function:
  - Place under `src/uv_package_template/` with types and docstring
  - Add/modify tests in `tests/`
  - Run `poe full`
- Extending CLI behavior:
  - Modify `__main__.py` only for orchestration and logging
  - Keep env logic in `env_vars.py` and core logic in separate modules (unit-testable)
- Adding dependencies:
  - Use `uv add <pkg>` (or `uv add --dev <tool>` for dev)
  - Keep optional deps behind feature flags/extras when possible

## Build & publish
- Build with `uv build` (hatchling)
- PyPI publish via `uv publish` after removing the `"Private :: Do Not Upload"` classifier

## Commit and PR guidance
- Commits: imperative, concise (e.g., "Add ruff config", "Fix CLI exit")
- Before PR: run `poe full`; update docs if behavior changes
- PR description: what/why, notable decisions, linked issues; include logs or screenshots if CLI output changes

## File map (high-level)
- `src/uv_package_template/__main__.py`: CLI entrypoint (`main`) and example orchestration
- `src/uv_package_template/env_vars.py`: runtime `.env` loading and env validation
- `src/uv_package_template/example_app_logic.py`: core example logic; no env reads
- `src/uv_package_template/setup_logging.py`: logging configuration utilities
- `tests/`: pytest tests; import root is `src/`
- `pyproject.toml`: metadata, scripts, ruff/mypy/pytest config, poe tasks

---
If unsure, default to adding types, tests, and avoiding side effects; ensure all checks pass.
