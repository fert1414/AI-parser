import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("news_agent_logger")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_formatter = logging.Formatter("[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Stream handler (console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(stream_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()