# UV-Package-Template

[![CI](https://github.com/sirbuffalo/uv-package-template/actions/workflows/ci.yml/badge.svg)](https://github.com/sirbuffalo/uv-package-template/actions/workflows/ci.yml)

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
- Environmental vars. Recommend https://direnv.net/ plus `.env` setup below.

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
uv sync --group dev
```

```bash
# If using direnv
cp .env.example .env      # updating as needed
cp .envrc.sample .envrc   # updating as needed
direnv allow .
```

## Quickstart

Dev machine:

- `poe sync` (Create dev environment)
- `poe install-hooks` (Install Git hooks: pre-commit and pre-push)
- `poe run` (logs a message and runs example logic)

Production (no dev tools):

- `uv sync --no-default-groups` (no dev tools)
- `uv run main` (`poe run` without poe)

## Development

### Commands

- Dev commands are task run with Poe (installed with the dev group):
  - Sync dependencies: `poe sync`
  - Sync and upgrade dependencies: `poe upgrade`
  - Install Git hooks (pre-commit, pre-push): `poe install-hooks`
  - Basic checks: `poe fast`
  - Full checks: `poe full`
  - Lint: `poe lint`
  - Format: `poe fmt`
  - Type check: `poe typecheck`
  - Tests: `poe test`
  - Hooks against all files: `poe hooks` (same intent at `poe full`)
- Add dependencies: `uv add <package>` (example: `uv add flask`)
- Add dev tools: `uv add --group dev <tool>` (e.g., `pytest-cov`)

### Package Layout

- `pyproject.toml`: project metadata, scripts, dev dependency group, ruff/pytest/mypy config, Poe tasks
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
