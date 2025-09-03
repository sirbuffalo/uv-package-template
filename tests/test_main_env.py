from __future__ import annotations

import pytest
from pytest import MonkeyPatch


def test_env_logic_exits_when_missing_token(monkeypatch: MonkeyPatch) -> None:
    # Ensure the expected var is absent
    monkeypatch.delenv('EXAMPLE_API_TOKEN', raising=False)

    # Call the new helper that encapsulates the former `alt` logic
    import uv_package_template.__main__ as main_mod

    with pytest.raises(SystemExit) as ex:
        main_mod._example_logic_with_env_var()
    assert ex.value.code == 1


def test_env_logic_runs_when_token_present(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv('EXAMPLE_API_TOKEN', 'abc123')

    # Patch the function reference used in uv_package_template.__main__
    import uv_package_template.__main__ as main_mod

    called: list[str] = []

    def _fake_logic(token: str) -> None:
        called.append(token)

    monkeypatch.setattr(main_mod, 'some_app_logic', _fake_logic)

    # Should not raise
    main_mod._example_logic_with_env_var()
    assert called == ['abc123']
