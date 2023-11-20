from fastapi import FastAPI, File, UploadFile
import uvicorn
from voice_recognition_model import identify_the_audio
from log import setup_logger
logger = setup_logger(__name__)
app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["audio/mp3", "audio/aac", "audio/wav", "audio/mpeg", "audio/vnd.dlna.adts"]:
        return {"error": "Invalid file format. Please upload MP3 or AAC files."}

    # Save the file
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    logger.info(file.filename)
    result = identify_the_audio(file.filename)
    return {"filename": file.filename,
            "result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
