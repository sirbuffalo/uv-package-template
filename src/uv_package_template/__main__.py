from __future__ import annotations

from logging import Logger

from .env_vars import load_or_die
from .example_app_logic import some_app_logic
from .setup_logging import configure_logging, get_logger
logger: Logger = get_logger(__name__)


def _example_logic_with_env_var() -> None:
    api_token: str = load_or_die('EXAMPLE_API_TOKEN')
    some_app_logic(api_token)


def main() -> None:
    """Main entrypoint."""
    # Configure logging at runtime (avoid import-time side effects)
    configure_logging()
    logger.info('Hello from uv_package_template:main')

    _example_logic_with_env_var()


# package level entry point
if __name__ == '__main__':
    main()
