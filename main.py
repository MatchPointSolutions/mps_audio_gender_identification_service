from fastapi import FastAPI, File, UploadFile
import uvicorn
from email_notification import send_email
from acr_cloud import acr_cloud_identify_audio
from voice_recognition_model import identify_the_audio
from multi_voice_recognition_model import get_multi_voice_output
from acoust_id import get_acoust_id_audio_details
from config import SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USER, SUBJECT
from log import setup_logger
logger = setup_logger(__name__)
app = FastAPI()

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
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        logger.info(file.filename)
        result = get_acoust_id_audio_details(file.filename)
        body = f"""The Result from processed Audio file:
                    {result}"""
        try:
            send_email(SUBJECT, body,str(receiver_email), SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
            print(f"Email Notification sent to {receiver_email}")
        except:
            print("Email Notification not sent")
        return {"filename": file.filename,
                "result": result}
    except Exception as error:
        return {"Error": str(error)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")


