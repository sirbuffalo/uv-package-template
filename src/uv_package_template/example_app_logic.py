from __future__ import annotations

from logging import Logger

from .setup_logging import get_logger

logger: Logger = get_logger(__name__)


def some_app_logic(api_token: str) -> None:
    """Example application logic that requires a token.

    The caller is responsible for providing configuration such as tokens;
    this function avoids reading environment variables at import time.
    """
    logger.info(f'some_app_logic, with API token: {api_token}')
