from __future__ import annotations

# from collections.abc import Callable
# from contextlib import suppress
from logging import Logger
from os import getenv
import sys

from .setup_logging import get_logger

logger: Logger = get_logger(__name__)

# Commented out use of optional runtime dependency: python-dotenv
# Now recommend using direnv tool in developer shell for .env file loading

# # Optional runtime dependency: python-dotenv.
# # Keep a module-level reference so tests can monkeypatch `load_dotenv`.
# load_dotenv: Callable[[], bool] | None = None
# _dotenv_loaded: bool = False


def load_or_die(var_name: str) -> str:
    """Load an environment variable from .env or the environment.
    Dies if the requested variable is not defined."""
    # # Lazily import python-dotenv if available, otherwise no-op. This avoids
    # # forcing the dependency on all users while still supporting .env usage.
    # global load_dotenv, _dotenv_loaded
    # if not _dotenv_loaded:
    #     # Respect an existing loader (e.g., monkeypatched in tests). Only
    #     # import and set a default if none is defined yet.
    #     if load_dotenv is None:
    #         try:
    #             from dotenv import load_dotenv as _load_dotenv

    #             load_dotenv = _load_dotenv
    #         except Exception:
    #             # Provide a no-op so callers/tests can rely on the name existing.
    #             def _noop_load_dotenv() -> bool:
    #                 return False

    #             load_dotenv = _noop_load_dotenv

    #     # Call the loader (real or no-op) only the first time.
    #     with suppress(Exception):
    #         load_dotenv()
    #     _dotenv_loaded = True

    var_value: str | None = getenv(var_name)
    if not var_value:
        logger.error(f'Missing env var: {var_name}')
        sys.exit(1)

    return var_value
