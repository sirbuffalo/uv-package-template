from __future__ import annotations

from os import getenv
import sys
from typing import Callable

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
        try:  # type: ignore[no-redef]
            from dotenv import load_dotenv as _load_dotenv  # type: ignore
            load_dotenv = _load_dotenv  # type: ignore[assignment]
        except Exception:
            # Provide a no-op so callers/tests can rely on the name existing.
            load_dotenv = lambda: False  # type: ignore[assignment]

    # Call the loader (real or no-op)
    try:
        load_dotenv()  # type: ignore[misc, operator]
    except Exception:
        # Loading .env is best-effort; continue if it fails.
        pass

    token = getenv('EXAMPLE_TOKEN')
    if not token:
        logger.error('Missing EXAMPLE_TOKEN')
        sys.exit(1)

    some_app_logic(token)


def alt() -> None:
    logger.info('Hello from uv_package_template:alt')


if __name__ == '__main__':
    main()
