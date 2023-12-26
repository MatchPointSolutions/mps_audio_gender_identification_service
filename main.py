from fastapi import FastAPI, File, UploadFile
import uvicorn
import gradio as gr
from pathlib import Path
from email_notification import send_email
from acr_cloud import acr_cloud_identify_audio
from voice_recognition_model import identify_the_audio
from multi_voice_recognition_model import get_multi_voice_output
from acoust_id import get_acoust_id_audio_details
# from seperator import audio_seperator
from config import SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USER, SUBJECT
from log import setup_logger
logger = setup_logger(__name__)
app = FastAPI()
import os
import subprocess
import shutil
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    logger.info(file.filename)
    result = identify_the_audio(file.filename)
    return {"filename": file.filename,
            "result": result}


@app.post("/test_multiaudio_pyannote/")
async def upload_file(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        logger.info(file.filename)
        result = get_multi_voice_output(file.filename)
        return {"filename": file.filename,
                "result": result}
    except Exception as error:
        return {"Error": str(error)}

@app.post("/test_acr_cloud/")
async def upload_file(file: UploadFile = File(...)):
    try:
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        logger.info(file.filename)
        result = acr_cloud_identify_audio(file.filename)
        return {"filename": file.filename,
                "result": result}
    except Exception as error:
        return {"Error": str(error)}

@app.post("/test_acoust_id/")
async def upload_file(receiver_email, file: UploadFile = File(...)):
    try:
        data_dict = dict()
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        logger.info(file.filename)
        result = get_acoust_id_audio_details(file.filename)

        jsondata = {"filename": file.filename,
                    "result": result}
        data_dict["title"] = jsondata["result"]["results"][0]["recordings"][2]["title"]
        data_dict["artist"] = jsondata["result"]["results"][0]["recordings"][2]["artists"]
        data_dict["filename"] = file.filename
        body = f"""The Result from processed Audio file:
                    {data_dict}"""
        try:
            send_email(SUBJECT, body,str(receiver_email), SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
            logger.info(f"Email Notification sent to {receiver_email}")
        except:
            logger.info("Email Notification not sent")
        return {"result": data_dict}
    except Exception as error:
        return {"Error": str(error)}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")

# Create the output directory if it doesn't exist
OUTPUT_DIR = "./data"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def audio_seperator(file):
    try:
        logger.info("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        logger.info("file: {}".format(file))
        temp_file_path = Path(file)
        filename = temp_file_path.name
        result = subprocess.run(
            ['spleeter', 'separate', '-o', OUTPUT_DIR, file],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stderr
        logger.info(output)
        # list files in the output directory recursively
        for dirpath, dirnames, filenames in os.walk(OUTPUT_DIR):
            for filename in filenames:
                if(filename == "vocals.wav"):
                    file_path = os.path.join(dirpath, filename)
                    vocal_response = get_multi_voice_output(file_path)
                    logger.info(file_path)
                    break
                    
        return vocal_response
    except Exception as error:
        logger.exception(f"in audio_seperator: Error: {error}")
        return None
def gradio_audio_file_analysis(input_file,receiver_email):
    try:
        temp_file_path = Path(input_file)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result1thread = executor.submit(get_acoust_id_audio_details,input_file)
            result2thread = executor.submit(audio_seperator,input_file)
        result1 = result1thread.result()
        result2 = result2thread.result()
        jsondata = {"filename": temp_file_path.name,
                    "result": result1}
        # is empty results
        if jsondata["result"]["results"]:
            title = jsondata["result"]["results"][0]["recordings"][2].get("title","")
            artist = jsondata["result"]["results"][0]["recordings"][2]["artists"][0].get("name","")
        else:
            title = "could not find the title in acoustid cloud"
            artist = "could not find the artist in acoustid cloud"
        male_count = result2["male_count"]
        female_count = result2["female_count"]
        filename  = temp_file_path.name
        body = f"""
            Thank you for using Matchpoint Audio Analyzer service. Our System has analyzed the audio file and Below are the analysis details.
                Human Voices:
                No. of Male voices : {male_count}
                No. of femal Voices : {female_count}
                Music Title : {title}
                Music Artist : {artist}
                Filename : {filename}
            Note: Matchpoint human Voice identification service works with 80% accuracy.
        """
        try:
            send_email(SUBJECT, body,str(receiver_email), SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
            logger.info(f"Email Notification sent to {receiver_email}")
            email = f"Email Notification sent to {receiver_email}"
        except:
            logger.info("Email Notification not sent")
            email = f"Email Notification not sent to {receiver_email}"
        body = f"""
            Thank you for using Matchpoint Audio Analyzer service. Our System has analyzed the audio file and Below are the analysis details.
                Human Voices:
                No. of Male voices : {male_count}
                No. of femal Voices : {female_count}
                Music Title : {title}
                Music Artist : {artist}
                Filename : {filename}
                Email : {email}
            Note: Matchpoint human Voice identification service works with 80% accuracy.
        """
        shutil.rmtree(OUTPUT_DIR)
        return body
    except Exception as error:
        logger.info(f"in gradio_audio_file_analysis: Error: {error}")
        shutil.rmtree(OUTPUT_DIR)
        return "Unable to Process the audio file from gradio_audio_file_analysis"

demo1 = gr.Interface(fn= gradio_audio_file_analysis,
                    inputs = [
                    "file",
                    gr.Textbox(label="Email",info="Receive an Email Notification")
                    ],
                    outputs = "text",
                    allow_flagging="never")

# demo2 = gr.Interface(fn= audio_seperator,
#                     inputs = "file",
#                     outputs = "text",
#                     allow_flagging="never")


# demo = gr.TabbedInterface([demo1, demo2], ["Audio File Uploader", "Audio File Seperator"])
demo1.launch(server_name="0.0.0.0", server_port=7860)
# demo1.launch(share=True)