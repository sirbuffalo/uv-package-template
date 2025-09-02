from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from sys import stderr


def configure_logging(
    *,
    log_file: str = 'app.log',
    file_level: int = logging.DEBUG,
    console_level: int = logging.INFO,
    max_bytes: int = 1_000_000,
    backup_count: int = 3,
    force: bool = True,
) -> None:
    """Configure root logger with file + console handlers.

    - File: DEBUG level, rotating to keep size bounded.
    - Console (stderr): INFO by default; override via ``console_level``.
    """
    file_handler = RotatingFileHandler(
        log_file,
        mode='a',
        encoding='utf-8',
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(
        logging.Formatter(fmt='%(asctime)s %(levelname)s %(name)s: %(message)s')
    )

    console_handler = logging.StreamHandler(stderr)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter(fmt='%(levelname)s %(name)s: %(message)s'))

    logging.basicConfig(
        level=logging.DEBUG,  # root logger
        handlers=[file_handler, console_handler],
        force=force,
    )


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger for the given name (or root when None)."""
    return logging.getLogger(name)
