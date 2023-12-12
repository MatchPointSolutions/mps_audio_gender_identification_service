import os
from dotenv import load_dotenv
load_dotenv()

LOG_FILE_PATH=os.getenv("LOG_FILE_PATH")
MODEL_FILENAME=os.getenv("MODEL_FILENAME")
DATASET=os.getenv("DATASET")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
HOST=os.getenv("HOST")
ACCESS_KEY=os.getenv("ACCESS_KEY")
ACCESS_SECRET=os.getenv("ACCESS_SECRET")
ACOUST_ID_TOKEN = os.getenv("ACOUST_ID_TOKEN")
