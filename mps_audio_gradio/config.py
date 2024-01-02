"""
Load all the Environment variables
"""
import os
from dotenv import load_dotenv
load_dotenv()

LOG_FILE_PATH=os.getenv("LOG_FILE_PATH")
FASTAPI_URL = os.getenv("FASTAPI_URL")
