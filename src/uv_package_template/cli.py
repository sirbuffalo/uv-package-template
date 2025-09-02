from __future__ import annotations

from collections.abc import Callable
from contextlib import suppress
from os import getenv
import sys

from .example_app_logic import some_app_logic
from .setup_logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

# Optional runtime dependency: python-dotenv.
# Keep a module-level reference so tests can monkeypatch `load_dotenv`.
load_dotenv: Callable[[], bool] | None = None


def main() -> None:
    """CLI entrypoint.

    Loads environment at runtime and validates required settings, avoiding
    import-time side effects for library users.
    """
    logger.info('Hello from uv_package_template:main')

    # Lazily import python-dotenv if available, otherwise no-op. This avoids
    # forcing the dependency on all users while still supporting .env usage.
    global load_dotenv
    if load_dotenv is None:
        try:
            from dotenv import load_dotenv as _load_dotenv
            load_dotenv = _load_dotenv
        except Exception:
            # Provide a no-op so callers/tests can rely on the name existing.
            def _noop_load_dotenv() -> bool:
                return False

            load_dotenv = _noop_load_dotenv

    # Call the loader (real or no-op)
    if load_dotenv is not None:
        with suppress(Exception):
            load_dotenv()

    token = getenv('EXAMPLE_TOKEN')
    if not token:
        logger.error('Missing EXAMPLE_TOKEN')
        sys.exit(1)

    some_app_logic(token)


def alt() -> None:
    logger.info('Hello from uv_package_template:alt')


if __name__ == '__main__':
    main()
