from __future__ import annotations

import importlib
import sys
from types import ModuleType
from typing import Any, cast

import pytest
from pytest import MonkeyPatch


def reload_cli() -> ModuleType:
    # Ensure we reload the module to rebind functions if needed
    if 'uv_package_template.cli' in sys.modules:
        del sys.modules['uv_package_template.cli']
    return importlib.import_module('uv_package_template.cli')


def test_main_exits_when_missing_token(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv('EXAMPLE_TOKEN', raising=False)
    cli = reload_cli()
    # Prevent loading a real .env during this test
    def _no_load() -> bool:
        return False

    monkeypatch.setattr(cast(Any, cli), 'load_dotenv', _no_load)
    with pytest.raises(SystemExit) as ex:
        cli.main()
    assert ex.value.code == 1


def test_main_runs_when_token_present(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv('EXAMPLE_TOKEN', 'abc123')
    cli = reload_cli()
    called: list[str] = []

    def _fake_logic(token: str) -> None:
        called.append(token)

    monkeypatch.setattr(cast(Any, cli), 'some_app_logic', _fake_logic)
    # Should not raise
    cli.main()
    assert called == ['abc123']
