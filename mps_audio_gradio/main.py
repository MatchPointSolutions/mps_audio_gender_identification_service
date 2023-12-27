import os
import requests
import gradio as gr
from pathlib import Path
from log import setup_logger
from config import FASTAPI_URL
logger = setup_logger(__name__)


def call_fastapi(email_address,input_file):
    temp_file_path = Path(input_file)
    response = requests.post(f"{FASTAPI_URL}/mps_audio_recognition_service", receiver_email=email_address,file = temp_file_path)
    result = response.json()["result"]
    return result

demo = gr.Interface(fn= call_fastapi,
                    inputs = [
                    gr.Textbox(label="Email",info="Receive an Email Notification"),
                    "file"
                    ],
                    outputs = "text",
                    allow_flagging="never")

demo.launch(server_name="0.0.0.0", server_port=7860)
