"""
Uses Gradio open source python library for UI Interface
"""
import os
import requests
import gradio as gr
from pathlib import Path
from log import setup_logger
from config import FASTAPI_URL
logger = setup_logger(__name__)


def call_fastapi(email_address,input_file):
    """
    Args: email_address (receiver email address)
          input_file (path to the file containing audio to be analyzed)
    -   the file contents are sent over the API endpoint to get processed by
        MPS Audio Analyser
    Output: result (text)
    """
    # temp_file_path = Path(input_file)
    filename = input_file.split("/")[-1]
    with open(input_file, "rb") as audio_file:
    # Create a dictionary with the audio file data
        audio_content = audio_file.read()
    files = {"file": (filename, audio_content)}
    response = requests.post(f"{FASTAPI_URL}/mps_audio_recognition_service?receiver_email={email_address}", files=files)
    result = response.json()["result"]
    return result

demo = gr.Interface(
                    title="Audio Analysis",
                    css="footer {visibility: hidden}",
                    fn= call_fastapi,
                    inputs = [
                    gr.Textbox(label="Email",info="Receive an Email Notification"),
                    "file"
                    ],
                    outputs = "text",
                    allow_flagging="never")

demo.launch(server_name="0.0.0.0", server_port=7860)
