from __future__ import annotations

from uv_package_template.example_app_logic import some_app_logic


def test_some_app_logic_logs(caplog):
    caplog.set_level('INFO')
    some_app_logic('test-token')
    assert any('some_app_logic, with token: test-token' in m for m in caplog.messages)
