General instructions:

  create .venv and pick the venv in vs code after:
    uv sync

  add any pypi libraries with `uv add`. example:
    uv add flask

Run:
  uv sync --extra dev
To get ruff and pytest install for CI and testing.

See README-deploy.md if configuring continuous deployment
