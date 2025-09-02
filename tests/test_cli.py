from __future__ import annotations

import builtins
import importlib
import sys
from types import ModuleType

import pytest


def reload_cli() -> ModuleType:
    # Ensure we reload the module to rebind functions if needed
    if 'uv_package_template.cli' in sys.modules:
        del sys.modules['uv_package_template.cli']
    return importlib.import_module('uv_package_template.cli')


def test_main_exits_when_missing_token(monkeypatch):
    monkeypatch.delenv('EXAMPLE_TOKEN', raising=False)
    cli = reload_cli()
    # Prevent loading a real .env during this test
    import uv_package_template.cli as _cli  # type: ignore
    # Patch the load_dotenv that main() calls to a no-op
    _cli.load_dotenv = lambda: False  # type: ignore[assignment]
    with pytest.raises(SystemExit) as ex:
        cli.main()
    assert ex.value.code == 1


def test_main_runs_when_token_present(monkeypatch):
    monkeypatch.setenv('EXAMPLE_TOKEN', 'abc123')
    cli = reload_cli()
    called: list[str] = []

    def _fake_logic(token: str) -> None:
        called.append(token)

    monkeypatch.setattr(cli, 'some_app_logic', _fake_logic)
    # Should not raise
    cli.main()
    assert called == ['abc123']
