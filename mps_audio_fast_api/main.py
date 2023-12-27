import os
import subprocess
import shutil
import concurrent.futures
import uvicorn
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, File, UploadFile
from email_notification import send_email
from acr_cloud import acr_cloud_identify_audio
from voice_recognition_model import identify_the_audio
from multi_voice_recognition_model import get_multi_voice_output
from acoust_id import get_acoust_id_audio_details
from config import SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USER, SUBJECT
from log import setup_logger
logger = setup_logger(__name__)
app = FastAPI()



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


@app.post("/mps_audio_recognition_service/")
async def upload_file(receiver_email, file: UploadFile = File(...)):
    try:
        data_dict = dict()
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        logger.info(file.filename)
        result2 = audio_seperator(file.filename)
        result1 = get_acoust_id_audio_details(file.filename)

        jsondata = {"filename": file.filename,
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
        filename  = file.filename
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")



