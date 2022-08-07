# https://www.youtube.com/watch?v=gsa1oFn9n0M
import logging
from datetime import datetime
import os

LOG_DIR = "housing_logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}"
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format="[%(asctime)s] %(levelname)s: %(name)s:%(module)s => %(message)s",
    level=logging.INFO,
)
