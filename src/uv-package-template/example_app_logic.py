from dotenv import load_dotenv

from .setup_logging import get_logger

logger = get_logger(__name__)

load_dotenv()
if not (EXAMPLE_TOKEN := getenv('EXAMPLE_TOKEN')):
    logger.error('Missing EXAMPLE_TOKEN')
    raise SystemExit(1)

def some_app_logic():
    logger.info(f'some_app_logic, with token: {EXAMPLE_TOKEN}')
