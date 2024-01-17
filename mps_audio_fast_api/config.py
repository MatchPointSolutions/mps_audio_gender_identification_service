"""
Load all the Environment variables
"""
import os
from dotenv import load_dotenv
load_dotenv()

LOG_FILE_PATH=os.getenv("LOG_FILE_PATH")
MODEL_FILENAME=os.getenv("MODEL_FILENAME")
DATASET=os.getenv("DATASET")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
ACOUST_ID_TOKEN = os.getenv("ACOUST_ID_TOKEN")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SUBJECT = os.getenv("SUBJECT")
