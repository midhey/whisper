import logging
import os
from logging.handlers import RotatingFileHandler

LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

logger = logging.getLogger("transcriber")
logger.setLevel(logging.DEBUG)

class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level

# до 5 МБ, 5 файлов резервных копий
output_handler = RotatingFileHandler(
    os.path.join(LOG_FOLDER, "output.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
output_handler.setLevel(logging.DEBUG)
output_handler.addFilter(MaxLevelFilter(logging.INFO))
output_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
output_handler.setFormatter(output_formatter)

# до 5 МБ, 5 файлов резервных копий
error_handler = RotatingFileHandler(
    os.path.join(LOG_FOLDER, "error.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
error_handler.setLevel(logging.WARNING)
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)

logger.addHandler(output_handler)
logger.addHandler(error_handler)

