from __future__ import annotations

import sys
from os import getenv
from dotenv import load_dotenv
from .setup_logging import configure_logging, get_logger
from .example_app_logic import some_app_logic

configure_logging()
logger = get_logger(__name__)


def main() -> None:
    """CLI entrypoint.

    Loads environment at runtime and validates required settings, avoiding
    import-time side effects for library users.
    """
    logger.info('Hello from uv_package_template:main')
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
