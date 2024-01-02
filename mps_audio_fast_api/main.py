"""
MPS Audio Analyser uses the fastapi service to extract the details
from the uploaded audio file
"""
import os
import subprocess
import shutil
import uvicorn
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from email_notification import send_email
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
    """
    Args: file (audio file path)
    -   Spleeter is used to seperate vocals and music in an audio file
    Output: "vocals.wav"
    """
    try:
        logger.info("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        logger.info("file: {}".format(file))
        temp_file_path = Path(file)
        filename = file.split("/")[-1]
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
    """
    Args: receiver_email (message to be sent to the concerned email)
          file (uploaded audio file)
    -   result1 uses audio_seperator function to seperate vocals and music
    -   result2 uses get_acoust_id_details function to get music details from acoust id database
    Output: body (result1, result2)
    """
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    logger.info(file.filename)
    try:

        result2 = audio_seperator(file.filename)
    except:
        result2 = {"male_count": 0, "female_count": 0}


    logger.info("result2: -------->>>> {}".format(result2))
    try:
        result1 = get_acoust_id_audio_details(file.filename)
        jsondata = {"filename": file.filename,
                "result": result1}
    except:
        jsondata = {"filename": file.filename,
                "result": {"results": []}}
    # is empty results
    if jsondata["result"]["results"]:
        title = jsondata["result"]["results"][0]["recordings"][2].get("title","")
        artist = jsondata["result"]["results"][0]["recordings"][2]["artists"][0].get("name","")
    else:
        title = "could not find the title in acoustid cloud"
        artist = "could not find the artist in acoustid cloud"
    if result2 is not None:
        male_count = result2["male_count"]
        female_count = result2["female_count"]
    else:
        male_count = 0
        female_count = 0
        logger.info("MPS ML model failed to process the audio file")
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

    except:
        logger.info("Email Notification not sent")
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
    shutil.rmtree(OUTPUT_DIR)
    return {"result": body}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")



