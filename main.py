from fastapi import FastAPI, File, UploadFile
import uvicorn
from voice_recognition_model import identify_the_audio
from multi_voice_recognition_model import get_multi_voice_output
from log import setup_logger
logger = setup_logger(__name__)
app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["audio/mp3", "audio/aac", "audio/wav"]:
        return {"error": "Invalid file format. Please upload MP3 or WAV files."}

    # Save the file
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    logger.info(file.filename)
    result = identify_the_audio(file.filename)
    return {"filename": file.filename,
            "result": result}


@app.post("/test_multiaudio_pyannote/")
async def upload_file(file: UploadFile = File(...)):
    # if file.content_type not in ["audio/mp3", "audio/aac", "audio/wav"]:
    #     return {"error": "Invalid file format. Please upload MP3 or WAV files."}

    try:
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        logger.info(file.filename)
        result = get_multi_voice_output(file.filename)
        return {"filename": file.filename,
                "result": result}
    except Exception as error:
        return {"Error": str(error)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
