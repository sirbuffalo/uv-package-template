from __future__ import annotations

import sys
from .setup_logging import configure_logging, get_logger
from .example_app_logic import some_app_logic

configure_logging()
logger = get_logger(__name__)


def main():
    logger.info("Hello from uv-package-template:main")
    some_app_logic()


def alt():
    logger.info("Hello from uv-package-template:alt")


def vt_test() -> None:
    """Run the project's pytest suite.

    This entry point is meant for local dev/CI convenience. It imports pytest at
    runtime so production installs don't need to depend on pytest. If pytest
    isn't available, provide a friendly hint to install dev extras.
    """
    try:
        import pytest  # type: ignore
    except Exception:  # pragma: no cover - simple import guard
        logger.error(
            'pytest is not installed. Install dev deps with:\n'
            "  uv sync --extra dev\n"
            'or run tests directly via: uv run pytest'
        )
        sys.exit(1)

    # Delegate to pytest's console entry; it will use sys.argv.
    sys.exit(pytest.console_main())


if __name__ == "__main__":
    main()
