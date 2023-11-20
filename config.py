import os
from dotenv import load_dotenv
load_dotenv()

LOG_FILE_PATH=os.getenv("LOG_FILE_PATH")
MODEL_FILENAME=os.getenv("MODEL_FILENAME")
DATASET=os.getenv("DATASET")
