# UV-Package-Template

[![CI](https://github.com/sirbuffalo/uv_package_template/actions/workflows/ci.yml/badge.svg)](https://github.com/sirbuffalo/uv_package_template/actions/workflows/ci.yml)

A template for building uv-based Python packages.

## Architecture and Tooling

- uv for environment management
- poe scripts for dev task management
- Ruff for linting and formatting
- mypy for type checking
- pytest for testing
- GitHub Actions for CI/CD.

## Requirements

- uv installed: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `uv self update`
- Python 3.13 (configured in CI and pyproject.toml ruff settings; adjust as needed, perhaps `uv python install 3.13`)
- May require configuring environmental vars, either directly, or via a private `.env` file in the root. For example, create a `EXAMPLE_API_TOKEN=any_value_here` so the example logic can run. If you installed the `env` extra (see below), `.env` will be loaded programatically. To disable automated `.env` loading, install only dev tools: `uv sync --extra dev`.

## Using this repo as a Template

In addition to the renaming steps below, consider:

- Updating metadata: description, license, authors, classifiers, URLs
- Consider a `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, or `CHANGELOG.md`

### Renaming and Installation

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
          -e "s/uv_package_template/$NEWMODULENAME/g" \
          -e "s/uv-package-template/$NEWPACKAGENAME/g" "$f"
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
uv pip install -e '.[env]'
```

## Quickstart

- `uv sync --extra dev --extra env && uv pip install -e '.[env]'` (one-time bootstrap)
- `uv run poe sync` (Create environment, install dev + env extras, editable install.)
- Run the CLI entry point:
  - `uv run main` (logs a message and runs example logic)
  - Or directly: `uv run python -m uv_package_template`

## Development

### Commands

- Dev commands are task run with Poe (which is installed with dev extras):
  - Sync dependencies: `uv run poe sync`
  - Sync and upgrade dependencies: `uv run poe upgrade-deps`
  - All checks / format (run before push): `uv run poe check`
  - Lint: `uv run poe lint`
  - Format: `uv run poe fmt`
  - Type check: `uv run poe typecheck`
  - Tests: `uv run poe test`
- Add dependencies: `uv add <package>` (example: `uv add flask`)
- Add dev tools: `uv add --extra dev <tool>` (e.g., `pytest-cov`)

### Package Layout

- `pyproject.toml`: project metadata, scripts, dev extras, ruff/pytest/mypy config, Poe tasks
- `src/uv_package_template/__main__.py`: CLI entry point (`main`) and helper `_example_logic_with_env_var()`
- `src/uv_package_template/__init__.py`: version metadata without side effects
- `src/uv_package_template/env_vars.py`: environment loading helper used by the CLI
- `src/uv_package_template/example_app_logic.py`: example logic using `.env`
- `src/uv_package_template/setup_logging.py`: basic rotating file + console logging
- `tests/`: place tests here (configured via `tool.pytest.ini_options`)
- `.github/workflows/`: CI (lint + tests) and optional reusable deploy workflow
- `README-deploy.md`: optional server deployment guide

### Packaging and Publishing

Not needed unless distributing the package (via PyPI or otherwise).

- Build: `uv build` (uses hatchling)
- Publish: `uv publish` (configure PyPI credentials as needed)

### Other Notes

- Logging defaults: the console log level defaults to INFO, see `setup_logging.py`
- Deployment: see `README-deploy.md` if you plan to rsync to a server and restart a systemd unit. Otherwise you can delete that file.

## TODOs

Notes on next steps and open issues:

- None.
