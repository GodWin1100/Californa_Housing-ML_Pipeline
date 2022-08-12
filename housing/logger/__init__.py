# https://www.youtube.com/watch?v=gsa1oFn9n0M
import logging
from datetime import datetime
import os
import pandas as pd

LOG_DIR = "housing_logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}"
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format="[%(asctime)s] ^; %(levelname)s: ^; %(name)s:%(module)s:%(filename)s:%(funcName)s() ^; => %(message)s",
    level=logging.INFO,
)


def get_log_dataframe(file_path):
    data = []
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns = ["Time stamp", "Log Level", "file & function name", "message"]
    log_df.columns = columns

    log_df["log_message"] = log_df["Time stamp"].astype(str) + ":$" + log_df["message"]

    return log_df[["log_message"]]
