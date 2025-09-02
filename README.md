uv-package-template

[![CI](https://github.com/sirbuffalo/uv-package-template/actions/workflows/ci.yml/badge.svg)](https://github.com/sirbuffalo/uv-package-template/actions/workflows/ci.yml)


Lightweight template for a Python package

Uses:
 - uv for environment management
 - poe scripts for dev task management
 - Ruff for linting and formattting
 - mypy for type checking
 - pytest for testing
 - GitHub Actions for CI/CD

Requirements
- uv installed: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `uv self update`
- Python 3.13 (configured in CI and pyproject.toml ruff settings; adjust as needed, perhaps `uv python install 3.13`)

Converting a template repo to a new name:
- Run the following shell commands in the project root:
```bash
NEWPACKAGENAME=new-name # replace  (use hyphens)
NEWMODULENAME=new_name # replace (use underscores)
[ -d src/uv_package_template ] && mv src/uv_package_template src/$NEWMODULENAME
```
```bash
LC_ALL=C find . \
  \( -path './.git' -o -path './.venv' -o -path './.mypy_cache' -o -path './.ruff_cache' -o -path './.pytest_cache' -o -path './dist' -o -path './build' \) -prune -o \
  -type f -exec sh -c '
    for f do
      if grep -Iq "uv[_-]package[_-]template" "$f"; then
        sed -i "" \
          -e "s/uv_package_template/$NEWPACKAGENAME/g" \
          -e "s/uv-package-template/$NEWMODULENAME/g" "$f"
      fi
    done
  ' sh {} +
```
```bash
LC_ALL=C grep -RIn "uv[_-]package[_-]template" . || echo "All set"
```
```bash
# From the repo root
rm -rf .venv
uv sync --all-extras
uv pip install -e .
```

Quickstart
- `uv sync --all-extras` (Create environment and install dev extras.)
- Point VSCode Venv to ./venv/bin/ 
- Run the example CLI entry points:
  - `uv run main` (logs a message and runs example logic)
  - `uv run alt`
  - Or directly: `uv run python -m language.cli`
- Configure env (optional example): create a `.env` with `EXAMPLE_TOKEN=...` so the example logic can run. If you installed the `env` extra, it will be loaded automatically by the CLI.
To disable `.env` loading install just: `uv sync --extra dev`
- Add dependencies: `uv add <package>` (example: `uv add flask`)

Development
- Tasks via Poe (installed in dev extras):
  - Sync dependencies: `uv run poe sync`
  - Sync and upgrade dependencies: `uv run poe upgrade-deps`
  - All checks / format (run before push): `uv run poe check`
  - Lint: `uv run poe lint`
  - Format: `uv run poe fmt`
  - Type check: `uv run poe typecheck`
  - Tests: `uv run poe test`
- Add dev tools: `uv add --extra dev <tool>` (e.g., `pytest-cov`)

Project Layout
- `pyproject.toml`: project metadata, scripts, dev extras, ruff/pytest/mypy config, Poe tasks
- `src/uv_package_template/cli.py`: console entry points (`main`, `alt`)
  - Note: dev commands like lint/test now live under Poe tasks, not console scripts
- `src/uv_package_template/example_app_logic.py`: example logic using `.env`
- `src/uv_package_template/setup_logging.py`: basic rotating file + console logging
- `src/uv_package_template/__init__.py`: version metadata without side effects
- `tests/`: place tests here (configured via `tool.pytest.ini_options`)
- `.github/workflows/`: CI (lint + tests) and optional reusable deploy workflow
- `README-deploy.md`: optional server deployment guide

Packaging and Publish
- Build: `uv build` (uses hatchling)
- Publish: `uv publish` (configure PyPI credentials as needed)

Using This as a Template
- Rename the distribution and module:
  - In `pyproject.toml [project] name` (distribution name)
  - In `src/<your_package_name>/...` (module/package name)
  - Adjust console scripts in `[project.scripts]` to a single, descriptive name
- Update metadata: description, license, authors, classifiers, URLs
- Decide supported Python versions and set `requires-python` accordingly
- Add a license file (e.g., `LICENSE`) and optionally `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`

Notes and Suggestions
- Logging defaults: the console log level defaults to INFO; align docstrings and levels as desired.
- CI: `.github/workflows/ci.yml` runs uv + ruff + mypy + pytest on pushes/PRs; tweak Python versions or matrix as needed.
- Deployment: see `README-deploy.md` if you plan to rsync to a server and restart a systemd unit. Otherwise you can delete that file.
